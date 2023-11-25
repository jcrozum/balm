#!/bin/bash


PYTHON=./env/bin/python3

# Check that necessary system dependencies are present.

clingo --version > /dev/null
ret=$?
if [ $ret -ne 0 ]; then
    echo "Missing 'clingo'. Maybe run 'apt install gringo'?"
    exit 1
fi

$PYTHON bench/aeon-attractors.py 1 1 ./models/bbm/005.bnet
ret=$?
if [ $ret -ne 0 ]; then
    echo "Error running tsconj. Installation failed?"
    exit 1
fi

echo 
echo
echo " >> Everything seems to be in order."