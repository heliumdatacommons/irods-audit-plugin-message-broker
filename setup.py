""" irods-audit-plugin-message-broker setup script """
# Author: Dan Sikes - dsikes@renci.org
# Date: 04/11/18
# SOURCE: https://github.com/heliumdatacommons/irods-audit-plugin-message-broker

from setuptools import setup

setup(
    name='irods-audit-plugin-message-broker',
    version='0.4.1',
    description='iRODS audit plugin message broker formats event messages produced by irods into JSON objects',  # Required
    url='https://github.com/pypa/sampleproject',
    author='Dan Sikes',
    author_email='dsikes@renci.org',
    keywords='irods amqp audit plugin message broker rabbitmq',

    packages=['message_broker', 'message_broker.utils'],
    install_requires=['logzero', 'pika', 'pyaml'],
    entry_points={
        'console_scripts': [
            'mb=message_broker:main',
        ],
    }, 
    project_urls={
        'Bug Reports': 'https://github.com/heliumdatacommons/irods-audit-plugin-message-broker/issues',
        'Source': 'https://github.com/heliumdatacommons/irods-audit-plugin-message-broker',
    },
)