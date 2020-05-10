#!/bin/bash

PACKAGE_PATH=$(dirname $0);

push="$1"
if [[ "$push" = "--push" ]]; then
  build_type="$2"
else
  push=""
  build_type="$1"
fi

if [[ "$build_type" = "" ]]; then
  build_type="docker";
fi

IMAGE_NAME=dumbgdrive
DOCKER_IMAGE_NAME=b3m2a1/dumbgdrive
if [[ "$build_type" = "docker" ]]; then
  docker build -t IMAGE_NAME -f $PACKAGE_PATH/Dockerfile $PACKAGE_PATH
  if [[ "$push" == "--push" ]]; then
    docker tag IMAGE_NAME DOCKER_IMAGE_NAME
    docker push DOCKER_IMAGE_NAME
  fi
fi