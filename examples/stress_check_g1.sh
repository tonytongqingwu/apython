#!/bin/bash

check_ps () {
  ps_out=`ps -ef | grep $1 | grep -v 'grep' | grep -v $0`
  result=$(echo $ps_out | grep "$1")
  if [[ "$result" != "" ]];then
    echo "Running"
  else
    echo "Not Running"
    bash run_stress_g1.sh 
  fi
}

while :
  echo "checking"
  do
    check_ps stress_g1.py
    sleep 600
  done
