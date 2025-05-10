# -*- encoding: utf-8 -*-
'''
@File    :   sobol_sample.py
@Create  :   2025-04-27 22:33:16
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
from util.sample import creat_problem
from SALib.sample import sobol
from util.jobs import jobs2yaml
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
events = ['Fuping_20120621', 'Fuping_20130628']
problem = creat_problem(params)

param_values = sobol.sample(problem, 16, calc_second_order=True, seed=42)
print(param_values)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'sobol_16_{event}')

param_values = sobol.sample(problem, 8, calc_second_order=True, seed=42)
print(param_values)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'sobol_8_{event}')

param_values = sobol.sample(problem, 4, calc_second_order=True, seed=42)
print(param_values)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'sobol_4_{event}')

param_values = sobol.sample(problem, 2, calc_second_order=True, seed=42)
print(param_values)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'sobol_2_{event}')