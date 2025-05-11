# -*- encoding: utf-8 -*-
'''
@File    :   run_param.py
@Create  :   2025-05-11 21:15:50
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
from traceback import print_tb

from shapely import boundary
from util.read import read_params_info
import pandas as pd
from util.jobs import jobs2yaml

cal_params = {
    'BEXP': 1.757431781478226,
    'ChSSlp': 7.962958396133035,
    'DKSAT': 1.264374709688127,
    'MannN': 6.44956808341667,
    'OVROUGHRTFAC': 0.48209746060892944,
    'REFKDT': 2.7545405408367514,
    'RETDEPRTFAC': 2846.552443067357,
    'SLOPE': 0.11545758228749037,
    'SMCMAX': 0.8036102153360845,
    'LKSATFAC': 5003.681933321059,
    'NEXP': 11.18321152664721,
    'RSURFEXP': 4.485516048967838
}
event = 'Fuping_20190804'
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
param_info_yaml = './params/run_params.yaml'
params_info = read_params_info(param_info_yaml, params)
print(params_info)

for key, info in params_info.items():
    param_name = info['name']
    max_val = info['maxValue']
    ini_val = info['iniValue']
    min_val = info['minValue']
    bound = max_val - min_val

    periods = []
    singeljob = []
    set_param = cal_params.copy()
    set_param[key] = min_val
    singeljob.append(set_param)
    periods.append(f'{key}_{0}')

    for i in range(1, 21):
        periods.append(f'{key}_{i / 20}')
        set_param = cal_params.copy()
        set_param[key] = min_val + i * bound / 20
        singeljob.append(set_param)
    df = pd.DataFrame(singeljob)
    params_values = df[params].values
    df.to_csv(f"./work/floodana/paramsvalues/{key}.csv", index=False)
    jobs =  jobs2yaml(params, params_values, event, jobname=f'{key}_{event}', periods=periods)