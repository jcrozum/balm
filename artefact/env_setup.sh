#!/bin/bash

set -x

# Setup virtual Python environment.
rm -rf env
mkdir -p ./env
python3 -m venv ./env

PIP=./env/bin/pip3

# Install fixed versions of relevant dependencies 
# to aid reproducibility.
$PIP install -r ./dependencies/requirements.txt

# Install AEON
$PIP install biodivine_aeon==0.2.0a4
# If you wish to install aeon from source, replace the line above with:
#$PIP install ./dependencies/biodivine_aeon-0.2.0a4.zip

# Install nfvsmotifs
$PIP install ./dependencies/nfvsmotifs-0.1.zip

# Unzip the model datasets
unzip models.zip