
FROM ubuntu:eoan-20200410

# we assume we build from _outside_ this directory?
ADD . /home/DumbGDrive

RUN \
  apt-get update &&\
  apt-get -y install python3.7 python3-pip &&\
  apt-get clean

RUN \
  pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

ENTRYPOINT ["python3", "/home/DumbGDrive/CLI.py"]