# -*- encoding: utf-8 -*-
'''
@File    :   pso_best_result.py
@Create  :   2025-05-04 14:38:07
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import yaml
import numpy as np
import pandas as pd

from util.jobs import jobs2xlsx, jobs2yaml
from core.ObjFun import CalObjFun
from util.read import read_params_info
events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824', ]

obsdir = 'F:/水文年鉴/'
result_dir = './work/PSO/PSO_Best_re/result'
objs = ['Bias', 'PBias', 'NSE', 'RMSE', 'CC', 'KGE', 'MF']
params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT', 'ChSSlp', 'MannN', 'OVROUGHRTFAC']

result = []
for event in events:
    jobyaml = f'./work/PSO/PSO_Best_re/jobs/PSO_best_re_{event}_{event}.yaml'
    jobinfo = jobs2xlsx(jobyaml, return_info=True)
    if event == 'Fuping_20120621' or event == 'Fuping_20120721' or event == 'Fuping_20130811':
        print('correct')
        run_result = CalObjFun(result_dir, jobyaml,
                                    obsdir=obsdir, draw_pic=False, return_params=True, correct=True)
    else:
        run_result = CalObjFun(result_dir, jobyaml,
                                    obsdir=obsdir, draw_pic=False, return_params=True, correct=False)

    run_result['obj'] = run_result['period'].str.split('_').str[2]
    run_result['cal'] = 'cal_' + run_result['period'].str.split('_').str[0] + run_result['period'].str.split('_').str[1]
    run_result['MF']  = 0.5 * (run_result['KGE'] * (1)) +  0.5 * (run_result['NSE'] * (1))  
    result.append(run_result)

result_df = pd.concat(result, axis=0)
print(result_df)
result_df.to_excel('./work/PSO/PSO_Best_re/PSO_best_all.xlsx', index=False)
with pd.ExcelWriter('./work/PSO/PSO_Best_re/Fun/PSO_best_results.xlsx') as writer:
    for obj in objs:
        if obj == 'MF':
            obj_rows = result_df[result_df['obj'] == 'obj']
        else:
            obj_rows = result_df[result_df['obj'] == obj]
        
        obj_rows = obj_rows.drop(columns=['job_id', 'basin', 'period',] + params + list(set(objs) - set([obj])))
        print(obj_rows)
        pivot_df = obj_rows.pivot_table(index='event_no', columns='cal', values=obj)
        pivot_df = pivot_df.reset_index()
        pivot_df.to_excel(writer, sheet_name=obj, index=False)

