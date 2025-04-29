# -*- encoding: utf-8 -*-
'''
@File    :   Sampling.py
@Create  :   2025-04-18 14:17:52
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
from hmac import new
import os
import re
import sys
import yaml
import random
import numpy as np
import pandas as pd
from SALib.sample import latin
from SALib.sample import morris
from SALib.sample import sobol


from util.read import read_params_info
from util.jobs import jobs2yaml

np.random.seed(42)
random.seed(42)

def creat_problem(params, **kwargs):
    """
    Create a problem dictionary for parameter sampling.
    
    Parameters
    ----------
    params : list
        List of parameter names.
    kwargs : dict, optional
        Additional keyword arguments.
        - params_path (str): Path to the YAML file containing parameter information.

    Returns
    ----------
    problem : dict
        Problem dictionary containing number of variables, names, and bounds.
    """

    params_path = kwargs.get('params_path', './params/run_params.yaml')
    params_info = read_params_info(params_path, params)
    problem = {
        'num_vars': len(params_info),
        'names': np.array(list(params_info.keys())),
        'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
    }

    return problem

def sample_params(problem, n, sample_file=None, **kwargs):
    Resample = kwargs.get('Resample', False)
    savenpy = kwargs.get('savenpy', False)
    seed = kwargs.get('seed', 42)

    if os.path.exists(sample_file) and not Resample:
        param_values = np.load(sample_file)
        print("Not Resample : ", param_values.shape)
        return param_values
    
    else:
        param_values = latin.sample(problem, n, seed=seed)
        if savenpy:
            np.save(sample_file, param_values)
        print("Resample : ", param_values.shape)

        return param_values

def central_problem(params, central_point, precent_range=0.1, **kwargs):
    """
    Create a central problem dictionary for parameter sampling.

    Parameters
    ----------
    params : list
        List of parameter names.
    central_point : dict
        Dictionary containing central parameter values.
    precent_range : float, optional
        percentage range for the bounds (default is 0.1).
    kwargs : dict, optional
        Additional keyword arguments.

    Returns
    ----------
        problem : dict
            Central problem dictionary containing number of variables, names, and bounds.
    """

    problem = creat_problem(params)
    print('default problem : ', problem)
    for i in range(len(problem['bounds'])):
        param_name = problem['names'][i]
        maxValue = problem['bounds'][i][1]
        minValue = problem['bounds'][i][0]
        range_len = (problem['bounds'][i][1] - problem['bounds'][i][0]) * precent_range
        problem['bounds'][i][0] = round(max(minValue, central_point[param_name] - range_len), 4)
        problem['bounds'][i][1] = round(min(maxValue, central_point[param_name] + range_len), 4)
    print('new problem : ', problem)
    return problem

def central_sample(params, central_point, n, precent_range=0.1, sample_method='latin', **kwargs):
    """
    Generate a sample of parameters using the specified sampling method.

    Parameters
    ----------
    params : list
        List of parameter names.
    central_point : dict
        Dictionary containing central parameter values.
    n : int
        Number of samples to generate.
    precent_range : float, optional
        Percentage range for the bounds (default is 0.1).
    sample_method : str, optional
        Sampling method to use ('latin', 'morris', or 'sobol').
    kwargs : dict, optional
        Additional keyword arguments.
        - filename (str): Path to save the sample file.
        - seed (int): Random seed for reproducibility.
        - return_problem (bool): Whether to return the problem dictionary.

    Returns
    ----------
    param_values : numpy.ndarray
        Array of sampled parameter values.
    problem : dict, optional
        Central problem dictionary containing number of variables, names, and bounds.

    """
    seed = kwargs.get('seed', 42)
    sample_file = kwargs.get('filename', None)
    return_problem = kwargs.get('return_problem', False)
    problem = central_problem(params, central_point, precent_range)
    print(problem)
    if sample_method == 'latin':
        param_values = latin.sample(problem, n, seed=seed)
    elif sample_method == 'morris':
        param_values = morris.sample(problem, n, seed=seed)
    elif sample_method == 'sobol':
        param_values = sobol.sample(problem, n, seed=seed)
    else:
        raise ValueError("Invalid sample method. Choose from 'latin', 'morris', or 'sobol'.")

    if sample_file is not None:
        np.save(sample_file, param_values)
    print("Resample : ", param_values.shape)

    if return_problem:
        return param_values, problem
    else:
        return param_values



if __name__ == '__main__':

    params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
    # Create a dictionary from parameter values
    central_point = {
        'BEXP': 1.757,
        'ChSSlp': 7.963,
        'DKSAT': 1.264,
        'MannN': 6.450,
        'OVROUGHRTFAC': 0.482,
        'REFKDT': 2.755,
        'RETDEPRTFAC': 2846.552,
        'SLOPE': 0.115,
        'SMCMAX': 0.804,
        'LKSATFAC': 5003.682,
        'NEXP': 11.183,
        'RSURFEXP': 4.486
    }

    sample_size = 100
    param_values = central_sample(params, central_point, sample_size, precent_range=0.1, 
                               sample_method='latin',)

