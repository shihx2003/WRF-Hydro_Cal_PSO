#!/bin/bash

cp -r /public/home/Shihuaixuan/Run/Haihe_bak/Haihe_run_source ./run_source
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wrf_env
echo "The environment is activated and script is running."
nohup python3 run.py > ./run.log 2>&1 &
echo "Python script is running in the background. Check the log file for output."
ps aux | grep run.py
