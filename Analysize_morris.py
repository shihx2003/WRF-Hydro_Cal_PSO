# -*- encoding: utf-8 -*-
'''
@File    :   Analysize_morris.py
@Create  :   2025-04-19 16:09:52
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from SALib.analyze import morris as morris_analyze
import os
import seaborn as sns
from SALib.sample import saltelli
from util.read import read_params
from util.visualSi import Draw_morris_mu, Draw_morris_sigma, Draw_morris_mu_star

sen_path = "F:/Haihe/Run/params_sen/sen/Sen_data.xlsx"
results = pd.read_excel(sen_path, sheet_name='Fuping_20190804')


params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
params_values = np.array(results[params].values, dtype=float)
print(params_values.shape)
params_path = './params/run_params.yaml'
params_info = read_params(params_path, params)

problem_def = {
    'num_vars': len(params_info),
    'names': np.array(list(params_info.keys())),
    'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
}

obj_funs = ['PBias', 'CC', 'RMSE', 'NSE', 'KGE']
obj_Si = {}
for obj_fun in obj_funs:
    problem = problem_def.copy()
    results_values = np.array(results[obj_fun].values, dtype=float)
    
    Si = morris_analyze.analyze(problem, params_values, results_values)
    obj_Si[obj_fun] = Si
    # Draw_sobol_S1_ST(problem, Si, filename=f'S1_ST_{obj_fun}', figsize=(18, 6))
    # Draw_sobol_S2(problem, Si, filename=f'S2_{obj_fun}', figsize=(12, 10))
    Draw_morris_mu(problem, Si, filename=f'morris_mu_{obj_fun}')
    Draw_morris_mu_star(problem, Si, filename=f'morris_mu_sigma_{obj_fun}')
    Draw_morris_sigma(problem, Si, filename=f'morris_sigma_{obj_fun}')
    

