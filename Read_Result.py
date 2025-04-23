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
from core import ObjFun
import pandas as pd

def read_obs(basin, events):
    info = pd.read_excel(f"F:\\水文年鉴\\Haihe_Floods_Interp_1H\\{basin}_FloodEvents\\{basin}_Flood_Info.xlsx", sheet_name='Sheet1')
    obs_events = {}
    obs_info = {}
    if not isinstance(events, list):
        events = [events]

    for enent_no in events:
        enent_no = int(enent_no)
        flood_info = info[info['No'] == enent_no]
        start_time = flood_info.iloc[0]['start_date']
        end_time = flood_info.iloc[0]['end_date']
        obs = pd.read_excel(f"F:\\水文年鉴\\Haihe_Floods_Interp_1H\\{basin}_FloodEvents\\{basin}_{enent_no}.xlsx", sheet_name='Sheet1')
        obs = obs.rename(columns={'Q': 'obs'})
        obs['Date'] = pd.to_datetime(obs['Date'])
        
        obs_events[str(enent_no)] = obs
        obs_info[str(enent_no)] = [start_time, end_time]

    return obs_events, obs_info


station = {'1':'Fuping'}
basin = 'Fuping'
# event_no = '20190804'
event_no = ['20120621', '20120721', '20130811', '20160718', '20190804', '20200717', '20200801', '20200824']

obs_events, obs_info = read_obs(basin, event_no)
obs_values = obs_events[event_no]
start_time = obs_info[event_no][0]
end_time = obs_info[event_no][1]

print(obs_values)

jobs_params = pd.read_excel('job_info.xlsx', sheet_name='Sheet1')
job_ids = jobs_params['Job_id'].tolist()
job_kge = {}
for job_id in job_ids:
    result_name = f'./result./Sen_Fuping_20190804/{job_id}_{basin}_{event_no}.txt'

    sim = whf.Readfrxst_pts_out(result_name, station)
    sim = whf.ConvertTimeZone(sim, 'UTC', 'Asia/Shanghai')
    sim = sim[(sim['Date'] >= start_time) & (sim['Date'] <= end_time)]
    sim = sim.rename(columns={f'Fuping_{job_id}_Fuping_20190804': job_id})

    kge = ObjFun.KGE(obs_values, sim)
    #whf.DrawStreamFlow(obs_values, sim, f'{round(kge[job_id], 3)}_{job_id}')
    job_kge.update(kge)


job_nse_df = pd.DataFrame(list(job_kge.items()), columns=['Job_id', 'KGE'])

job_nse_df.to_excel('job_KGE.xlsx', index=False)
print(job_nse_df)