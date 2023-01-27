#!/bin/bash

here=$(dirname $0)
cd $here

egrep "174336" ../scripts/postprocessed_monitoring_24.txt | egrep -v "174336 174336" \
      | awk '{print $4}' > n24_174336_x.csv
