FROM ubuntu:latest
MAINTAINER Dan Sikes "dsikes@renci.org"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install https://s3.amazonaws.com/helium-devops/irods-audit-plugin-message-broker-0.2.1.tar.gz

WORKDIR /mb