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
import sys
import numpy as np
import pandas as pd
from util.read import read_jobs_frxst, read_params_info

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


def CalObjFun(dir, jobsyaml_path, file_path=None, **kwargs):
    draw_pic = kwargs.get('draw_pic', False)
    jobs_frxst, obs, obs_info = read_jobs_frxst(dir, jobsyaml_path, return_obs=True, draw_pic=draw_pic)
    job_ids = list(jobs_frxst.keys())

    pb_values = []
    cc_values = []
    rmse_values = []
    nse_values = []
    kge_values = []

    for job_id in job_ids:
        sim = jobs_frxst[job_id]

        pb = PBias(obs, sim)[f'{job_id}']
        cc = CC(obs, sim)[f'{job_id}']
        rmse = RMSE(obs, sim)[f'{job_id}']
        nse = NSE(obs, sim)[f'{job_id}']
        kge = KGE(obs, sim)[f'{job_id}']
        
        pb_values.append(pb)
        cc_values.append(cc)
        rmse_values.append(rmse)
        nse_values.append(nse)
        kge_values.append(kge)

    obj_values = pd.DataFrame({'job_id': job_ids,  'PBias': pb_values, 'CC': cc_values, 'RMSE': rmse_values, 'NSE': nse_values, 'KGE': kge_values})
    if file_path is not None:
        obj_values.to_excel(file_path, index=False)

    return obj_values

def MaxMinNorm(data, min_value, max_value):
    """
    """
    norm_data = (data - min_value) / (max_value - min_value)
    return norm_data

def CalDistance(params, target, points, **kwargs):
    params_yaml_path = kwargs.get('yaml_path', './params/run_params.yaml')
    return_Norm = kwargs.get('return_Norm', False)
    params_info = read_params_info(params_yaml_path, params)

    target_Norm = {}
    points_Norm = pd.DataFrame()
    points_Norm['job_id'] = points['job_id']
    for param in params:
        minValue = params_info[param]['minValue']
        maxValue = params_info[param]['maxValue']
        target_Norm[param] = MaxMinNorm(target[param], minValue, maxValue)
        points_Norm[param] = MaxMinNorm(points[param], minValue, maxValue)

    target_Norm = np.array(list(target_Norm.values()))
    points_values = points_Norm[params].values
    norm_distance = np.sqrt(np.sum((points_values - target_Norm)**2, axis=1))
    points_Norm['Norm_Distance'] = norm_distance
    if return_Norm:
        return points_Norm
    else:
        points_Norm = points_Norm.drop(columns=params)
        return points_Norm

