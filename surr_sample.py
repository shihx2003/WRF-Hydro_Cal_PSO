# -*- encoding: utf-8 -*-
'''
@File    :   surr_sample.py
@Create  :   2025-04-23 18:54:15
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd

from util.read import read_params
from util.sample import sample_params
from util.jobs import jobs2yaml

def job_sample():
    params = [ 'BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT']
    params_path = '.\\params\\run_params.yaml'
    params_info = read_params(params_path, params)

    problem = {
        'num_vars': len(params_info),
        'names': list(params_info.keys()),
        'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
    }
    n_samples = 200
    PBias_sample = sample_params(problem, n_samples, sample_file='surr_PBias_sample.npy', Resample=True, savenpy=True)
    cal_events = ['Fuping_20160718', 'Fuping_20190804', 'Fuping_20120721', 'Fuping_20200717', 'Fuping_20130811']
    for event in cal_events:
        jobname = f'surr_PBias_{event}'
        jobs = jobs2yaml(params, PBias_sample, event, jobname=jobname, yaml_file=f'{jobname}.yaml')

if __name__ == '__main__':
    job_sample()
