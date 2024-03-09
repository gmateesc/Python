#!/bin/bash

#
# egrep "Power Draw"  gpu_usage_7025277.log  > power_draw.log
#

me=$(basename $0)
here=$(dirname $0)
#cd $here


n_gpu=4

dir=logs_Nvidia/7162616_modes4_nvidia_ok

node=1
gpu=1

while getopts "hn:g:d:" arg; do
  case $arg in
    h)
      echo "Usage: $me [-g gpu_number] [-d log dir]"
      echo "   where 1 <= gpu_number <= 4"
      exit
      ;;
    n)
      node=$OPTARG
      ;;    
    g)
      gpu=$OPTARG
      #echo "procs=$procs"
      ;;
    d)
      dir=$OPTARG
      ;;    
  esac
done

shift $((OPTIND-1))


#
# Get power draw rows
#
egrep "Power Draw" $dir/gpu_usage_[1-9][0-9]*_$node.log  > power_draw.log

#
# Get power draw for a GPU
#
i=1
cat power_draw.log | while read line; do
  r=$(( i % 4 ))
  g=$(( gpu % 4 ))  
  #echo "$i $r $line"
  if [ $i -eq 1 ]; then
    printf 'n_%01d_g_%01d\n' $node $gpu
  fi
  if [ $r -eq $g ]; then
    w=$(echo $line | awk '{print $4}')
    echo "$w"
  fi
  i=$((i + 1 ))
done

