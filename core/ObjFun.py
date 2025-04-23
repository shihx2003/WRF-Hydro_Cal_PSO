# -*- encoding: utf-8 -*-
'''
@File    :   obj_fun.py
@Create  :   2025-04-19 13:51:11
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import numpy as np
import pandas as pd

def Bias(obs, sim):
    obs = obs.reset_index(drop=True)
    sim = sim.reset_index(drop=True)
    bias_values = {}
    for colums in sim.columns[1:]:
        bias_value = np.sum(sim[colums].values - obs['obs'].values) / len(obs['obs'])
        bias_values[colums] = bias_value

    return bias_values

def PBias(obs, sim):
    obs = obs.reset_index(drop=True)
    sim = sim.reset_index(drop=True)
    pbias_values = {}
    for colums in sim.columns[1:]:

        pbias_value = 100 * (np.sum(sim[colums].values - obs['obs'].values) / np.sum(obs['obs'].values))
        pbias_values[colums] = pbias_value
    
    return pbias_values

def RMSE(obs, sim):
    obs = obs.reset_index(drop=True)
    sim = sim.reset_index(drop=True)
    rmse_values = {}
    for colums in sim.columns[1:]:
        rmse_value = np.sqrt(np.sum((obs['obs'].values - sim[colums].values)**2) / len(obs['obs']))
        rmse_values[colums] = rmse_value
    return rmse_values

def CC(obs, sim):
    obs = obs.reset_index(drop=True)
    sim = sim.reset_index(drop=True)
    cc_values = {}
    for colums in sim.columns[1:]:
        cc_value = np.corrcoef(obs['obs'].values, sim[colums].values)[0, 1]
        cc_values[colums] = cc_value
    return cc_values

def NSE(obs, sim):
    obs = obs.reset_index(drop=True)
    sim = sim.reset_index(drop=True)
    nse_values = {}
    for colums in sim.columns[1:]:
        nse_value = 1 - (np.sum((obs['obs'].values - sim[colums].values)**2) / np.sum((obs['obs'].values - np.mean(obs['obs'].values))**2))
        nse_values[colums] = nse_value
    return nse_values

def KGE(obs, sim):
    obs = obs.reset_index(drop=True)
    sim = sim.reset_index(drop=True)
    kge_values = {}
    for colums in sim.columns[1:]:

        r = np.corrcoef(obs['obs'].values, sim[colums].values)[0, 1]
        alpha = np.std(sim[colums].values) / np.std(obs['obs'].values)
        beta = np.mean(sim[colums].values) / np.mean(obs['obs'].values)
        
        kge_value = 1 - np.sqrt((r-1)**2 + (alpha-1)**2 + (beta-1)**2)
        kge_values[colums] = kge_value
    return kge_values