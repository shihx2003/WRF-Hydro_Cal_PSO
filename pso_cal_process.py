# -*- encoding: utf-8 -*-
'''
@File    :   pso_cal_process.py
@Create  :   2025-05-10 13:03:03
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import numpy as np
import pandas as pd
import seaborn as sns


events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824', ]
events = ['Fuping_20190804re','Fuping_20130628']
params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT', 'ChSSlp', 'MannN', 'OVROUGHRTFAC', 'RETDEPRTFAC', 'LKSATFAC', 'NEXP', 'RSURFEXP']
obj_funs = ['Bias', 'PBias', 'NSE', 'RMSE', 'CC', 'KGE', 'obj']


cal_result_dir = './work/PSO/PSO_All/'

for event in events:
    path = cal_result_dir + f'PSO_{event}.xlsx'
    # Read the data
    df = pd.read_excel(path, sheet_name='Sheet1')
    df = df.drop(columns=['job_id.1'])
    df['iter'] = df['job_id'].str.split('_').str[1].astype(int)
    # df.to_excel('F:/Haihe/FinalPaperDate/PSO/cal/' + f'PSO_{event}_best2.xlsx', index=False)

    grouped_df = df.groupby('iter')
    best_rows = []
    for iter_num, group in grouped_df:
        top_two = group.sort_values('obj').head(1).copy()
        top_two['iteration'] = iter_num
        best_rows.extend(top_two.to_dict('records'))
    best_df = pd.DataFrame(best_rows)
    print(best_df)
    # best_df.to_excel('F:/Haihe/FinalPaperDate/PSO/cal/' + f'PSO_{event}_best.xlsx', index=False)

    wrts = []
    for iter_num, group in grouped_df:
        wrt = group[['iter', 'obj']].sort_values('obj', ascending=False)
        wrt = wrt.drop(columns=['iter'])
        wrt = wrt.rename(columns={'iter': f'iter_{iter_num}', 'obj': f'obj_{iter_num}'})
        wrt = wrt.reset_index(drop=True)
        wrts.append(wrt)

    wrt_df = pd.concat(wrts, axis=1)
    wrt_df.to_excel('F:/Haihe/Run/params_sen/work/PSO/PSO_All/cal/' + f'PSO_{event}_calpro.xlsx', index=True)
