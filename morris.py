# -*- encoding: utf-8 -*-
'''
@File    :   .py
@Create  :   2025-05-07 15:57:04
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from SALib.analyze import morris
from util.sample import creat_problem
from util.visual import Draw_morris_mu, Draw_morris_mu_star,  Draw_morris_sigma

events = ['Fuping_20120621', 'Fuping_20130628']
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC', 'NEXP', 'RSURFEXP']
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC', 'NEXP', 'RSURFEXP']
objfun_name = ['Bias', 'PBias', 'RMSE', 'CC', 'NSE', 'KGE']
problem_ini = creat_problem(params)
n_list = [2,4,8,16,32]
for n in n_list:
    path = f'./work/morris_n/Finial/morris_{n}_avg.xlsx'
    param_obj_values = pd.read_excel(path, sheet_name='Sheet1')
    param_values = param_obj_values[params].values
    obj_values = param_obj_values[objfun_name].values

    si_result = {}
    for obj in objfun_name:
        print(f'objfun: {obj}')
        obj_values = param_obj_values[obj].values
        problem = problem_ini.copy()
        Si = morris.analyze(problem, param_values, obj_values, print_to_console=True, num_resamples=10000, seed=42)
        si_result[obj] = Si.to_df()
    
        Draw_morris_mu(problem, Si, filename=f'morris_{n}_avg_{obj}_mu_abs', abs_mu=True)
        Draw_morris_mu_star(problem, Si, filename=f'morris_{n}_avg_{obj}_mu_star')

    # Write all results to a single Excel file with different sheets
    with pd.ExcelWriter(f'./work/morris_n/morris_{n}_morris_results.xlsx') as writer:
        for obj, df in si_result.items():
            df.to_excel(writer, sheet_name=obj)
    print(f"Sensitivity results for n={n} saved to Excel file.")