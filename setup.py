""" irods-audit-plugin-message-broker setup script """
# Author: Dan Sikes - dsikes@renci.org
# Date: 04/11/18
# SOURCE: https://github.com/heliumdatacommons/irods-audit-plugin-message-broker

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='irods-audit-plugin-message-broker',  # Required
    version='0.1.0',  # Required
    description='iRODS audit plugin message broker formats event messages produced by irods into JSON objects',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/pypa/sampleproject',  # Optional
    author='Dan Sikes',
    author_email='dsikes@renci.org',  # Optional
    keywords='irods amqp audit plugin message broker rabbitmq',  # Optional

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=['peppercorn'],  # Optional

    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/heliumdatacommons/irods-audit-plugin-message-broker/issues',
        'Source': 'https://github.com/heliumdatacommons/irods-audit-plugin-message-broker',
    },
)