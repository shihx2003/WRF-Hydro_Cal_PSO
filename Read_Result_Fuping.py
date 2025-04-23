# -*- encoding: utf-8 -*-
'''
@File    :   read_result.py
@Create  :   2025-04-05 13:00:48
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib

import os
import yaml
import numpy as np
import util.wrfhydrofrxst as whf
from util.read import read_obs, read_jobs
from core import ObjFun
import pandas as pd


station = {'1':'Fuping'}
basin = 'Fuping'
event_no = '20200824'

job_ids, _ = read_jobs(f'./jobs/sen_jobs_Fuping_{event_no}.yaml')

obs_events, obs_info = read_obs(basin, event_no)

obs_events[event_no] = obs_events[event_no][(obs_events[event_no]['Date'] <= pd.to_datetime('2020-09-01 08:00:00', format='%Y-%m-%d %H:%M:%S'))]
pb_values = []
cc_values = []
rmse_values = []
nse_values = []
kge_values = []

for job_id in job_ids:

    result_name = f'./result/Fuping_Sen_{event_no}/{job_id}_Fuping_{event_no}.txt'
    sim = whf.Readfrxst_pts_out(result_name, station)
    sim = whf.ConvertTimeZone(sim, 'UTC', 'Asia/Shanghai')

    sim = sim[(sim['Date'] >= obs_info[event_no][0]) & (sim['Date'] <= obs_info[event_no][1])]
    sim = sim.rename(columns={f'Fuping_{job_id}_Fuping_{event_no}': f'Fuping_Sen_{event_no}_{job_id}'})

    pb = ObjFun.PBias(obs_events[event_no], sim)[f'Fuping_Sen_{event_no}_{job_id}']
    cc = ObjFun.CC(obs_events[event_no], sim)[f'Fuping_Sen_{event_no}_{job_id}']
    rmse = ObjFun.RMSE(obs_events[event_no], sim)[f'Fuping_Sen_{event_no}_{job_id}']
    nse = ObjFun.NSE(obs_events[event_no], sim)[f'Fuping_Sen_{event_no}_{job_id}']
    kge = ObjFun.KGE(obs_events[event_no], sim)[f'Fuping_Sen_{event_no}_{job_id}']
    
    pb_values.append(pb)
    cc_values.append(cc)
    rmse_values.append(rmse)
    nse_values.append(nse)
    kge_values.append(kge)


    # if kge >= 0.0:
    #     whf.DrawStreamFlow(obs_events[event_no], sim, f'AA_{round(kge,2)}_Fuping_Sen_{event_no}_{job_id}')
    # else:
    #     whf.DrawStreamFlow(obs_events[event_no], sim, f'{round(kge,2)}_Fuping_Sen_{event_no}_{job_id}')

path = r"F:\Haihe\Run\params_sen\sen\job_values.xlsx"
params_value = pd.read_excel(path, sheet_name='Sheet1')
obj_df = pd.DataFrame({'Job_id': job_ids,  'PBias': pb_values, 'CC': cc_values, 'RMSE': rmse_values, 'NSE': nse_values, 'KGE': kge_values})
obj_df.to_excel(f'./sen/Fuping_{event_no}_obj.xlsx', index=False)
merged_df = pd.merge(params_value, obj_df, on='Job_id', how='inner')
merged_df.to_excel(f'./sen/Fuping_{event_no}_sendate.xlsx', index=False)
