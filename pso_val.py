# -*- encoding: utf-8 -*-
'''
@File    :   pso_val.py
@Create  :   2025-05-03 19:37:46
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import numpy as np
import pandas as pd
from util.jobs import jobs2yaml

events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824', ]

obj = ['Bias', 'PBias', 'NSE', 'RMSE', 'CC', 'KGE', 'obj']
# params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT', 'ChSSlp', 'MannN', 'OVROUGHRTFAC']

params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT', 'ChSSlp', 'MannN', 'OVROUGHRTFAC', 'RETDEPRTFAC', 'LKSATFAC', 'NEXP', 'RSURFEXP']

path = './work/PSO/PSO_best_d.xlsx'
df = pd.read_excel(path, sheet_name='resen')
df['periods'] = df['event'] + '_' + df['best_for']

periods = df['periods'].tolist()
params_values = df[params].values
for event in events:
    jobs =  jobs2yaml(params, params_values, event, jobname=f'PSO_best_re_{event}', periods=periods)
print(df)