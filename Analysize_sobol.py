# -*- encoding: utf-8 -*-
'''
@File    :   analysize.py
@Create  :   2025-04-19 15:47:00
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from SALib.analyze import sobol as sobol_analyze
import os
import seaborn as sns
from SALib.sample import saltelli
from util.read import read_params
from util.visual import Draw_sobol_S1_ST, Draw_sobol_S2
import matplotlib.pyplot as plt

sen_path = "F:/Haihe/Run/params_sen/sen/Sen_data.xlsx"
results = pd.read_excel(sen_path, sheet_name='Fuping_20190804')


params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
params_path = './params/run_params.yaml'
params_info = read_params(params_path, params)

problem = {
    'num_vars': len(params_info),
    'names': np.array(list(params_info.keys())),
    'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
}

obj_funs = ['PBias', 'CC', 'RMSE', 'NSE', 'KGE']
obj_Si = {}
for obj_fun in obj_funs:
    results_values = np.array(results[obj_fun].values, dtype=float)

    Si = sobol_analyze.analyze(problem, results_values, calc_second_order=True, print_to_console=False)
    obj_Si[obj_fun] = Si
    # Draw_sobol_S1_ST(problem, Si, filename=f'S1_ST_{obj_fun}', figsize=(18, 6))
    Draw_sobol_S2(problem, Si, filename=f'S2_{obj_fun}', figsize=(12, 10))
