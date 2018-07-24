import json
import yaml
import redis
from logzero import logger
from utils.RabbitMQInit import RabbitMQInit



class MessageBroker():
    
    def __init__(self, args):
        self.payload = {}
        self.args = args
        self.r = redis.StrictRedis(host=self.args.redis_host, port=self.args.redis_port, db=self.args.redis_db)
        logger.debug("MessageBroker has been instantiated")

    def sanitize(self, message):
        logger.debug("recieved new message to sanitize")
        start_sign_post = '__BEGIN_JSON__'
        end_sign_post = '__END_JSON__'

        if start_sign_post in message:
            start = message.find(start_sign_post) + len(start_sign_post)
            end = message.find(end_sign_post)
            logger.debug("sanitzed message successfully")
            return json.loads(message[start:end])
        
        logger.error("unable to sanitize message")
        return None
    
    def getQueues(self):
        try:
            with open('%s' % (self.args.queueconfig), 'r') as f:
                return yaml.load(f)
        except:
            logger.error("unable to load specified queue config file %s " % self.args.queueconfig)
        
    
    def processMessagesByPid(self, pid):
        messages = self.r.lrange(pid, 0, -1)
        try:
            with open('%s' % (self.args.keymap_file), 'r') as f:
                keymap = yaml.load(f)
        except:
            logger.error("unable to load specified keymap file %s " % self.args.keymap_file)

        for message in messages:
            message = json.loads(message)
            final_message = {}
            for key in keymap:
                if key in message:
                    final_message[keymap[key]] = message[key]

            yield final_message

    def consumeMessage(self, ch, method, properties, body):
        amqp_message = self.sanitize(body)
        if amqp_message:
            queueconfig = self.getQueues()
            self.r.lpush(amqp_message['pid'], json.dumps(amqp_message))
            for key in amqp_message:
                if key == 'action' and amqp_message[key] == 'END':
                    for message in self.processMessagesByPid(amqp_message['pid']):
                    # publish the newly formatted message onto all configured queues
                        for queue in queueconfig['queues']:
                            logger.debug("publishing formatted message to %s queue" % (queue))
                            self.rabbit.publish(json.dumps(message), queue)

    def start(self):
        self.rabbit = RabbitMQInit(self.args.rabbitmq_host, self.args.rabbitmq_port, self.args.rabbitmq_user, self.args.rabbitmq_pass)
        self.rabbit.consume(self.consumeMessage, self.args.rabbitmq_audit_queue)
        
