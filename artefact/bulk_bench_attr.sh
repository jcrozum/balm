#!/bin/bash

set -x

mkdir -p ./results/attr/

echo "model elapsed attractors" > ./results/attr/bbm_aeon.tsv
./bulk_bench.sh ./models/bbm-bnet-inputs-random-128 1h ./bench/attr-aeon.py >> ./results/attr/bbm_aeon.tsv
trap 'exit 2' SIGINT
