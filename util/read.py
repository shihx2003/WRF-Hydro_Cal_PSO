# -*- encoding: utf-8 -*-
'''
@File    :   read.py
@Create  :   2025-04-22 13:21:47
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import yaml
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

def read_params(path, params):
    params_info = {}
    params_ymal = yaml.safe_load(open(path, 'r', encoding='utf-8'))
    for param in params:
        if param in params_ymal.keys():
            params_info[param] = params_ymal[param]
        else:
            print(f"Parameter '{param}' not found in the YAML file.")
    
    return params_info

def read_jobs(path):
    jobs_yaml = yaml.safe_load(open(path, 'r', encoding='utf-8'))
    jobs_id = list(jobs_yaml.keys())

    return jobs_id, jobs_yaml
