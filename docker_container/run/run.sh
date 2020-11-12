#!/bin/bash

set -e

project_vol=${DS_PROJECT_DIR:-`pwd`/project}
config_vol=${DS_CONFIG_DIR:-`pwd`/config}
secret_vol=${DS_SECRET_DIR:-`pwd`/secret}
port=${DS_PORT:-8888}
image=${DS_IMAGE:-gazprom-neft/ds-py3:cpu}


sudo docker run --rm -p ${port}:8888 \
  -v ${notebooks_vol}:/project \
  -v ${config_vol}:/jupyter/config \
  -v ${secret_vol}:/jupyter/secret \
  $@ \
  ${image}
