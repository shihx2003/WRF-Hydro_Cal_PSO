# -*- encoding: utf-8 -*-
'''
@File    :   sobol.py
@Create  :   2025-05-07 15:57:04
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
from encodings.punycode import T
import numpy as np
import pandas as pd
from SALib.analyze import sobol
from util.sample import creat_problem
from util.visual import Draw_sobol_S1_ST, Draw_sobol_S2

events = ['Fuping_20120621', 'Fuping_20130628']
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC', 'NEXP', 'RSURFEXP']
objfun_name = ['Bias', 'PBias', 'RMSE', 'CC', 'NSE', 'KGE']
# objfun_name = ['Bias', 'NSE', 'KGE']
problem_ini = creat_problem(params)
n_list = [2,4,8,16,20190804]
for n in n_list:
    path = f'./work/sobol_n/Finial/sobol_{n}_avg.xlsx'
    param_obj_values = pd.read_excel(path, sheet_name='Sheet1')
    param_values = param_obj_values[params].values
    obj_values = param_obj_values[objfun_name].values
    si_result = {}
    for obj in objfun_name:
        print(f'objfun: {obj}')
        obj_values = param_obj_values[obj].values
        problem = problem_ini.copy()
        Si = sobol.analyze(problem, obj_values, calc_second_order=True, print_to_console=False, num_resamples=10, seed=42)
        si_result[obj] = Si.to_df()
        # print(type(Si.to_df()))
        Draw_sobol_S1_ST(problem, Si, filename=f'sobol_{n}_avg_{obj}_S1', abs_si=True)
        Draw_sobol_S2(problem, Si, filename=f'sobol_{n}_avg_{obj}_S2', abs_si=True)

    # Write all results to a single Excel file with different sheets
    with pd.ExcelWriter(f'./work/sobol_n/sobol_{n}_sobol_results.xlsx') as writer:
        for obj, dfs in si_result.items():
            df = pd.concat(dfs, axis=1)
            df = df.reset_index()
            df = df.rename(columns={'index': obj})
            print(df)
            df.to_excel(writer, sheet_name=obj)
    print(f"Sensitivity results for n={n} saved to Excel file.")