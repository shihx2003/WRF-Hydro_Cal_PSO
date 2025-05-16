#!/bin/bash

cp -r ../run_source ./run_source
source ~/anaconda3/etc/profile.d/conda.sh
conda activate pso
echo "The environment is activated and script is running."
nohup python3 run_pso.py > ./run_pso.log 2>&1 &
echo "Python script is running in the background. Check the log file for output."
ps aux | grep run_pso.py
