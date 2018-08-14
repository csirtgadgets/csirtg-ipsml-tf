#!/bin/bash

set -e

rm -rf tmp
mkdir tmp

cat data/whitelist.txt | csirtg-ipsml-tf-train --build --good > tmp/whitelist.csv
cat data/blacklist.txt | csirtg-ipsml-tf-train --build > tmp/blacklist.csv
cat tmp/whitelist.csv tmp/blacklist.csv | gshuf > data/training.csv
time csirtg-ipsml-tf-train
csirtg-ipsml-tf -i '129.79.78.188,21|128.205.1.1,17|189.254.33.157,01|141.142.234.238,17|185.244.25.200,04'