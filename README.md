[diagram1]: irods-audit-plugin-message-broker.png

# iRODS Audit Plugin MessageBroker

This packages primary responsibility is to produce friendly iROD event messages that can be indexed quickly. 


## iRODS Auditing via AMQP
NOTE: You can locate the iRODS Audit Plugin here: https://github.com/irods/irods_rule_engine_plugin_audit_amqp

The MessageBroker package reads all of the audit messages produced by the iRODS rule engine plugin. It is filtering
all of the messages, and converting them into meaniful JSON objects that can be easily indexed.
The JSON object that is produced after filtering is then published back to a pre-defined queue for other workers to consume and do with it what they will.
 
## Building this Package

Here are the required steps to build this package:

1. Clone the Repo into the directory of your choice
2. From the root of the project, run `python setup.py sdist`
3. That will create a `dist/` directory with a tar.gz package inside of it


## Installing this Package

To install this package, simply use `pip`.

`pip install irods-audit-plugin-message-broker-0.1.0.tar.gz`

Note: This package is not available on PyPi, so you will need to build the package before you can install it.


## Starting the Message Broker
To start the message broker, simply use the `start` command.

``` mb start ```


## MessageBroker Options

| Available Option        | Default Value      |
| ------------- |:-------------:|
| --rabbit-mq-host | localhost |
| --rabbit-mq-port | 6372 |
| --rabbitmq-audit-queue | audit_messages |
| --rabbitmq-format-queue | audit_messages_formatted |
| --keymap-file | keymap.yml |


Be sure to provide your optional arguments as needed.

``` mb start --keymap-file=some_different_keymap.yml --rabbitmq-format-queue=some_different_queue ```

If everything is operating properly, whichever queue you have specified to contain your formatted messages
should be populated when iRODS generates any sort of event data.

## End to End Architecture 
The diagram below illustrates the way the MessageBroker is being used:

![alt text][diagram1]


With this in place, anyone who wishes to subscribe to the formatted queue would start recieving 
formatted messages as they are proccessed by the Message Broker. This will allow us to build
various forms of indexers, with little overhead.


### Questions about this Package?
Send me an email at `dsikes@renci.org` if you need assistance with this package.
