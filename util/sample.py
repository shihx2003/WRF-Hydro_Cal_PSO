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
from SALib.sample import latin

from util.read import read_params
from util.jobs import generte_jobs

np.random.seed(42)
random.seed(42)

def sample_params(problem, n, sample_file=None, Resample=True, savenpy=False):

    if os.path.exists(sample_file) and not Resample:
        param_values = np.load(sample_file)
        print("Not Resample : ", param_values.shape)
        return param_values
    
    else:
        param_values = latin.sample(problem, n, seed=42)
        if savenpy:
            np.save(sample_file, param_values)
        print("Resample : ", param_values.shape)

        return param_values

if __name__ == '__main__':

    # params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
    params = [ 'BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT']
    params_path = '.\\params\\run_params.yaml'
    params_info = read_params(params_path, params)

    problem = {
        'num_vars': len(params_info),
        'names': list(params_info.keys()),
        'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
    }

    n_samples = 1000
    sample_params(problem, n_samples, sample_file='PBias_sample.npy', Resample=True, savenpy=True)

