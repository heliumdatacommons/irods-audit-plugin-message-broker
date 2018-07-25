import json
import yaml
import redis
import logging
import logzero
from logzero import logger
from utils.RabbitMQInit import RabbitMQInit
import os
import errno
import re

def get_log_level(level):
    if level == 'DEBUG':
        return logging.DEBUG
    if level == 'INFO':
        return logging.INFO
    if level == 'WARNING':
        return logging.WARNING
    if level == 'NOTSET':
        return logging.NOTSET
    if level == 'ERROR':
        return logging.ERROR
    if level == 'CRITICAL':
        return logging.CRITICAL

class MessageBroker():
    
    def __init__(self, args):
        self.payload = {}
        self.args = args
        self.config = self.getConf(self.args.config_file)

        # TODO: consider moving connection values for Redis and RabbitMQ into the config file
        # NOTE: its ok to keep the command line options, but to prevent typing out so much.. it could be useful.
        self.r = redis.StrictRedis(host=self.args.redis_host, port=self.args.redis_port, db=self.args.redis_db)
        
        if not os.path.exists(os.path.dirname(self.args.log_file)):
            try:
                os.makedirs(os.path.dirname(self.args.log_file))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        logzero.logfile(self.args.log_file, maxBytes=1e6, backupCount=3)
        logzero.loglevel(get_log_level(self.args.log_level))
        logger.debug("MessageBroker has been instantiated")

    def sanitize(self, message):
        start_sign_post = '__BEGIN_JSON__'
        end_sign_post = '__END_JSON__'

        if start_sign_post in message:
            start = message.find(start_sign_post) + len(start_sign_post)
            end = message.find(end_sign_post)
            return json.loads(message[start:end])
        
        logger.error("unable to sanitize message")
        return None
    
    def getConf(self, conf):
        try:
            with open('%s' % (conf), 'r') as f:
                return yaml.load(f)
        except:
            logger.error("unable to load specified config file %s " % conf)
    
        
    
    def processMessagesByPid(self, pid):
        messages = self.r.lrange('pending_' + pid, 0, -1)
        self.r.delete('pending_' + pid)
        
        keymap = self.config['keymap']

        for message in messages:
            message = json.loads(message)
            final_message = {}
            for key in keymap:
                if key in message:
                    final_message[keymap[key]] = message[key]

            yield final_message

    def consumeUnformattedMessages(self, ch, method, properties, body):
        amqp_message = self.sanitize(body)
        if amqp_message:
            self.r.lpush('pending_' + amqp_message['pid'], json.dumps(amqp_message))

    def consumeFormattedMessages(self):
        logger.debug("starting producer")
        ready_pids = self.r.scan_iter("ready_*")
        logger.debug("detected %d pids that need to be produced" % (len(list(ready_pids))))
        for ready_pid in self.r.scan_iter("ready_*"):
            # get message count
            for message in self.r.lrange( ready_pid, 0, -1):
                message = json.loads(message)
                # publish the newly formatted message onto all configured queues
                for queue in self.config['queues']:
                    logger.debug("publishing new message to %s queue" % (queue))
                    
                    if 'pep_whitelist' in self.config['queues'][queue]:
                        if 'rule_name' in message:
                            if message['rule_name'] in self.config['queues'][queue]['pep_whitelist']:
                                self.rabbit.publish(json.dumps(message), queue)
                    
                    if 'pep_regex' in self.config['queues'][queue] and 'pep_whitelist' not in self.config['queues'][queue]:
                        patterns = []
                        for reg in self.config['queues'][queue]['pep_regex']:
                                patterns.append(re.compile(reg))

                        if 'rule_name' in message:
                            for pattern in patterns:
                                if pattern.match(message['rule_name']):
                                    logger.debug("message matched regex pattern %s " % (self.config['queues'][queue]['pep_regex'][patterns.index(pattern)]))
                                    self.rabbit.publish(json.dumps(message), queue)
                    
            logger.debug("removing key %s from redis" % (ready_pid))
            self.r.delete(ready_pid)
    
    def cleanRedis(self):
        # cleans redis from any messages older than X minutes (calculates it via timestamp from first message in list)
        pass
    
    def formatMessages(self):
        for pending_pid in self.r.scan_iter("pending_*"):
            logger.debug("loading pending pid %s" % pending_pid)
            for message in self.r.lrange( pending_pid, 0, -1):
                message = json.loads(message)
                if 'action' in list(message.keys()):
                    for key in message:
                        if key == 'action' and message[key] == 'END':
                            logger.debug("message %s with END action detected! Moving it to ready!" % (message['pid']))
                            for message in self.processMessagesByPid(message['pid']):
                                self.r.lpush('ready_' + message['pid'], json.dumps(message))

    def start(self):
        self.rabbit = RabbitMQInit(self.args.rabbitmq_host, self.args.rabbitmq_port, self.args.rabbitmq_user, self.args.rabbitmq_pass)

        if self.args.mode == 'producer':
            self.rabbit.consume(self.consumeUnformattedMessages, self.args.rabbitmq_audit_queue)
        
        if self.args.mode == 'formatter':
            self.formatMessages()

        if self.args.mode == 'consumer':
            self.consumeFormattedMessages()
        
        if self.args.mode == 'cleaner':
            self.cleanRedis()