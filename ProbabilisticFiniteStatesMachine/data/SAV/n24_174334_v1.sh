#!/bin/bash

here=$(dirname $0)
cd $here

egrep "174334 174942" ../scripts/postprocessed_monitoring_24.txt \
      | awk '{print $4}' > n24_174334_174942.csv
