# -*- encoding: utf-8 -*-
'''
@File    :   morris_n_sample.py
@Create  :   2025-04-27 22:33:16
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
from util.sample import creat_problem
from SALib.sample import morris
from util.jobs import jobs2yaml
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
events = ['Fuping_20120621', 'Fuping_20130628']
problem_ini = creat_problem(params)

problem = problem_ini.copy()
param_values = morris.sample(problem, 32, seed=42)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'morris_32_{event}')

problem = problem_ini.copy()
param_values = morris.sample(problem, 16, seed=42)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'morris_16_{event}')

problem = problem_ini.copy()
param_values = morris.sample(problem, 8, seed=42)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'morris_8_{event}')

problem = problem_ini.copy()
param_values = morris.sample(problem, 4, seed=42)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'morris_4_{event}')

problem = problem_ini.copy()
param_values = morris.sample(problem, 2, seed=42)
for event in events:
    jobs = jobs2yaml(params, param_values=param_values, eventname=event, jobname=f'morris_2_{event}')