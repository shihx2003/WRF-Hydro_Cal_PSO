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
from core import obj_fun
import pandas as pd

station = {'1':'Zhongtangmei'}
basin = 'Zhongtangmei'
event_no = '20190804'

job_ids, _ = read_jobs('./jobs/sen_jobs_Zhongtangmei_20190804.yaml')
obs_events, obs_info = read_obs(basin, event_no)

pb_values = []
cc_values = []
rmse_values = []
nse_values = []
kge_values = []
for job_id in job_ids:

    result_name = f'./result/Zhongtangmei_Sen_20190804/{job_id}_Zhongtangmei_20190804.txt'
    sim = whf.Readfrxst_pts_out(result_name, station)
    sim = whf.ConvertTimeZone(sim, 'UTC', 'Asia/Shanghai')
    sim = sim[(sim['Date'] >= obs_info[event_no][0]) & (sim['Date'] <= obs_info[event_no][1])]
    sim = sim.rename(columns={f'Zhongtangmei_{job_id}_Zhongtangmei_20190804': f'Zhongtangmei_Sen_20190804_{job_id}'})

    pb = obj_fun.PBias(obs_events[event_no], sim)[f'Zhongtangmei_Sen_20190804_{job_id}']
    cc = obj_fun.CC(obs_events[event_no], sim)[f'Zhongtangmei_Sen_20190804_{job_id}']
    rmse = obj_fun.RMSE(obs_events[event_no], sim)[f'Zhongtangmei_Sen_20190804_{job_id}']
    nse = obj_fun.NSE(obs_events[event_no], sim)[f'Zhongtangmei_Sen_20190804_{job_id}']
    kge = obj_fun.KGE(obs_events[event_no], sim)[f'Zhongtangmei_Sen_20190804_{job_id}']
    
    pb_values.append(pb)
    cc_values.append(cc)
    rmse_values.append(rmse)
    nse_values.append(nse)
    kge_values.append(kge)

    # if kge >= 0.0:
    #     whf.DrawStreamFlow(obs_events[event_no], sim, f'AA_{round(kge,2)}_Zhongtangmei_Sen_20190804_{job_id}')
    # whf.DrawStreamFlow(obs_events[event_no], sim, f'{round(kge,2)}_Zhongtangmei_Sen_20190804_{job_id}')

obj_df = pd.DataFrame({'Job_id': job_ids,  'PBias': pb_values, 'CC': cc_values, 'RMSE': rmse_values, 'NSE': nse_values, 'KGE': kge_values})
obj_df.to_excel(f'./Zhongtangmei_20190804_all.xlsx', index=False)

path = r"F:\Haihe\Run\params_sen\sen\job_values.xlsx"
params_value = pd.read_excel(path, sheet_name='Sheet1')

merged_df = pd.merge(params_value, obj_df, on='Job_id', how='inner')
merged_df.to_excel(f'./sen/Zhongtangmei_{event_no}_sendate.xlsx', index=False)