import sys
import argparse
from logzero import logger
import traceback
import os

from MessageBroker import MessageBroker

def main():
    
    try:

        parser = argparse.ArgumentParser()
        parser.add_argument("start", help="Start the MessageBroker ") 
        parser.add_argument("--log-level", help="What level should the logger be run at ", default='DEBUG')
        parser.add_argument("--log-file", help="Specify what file should the logger write to", default='/var/log/mb/mb.log')
        parser.add_argument("--rabbitmq-host", help="Which RabbitMQ server should the MessageBroker connect to ", default='localhost')
        parser.add_argument("--rabbitmq-port", help="Which port the RabbitMQ server is listening on ", default=5672)
        parser.add_argument("--rabbitmq-user", help="Which user to connect to RabbitMQ with", default="guest")
        parser.add_argument("--rabbitmq-pass", help="Which password to use to connect to the RabbitMQ instance", default="guest")
        parser.add_argument("--rabbitmq-audit-queue", help="Which queue is iRODS publishing to ", default='audit_messages')
        parser.add_argument("--disable-keymap", help="Disable keymapping for debugging purposes.", default=False)
        parser.add_argument("--keymap-file", help="Provide a keymap file for the MessageBroker to use during filtering ", default='keymap.yml')
        parser.add_argument("--redis-host", help="Provide a redis host to connect to for intermediate message storage", default="localhost")
        parser.add_argument("--redis-port", help="Provide alternate Redis port", default=6379)
        parser.add_argument("--redis-db", help="Select the Redis logical database having the specified zero-based numeric index.", default=0)
        parser.add_argument("--queueconfig", help="Provide a queue config file for the MessageBroker to know which queues to populate with formatted messages ", default='queueconfig.yml')


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
        tb = traceback.format_exc()
        if 'DEBUG' not in os.environ:
            logger.error(str(e))
        else:
            print tb

if __name__ == '__main__':
    main()