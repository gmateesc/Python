#!/bin/bash

here=$(dirname $0)
cd $here

p="174335"
t="174949"

egrep "$p $t" ../scripts/postprocessed_monitoring_24.txt \
      | awk '{print $4}' > n24_${p}_${t}.csv

#egrep "174335 174949" postprocessed_monitoring_24.txt | awk '{print $4}' > n24_174335_174949.csv
