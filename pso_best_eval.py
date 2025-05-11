# -*- encoding: utf-8 -*-
'''
@File    :   pso_best_eval.py
@Create  :   2025-05-11 14:07:02
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import pandas as pd
import numpy as np

from core.ObjFun import FastCalObj

QP_path = "F:/Haihe/FinalPaperDate/PSO/best/Qsim_Qobs_Prec.xlsx"
events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824', ]

results = []

for event in events:
    basin = event.split('_')[0]
    eventno = event.split('_')[1]

    QPdate = pd.read_excel(QP_path, sheet_name=eventno)
    QPdate['Date'] = pd.to_datetime(QPdate['Date'])
    sim = QPdate[['Date','Qsim']].copy()
    sim = sim.rename(columns={'Qsim': eventno})
    obs = QPdate[['Date', 'Qobs']].copy()
    obs = obs.rename(columns={'Qobs': 'obs'})

    obj_fun = FastCalObj(obs, sim, eventno)
    results.append(obj_fun)

results_df = pd.DataFrame(results)
print(results_df)
results_df.to_excel("F:/Haihe/FinalPaperDate/PSO/best/PSO_eval.xlsx", index=False)