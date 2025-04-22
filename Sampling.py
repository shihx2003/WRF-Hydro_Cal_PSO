# -*- encoding: utf-8 -*-
'''
@File    :   Sampling.py
@Create  :   2025-04-18 14:17:52
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import sys
import yaml
import random
import numpy as np
import pandas as pd


from SALib.analyze import sobol as sobol_analyze
from SALib.sample import sobol as sobol_sample

np.random.seed(42)
random.seed(42)

def read_params(path,params):
    params_info = {}
    params_ymal = yaml.safe_load(open(path, 'r', encoding='utf-8'))
    for param in params:
        if param in params_ymal.keys():
            params_info[param] = params_ymal[param]
        else:
            print(f"Parameter '{param}' not found in the YAML file.")
    
    return params_info

def sample_params(problem, n, sample_file=None, Resample=False):
    """
    """

    if os.path.exists(sample_file) and not Resample:
        param_values = np.load(sample_file)
        print("Not Resample : ", param_values.shape)

        return param_values
    else:
        param_values = sobol_sample.sample(problem, n, seed=42)
        np.save(sample_file, param_values)
        print("Resample : ", param_values.shape)

        return param_values

def generte_jobs(params, param_values, ymal_file=None):
    jobs = {}
    print(f"Number of jobs: {len(param_values)}")
    for i in range(len(param_values)):
        value = param_values[i]
        set_params = {}
        for j, param in enumerate(params):
            set_params[param] = float(value[j])
        job_info = {
                'job_id': f'Sen_{i+1}',
                'period': 'Not Supported',
                'event_no': 'Fuping_20200824',
                'basin' : 'Fuping',
                'set_params': set_params
            }
        jobs[f'Sen_{i+1}'] = job_info

    if ymal_file is None:
        ymal_file = 'sen_jobs.yaml'
    with open(f'./jobs/{ymal_file}', 'w', encoding='utf-8') as f:
        yaml.dump(jobs, f, default_flow_style=False, sort_keys=False)

    return jobs

params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
params_path = '.\\params\\run_params.yaml'
params_info = read_params(params_path, params)

problem = {
    'num_vars': len(params_info),
    'names': list(params_info.keys()),
    'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
}

n_sample = 16
sample_file = "params_value.npy"
params_value = sample_params(problem, n_sample, sample_file=sample_file, Resample=False)
generte_jobs(params_info, params_value, ymal_file='sen_jobs_Fuping_20200824.yaml')


df = pd.DataFrame(params_value, columns=list(params_info.keys()))
df.to_csv("params_value.csv", index=False)
print(df.head())