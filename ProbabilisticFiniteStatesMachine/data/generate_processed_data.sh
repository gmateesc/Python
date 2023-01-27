#!/bin/bash

#
# Script to generate processed CSV data from the
# raw data created by postprocess_monitoring.sh
#

me=$(basename $0)
here=$(dirname $0)
cd $here


procs=12
#procs=24

while getopts "hp:" arg; do
  case $arg in
    h)
      echo "Usage: $me [-p num_procs"
      exit
      ;;
    p)
      procs=$OPTARG
      echo "procs=$procs"
      ;;
  esac
done

shift $((OPTIND-1))



raw_dir=msn_6frag_efmo_rhf_n48/01_raw
processed_dir=msn_6frag_efmo_rhf_n48/02_processed


raw_file=$raw_dir/n${procs}/postprocessed_monitoring_${procs}.txt
processed_file_path=$processed_dir/n${procs}

mkdir -p $processed_file_path


PIDs=$(cat $raw_file | awk '{print $1}' | egrep -v "^#|PID" | egrep "^[0-9]+" | sort -u -n)

i=1
for pid in $PIDs; do
  echo $i $pid
  #i2=$(printf %02s $i)
  #egrep "$pid" $raw_file | egrep -v "${pid}.*${pid}" | awk '{print $4}' > n24_${i2}_${pid}.csv
  egrep "$pid" $raw_file | egrep -v "${pid}.*${pid}" | awk '{print $4}' > $processed_file_path/n${procs}_${pid}.csv  
  (( i = i + 1 ))
  #if [ $i -ge 3 ]; then
  #  break
  #fi
done

