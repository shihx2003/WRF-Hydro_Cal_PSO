# -*- encoding: utf-8 -*-
'''
@File    :   generte_jobs.py
@Create  :   2025-04-23 13:01:26
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import yaml
import numpy as np
import pandas as pd
from util.read import read_params_info

def jobs2yaml(paramsnames, param_values, eventname, **kwargs):
    """
    Generate a YAML file containing job information based on parameter values.
    'job_id' =  f'{jobname}_{i+1}'
    
    Parameters
    ----------
    paramsnames : list
        List of parameter names.
    param_values : np.ndarray
        Array of parameter values for each job.
    eventname : str
        Event name for the job.
    kwargs : dict, optional
        Additional keyword arguments.
        - params_path (str): Path to the YAML file containing parameter information, default is './params/run_params.yaml'.
        - jobname (str): Name of the job, default is 'Run'.
        - fixed_parmas (dict): Fixed parameters for the job, default is None.
        - yaml_file (str): Name of the output YAML file, default is '{jobname}_{eventname}.yaml'.
    
    Returns
    ----------
    jobs : dict
        Dictionary containing job information.
    """
    params_path = kwargs.get('params_path', './params/run_params.yaml')
    jobname = kwargs.get('jobname', 'Run')
    fixed_parmas = kwargs.get('fixed_parmas', None)
    periods = kwargs.get('periods', None)

    basin, no = eventname.split('_')[0], eventname.split('_')[1]
    yaml_file = kwargs.get('yaml_file', f'{jobname}_{eventname}.yaml')
    params_info = read_params_info(params_path, paramsnames)

    jobs = {}
    for i in range(len(param_values)):
        value = param_values[i]
        if periods is not None:
            period = periods[i]
        else:
            period = 'Not_Supported'
        
        if fixed_parmas is not None:
            set_params = fixed_parmas.copy()
        else:
            set_params = {}

        for j, param in enumerate(params_info):
            set_params[param] = float(value[j])
        job_info = {
                'job_id': f'{jobname}_{i+1}',
                'period': period,
                'event_no': f'{eventname}',
                'basin' : f'{basin}',
                'set_params': set_params
            }
        jobs[f'{jobname}_{i+1}'] = job_info

    with open(f'./jobs/{yaml_file}', 'w', encoding='utf-8') as f:
        yaml.dump(jobs, f, default_flow_style=False, sort_keys=False)
    print(f"Number of jobs: {len(param_values)}, saved to {yaml_file}")

    return jobs


def jobs2xlsx(yaml_path, xlsx_path=None, **kwargs):
    """
    Convert a YAML file containing job information into an Excel file.

    Parameters
    ----------
    yaml_path : str
        Path to the YAML file containing job information.
    xlsx_path : str, optional
        Path to save the Excel file. If None, the Excel file will not be saved.
    kwargs : dict, optional
    

    Returns
    ----------
    

    """
    return_info = kwargs.get('return_info', False)
    with open(yaml_path, 'r', encoding='utf-8') as f:
        loaded_jobs = yaml.load(f, Loader=yaml.FullLoader)

    rows = []
    for sen_id, sen_data in loaded_jobs.items():
        set_params = sen_data['set_params']
        if return_info:
            row =  {'job_id': sen_id,
                    'event_no': sen_data['event_no'],
                    'basin': sen_data['basin'],
                    'period': sen_data['period'],
                    }
        else:
            row = {'job_id': sen_id}
        row.update(set_params)
        rows.append(row)
    params_values = pd.DataFrame(rows)
    if xlsx_path is not None:
        params_values.to_excel(xlsx_path, index=False)

    return params_values

