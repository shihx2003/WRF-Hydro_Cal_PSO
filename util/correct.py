# -*- encoding: utf-8 -*-
'''
@File    :   correct.py
@Create  :   2025-04-29 20:03:05
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import pandas as pd
from util.wrfhydrofrxst import ConvertTimeZone
def correct_sim(sim, eventname):
    sim = sim.copy()
    if eventname == 'Fuping_20120621':
        sim['Date'] = sim['Date'] - pd.Timedelta(hours=16)

    elif eventname == 'Fuping_20120721':
        sim['Date'] = sim['Date'] - pd.Timedelta(hours=8)

    elif eventname == 'Fuping_20130811':
        sim['Date'] = sim['Date'] + pd.Timedelta(hours=19)

    else:
        raise ValueError(f"Event name '{eventname}' is not recognized for time zone conversion.")
    
    return sim
