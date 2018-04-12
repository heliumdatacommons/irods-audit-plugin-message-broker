import sys
import argparse
from logzero import logger

from MessageBroker import MessageBroker

def main():
    
    try:

        parser = argparse.ArgumentParser()
        parser.add_argument("start", help="Start the MessageBroker ") 
        parser.add_argument("--log-level", help="What level should the logger be run at ", default='critical')
        parser.add_argument("--rabbitmq-host", help="Which RabbitMQ server should the MessageBroker connect to ", default='localhost')
        parser.add_argument("--rabbitmq-port", help="Which port the RabbitMQ server is listening on ", default=5672)
        parser.add_argument("--rabbitmq-user", help="Which user to connect to RabbitMQ with", default="guest")
        parser.add_argument("--rabbitmq-pass", help="Which password to use to connect to the RabbitMQ instance", default="guest")
        parser.add_argument("--rabbitmq-audit-queue", help="Which queue is iRODS publishing to ", default='audit_messages')
        parser.add_argument("--rabbitmq-format-queue", help="Which queue should the MessageBroker publish formatted messages to ", default='audit_messages_formatted') 
        parser.add_argument("--keymap-file", help="Provide a keymap file for the MessageBroker to use during filtering ", default='keymap.yml')


        # get the provided arguments for this instance of the MessageBroker
        args = parser.parse_args()
        
        # instantiate our MessageBroker class with the provided arguments
        mb = MessageBroker(args)

        # Start the MessageBroker (mb start)
        mb.start()

    except KeyboardInterrupt:
        print "Message Broker is going down now!"
        sys.exit(1)
    
    except Exception, e:
        logger.error(str(e))

if __name__ == '__main__':
    main()