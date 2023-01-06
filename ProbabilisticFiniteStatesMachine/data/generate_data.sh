#!/bin/bash

here=$(dirname $0)
cd $here

PIDs=$(cat ../scripts/postprocessed_monitoring_24.txt | awk '{print $1}' | egrep -v "^#|PID" | egrep "^[0-9]+" | sort -u -n)

i=1
for pid in $PIDs; do
  echo $i $pid
  #i2=$(printf %02s $i)
  #egrep "$pid" ../scripts/postprocessed_monitoring_24.txt | egrep -v "${pid}.*${pid}" | awk '{print $4}' > n24_${i2}_${pid}.csv
  egrep "$pid" ../scripts/postprocessed_monitoring_24.txt | egrep -v "${pid}.*${pid}" | awk '{print $4}' > n24_${pid}.csv  
  (( i = i + 1 ))
  #if [ $i -ge 3 ]; then
  #  break
  #fi
done
