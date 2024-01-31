#!/bin/bash


PYTHON=./env/bin/python3

# Check that necessary system dependencies are present.

echo " > Checking 'clingo'"
clingo --version > /dev/null
ret=$?
if [ $ret -ne 0 ]; then
    echo "Missing 'clingo'. Maybe run 'apt install gringo'?"
    exit 1
fi

echo " > Checking 'mole'"
mole &> /dev/null
ret=$?
if [ $ret -ne 1 ]; then
    echo "Missing 'mole'. Forgot to add ./dependencies/mole-140428 to PATH?"
    exit 1
fi

echo " > Checking 'AEON.py'"
$PYTHON ./bench/attr-aeon.py ./models/bbm-bnet-inputs-random-128/005.bnet > /dev/null
ret=$?
if [ $ret -ne 0 ]; then
    echo "Error running AEON. Installation failed?"
    exit 1
fi

echo
echo " >> Everything seems to be in order."