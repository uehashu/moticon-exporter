#!/usr/bin/env bash

#!/bin/sh
currentDir=$(echo $(cd $(dirname $0) && pwd))
PYTHON_SITE_PACKAGES=${currentDir}/site-packages

export PYTHONPATH=$PYTHONPATH:${PYTHON_SITE_PACKAGES}
export TK_SILENCE_DEPRECATION=1
export H5PY_DEFAULT_READONLY=1

python3 moticon-exporter.py
