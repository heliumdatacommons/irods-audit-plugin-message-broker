import json
import yaml
from logzero import logger
from utils.RabbitMQInit import RabbitMQInit



class MessageBroker():
    
    def __init__(self, args):
        logger.debug("MessageBroker has been instantiated")
        self.payload = {}
        self.args = args

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
                self.queueconfig = yaml.load(f)
        except:
            logger.error("unable to load specified queue config file %s " % self.args.queueconfig)
        
    
    def processMessage(self, id, message):

        try:
            with open('%s' % (self.args.keymap_file), 'r') as f:
                keymap = yaml.load(f)
        except:
            logger.error("unable to load specified keymap file %s " % self.args.keymap_file)
        
        final_message = {}
        for key in keymap:
            if key in message:
                final_message[keymap[key]] = message[key]

        return final_message

    def consumeMessage(self, ch, method, properties, body):
        amqp_message = self.sanitize(body)

        if amqp_message:
            if amqp_message['pid'] not in self.payload:
                self.payload[amqp_message['pid']] = {}

            for key in amqp_message:
                self.payload[amqp_message['pid']][key] = amqp_message[key]
                if key == 'action' and amqp_message[key] == 'END':
                    formatted_message = self.processMessage(amqp_message['hostname'] + ':' + amqp_message['pid'], self.payload[amqp_message['pid']])

                    # load in our configured queues
                    self.getQueues()

                    # publish the newly formatted message onto all configured queues
                    for queue in self.queueconfig['queues']:
                        logger.debug("publishing formatted message to %s queue" % (queue))
                        self.rabbit.publish(json.dumps(formatted_message), queue)

    def start(self):
        self.rabbit = RabbitMQInit(self.args.rabbitmq_host, self.args.rabbitmq_port, self.args.rabbitmq_user, self.args.rabbitmq_pass)
        self.rabbit.consume(self.consumeMessage, self.args.rabbitmq_audit_queue)
        
