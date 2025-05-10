# -*- encoding: utf-8 -*-
'''
@File    :   morris_surr.py
@Create  :   2025-05-08 19:16:08
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from SALib.analyze import sobol as sobol_analyze
from SALib.sample import sobol as sobol_sample
from util.sample import creat_problem
import joblib
from util.visual import Draw_sobol_S1_ST, Draw_sobol_S2

params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC', 'NEXP', 'RSURFEXP']
objfun_name = ['Bias', 'PBias', 'RMSE', 'CC', 'NSE', 'KGE']
problem = creat_problem(params)

n = 1024*2

param_values = sobol_sample.sample(problem, n, calc_second_order=True, seed=42)
rf = joblib.load('./models/RF.pkl')

print(param_values.shape)

y_pred = rf.predict(param_values)
print(y_pred.shape)

for i in range(len(objfun_name)):
    obj = objfun_name[i]
    print(f'objfun: {obj}')
    obj_values = y_pred[:, i]
    Si = sobol_analyze.analyze(problem, obj_values, calc_second_order=True, print_to_console=True, num_resamples=10, seed=42)
    Draw_sobol_S1_ST(problem, Si, filename=f'sobol_{n}_surr_{obj}_S1', abs_si=False)
    Draw_sobol_S2(problem, Si, filename=f'sobol_{n}_surr_{obj}_S2', abs_si=False)