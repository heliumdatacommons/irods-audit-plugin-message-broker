import pika
from logzero import logger

class RabbitMQInit():

    def __init__(self, host):
        self.host = host

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
    
    def consume(self, callback, queue='', no_ack=True):
        if queue == '':
            raise Exception("unable to consume. No queue provided.")
        
        logger.debug("consuming from queue %s" % (queue))
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(callback, queue=queue, no_ack=no_ack)
        self.channel.start_consuming()
    
    def publish(self, message, queue=''):
        if queue == '':
            raise Exception("unable to publish. No queue provided.")

        logger.debug("publishing to queue %s" % (queue))
        self.channel.queue_declare(queue=queue)   
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)

    def close(self):
        self.connection.close()