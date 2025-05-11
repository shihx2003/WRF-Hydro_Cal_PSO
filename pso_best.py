# -*- encoding: utf-8 -*-
'''
@File    :   PSObest.py
@Create  :   2025-05-10 21:39:07
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from util.read import read_obs
import util.wrfhydrofrxst as whf
from util.correct import correct_sim
# from util.spec_precip import PrecipDataLoader

station = {'1':'Fuping'}
pso_best = "F:/Haihe/FinalPaperDate/PSO/best/PSO_cal_best.xlsx"
obsdir = "F:/水文年鉴"
info_df = pd.read_excel(pso_best, sheet_name='Sheet1')

simobs_dic = {}
for _, row in info_df.iterrows():
    job_id = row['job_id']
    event = row['event']
    basin = event.split('_')[0]
    eventno = event.split('_')[1]
    obsvalue, obsinfo = read_obs(basin, eventno, obsdir)
    obs = obsvalue[eventno]
    start_time = obsinfo[eventno][0]
    end_time = obsinfo[eventno][1]
    
    
    result_file = f'./work/PSO/PSO_All/originfiles/{job_id}_{event}.txt'
    sim = whf.Readfrxst_pts_out(result_file, station)
    sim = sim.rename(columns={f'Fuping_{job_id}_{event}': event[7:]})

    if event == 'Fuping_20120621' or event == 'Fuping_20120721' or event == 'Fuping_20130811':
        sim = correct_sim(sim, event)
    else:
        sim = whf.ConvertTimeZone(sim)
    sim = sim[(sim['Date'] >= start_time) & (sim['Date'] <= end_time)]
    merged_df = pd.merge(sim, obs, on='Date', how='inner')
    simobs_dic[eventno] = merged_df

with pd.ExcelWriter('F:/Haihe/FinalPaperDate/PSO/best/PSOresult.xlsx', engine='openpyxl') as writer:
    for no, df in simobs_dic.items():
        df.to_excel(writer, sheet_name=no, index=False)
