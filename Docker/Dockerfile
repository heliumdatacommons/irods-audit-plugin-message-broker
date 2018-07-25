FROM ubuntu:latest
MAINTAINER Dan Sikes "dsikes@renci.org"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install https://s3.amazonaws.com/helium-devops/irods-audit-plugin-message-broker-0.4.5.tar.gz

WORKDIR /mb