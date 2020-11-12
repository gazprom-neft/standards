#!/bin/bash

export JUPYTER_CONFIG_DIR=/jupyter/config

exec jupyter lab --no-browser --allow-root
