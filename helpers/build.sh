#!/bin/bash

set -e

rm -rf tmp
mkdir tmp

cat data/whitelist.txt | csirtg-ipsml-tf-train --build --good > tmp/whitelist.csv
cat data/blacklist.txt | csirtg-ipsml-tf-train --build > tmp/blacklist.csv
cat tmp/whitelist.csv tmp/blacklist.csv | gshuf > data/training.csv
#time csirtg-ipsml-tf-train
