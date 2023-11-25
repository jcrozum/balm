#!/bin/bash

MODEL_DIR=$1
TIMEOUT=$2
TOOL=$3

# The tested limit was 2^26kB 67_108_864kB ~ 67GB
if [[ -z "${MEMORY_LIMIT}" ]]; then
  echo "Please set env. variable MEMORY_LIMIT appropriate for your system (number, in kB)."
  exit 1
fi

ulimit -v $MEMORY_LIMIT

for MODEL in `ls $MODEL_DIR | grep "\.bnet"`
do
    timeout $TIMEOUT ./env/bin/python3 $TOOL $MODEL_DIR/$MODEL
    ret=$?
    # 124 is the return code for timeout.
    if [ $ret -eq 124 ]; then
            echo -e "$MODEL_DIR/$MODEL\tTIMEOUT"
    fi
    # Properly exit the loop if Ctrl+C is pressed.
    trap 'exit 2' SIGINT
done