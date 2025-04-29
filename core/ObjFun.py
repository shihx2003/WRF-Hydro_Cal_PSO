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
import re
import sys
import numpy as np
import pandas as pd
from util.read import read_jobs_frxst, read_params_info
from util.jobs import jobs2xlsx

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


def CalObjFun(dir, jobsyaml_path, save_path=None, **kwargs):
    """
    Calculate the objective function values for the given simulation results.

    Parameters
    ----------
    dir : str
        The directory where the simulation results are stored.
    jobsyaml_path : str
        The path to the YAML file containing job information.
    save_path : str, optional
        The path to save the results. If None, the results will not be saved.
    **kwargs : keyword arguments
        Additional parameters for the function:
        - draw_pic : bool, optional
            If True, draw pictures of the simulation results. Default is False.
        - obsdir : str, optional
            The directory where the observed data is stored. Default is '/public/home/Shihuaixuan/Data/Qobs'.
        - return_params : bool, optional
            If True, return the parameters along with the objective function values. Default is False.

    Returns
    ----------
    return_fun : pd.DataFrame
        A DataFrame containing the objective function values for each job ID. If return_params is True, it will also include the parameters.
    """

    # draw_pic = kwargs.get('draw_pic', False)
    obsdir = kwargs.get('obsdir', '/public/home/Shihuaixuan/Data/Qobs')
    return_params = kwargs.get('return_params', False)

    jobs_frxst, obs, obs_info = read_jobs_frxst(dir, jobsyaml_path, return_obs=True, **kwargs)
    job_ids = list(jobs_frxst.keys())

    bias_values = []
    pb_values = []
    cc_values = []
    rmse_values = []
    nse_values = []
    kge_values = []

    for job_id in job_ids:
        sim = jobs_frxst[job_id]

        bias = Bias(obs, sim)[f'{job_id}']
        pb = PBias(obs, sim)[f'{job_id}']
        cc = CC(obs, sim)[f'{job_id}']
        rmse = RMSE(obs, sim)[f'{job_id}']
        nse = NSE(obs, sim)[f'{job_id}']
        kge = KGE(obs, sim)[f'{job_id}']
        
        bias_values.append(bias)
        pb_values.append(pb)
        cc_values.append(cc)
        rmse_values.append(rmse)
        nse_values.append(nse)
        kge_values.append(kge)

    obj_values = pd.DataFrame({'job_id': job_ids, 'Bias': bias_values,  'PBias': pb_values,
                                'CC': cc_values, 'RMSE': rmse_values, 'NSE': nse_values, 'KGE': kge_values})

    if return_params:
        params_values = jobs2xlsx(jobsyaml_path)
        params_and_obj_values = pd.concat([params_values, obj_values], axis=1)
        return_fun = params_and_obj_values.copy()
    else:
        return_fun = obj_values.copy()
    
    if save_path is not None:
        return_fun.to_excel(save_path, index=False)
    
    return return_fun

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

if __name__ == '__main__':
    jobyaml = './jobs/surr_PBias_Fuping_20120721.yaml'
    frxst_dir = './result/Fuping_surr_PBias'

    params_values = jobs2xlsx(jobyaml)
    obj_values = CalObjFun(frxst_dir, jobyaml)
    params = params_values.columns[1:].tolist()
    target = params_values[(params_values['Job_id'] == 'surr_PBias_Fuping_20120721_114')].to_dict(orient='records')[0]

    Distance = CalDistance(params, target, params_values)
    obj_values['Distance'] = Distance['Norm_Distance']
    obj_values[params] = params_values[params]
    obj_values.to_excel('./surr/Fuping_PBias_20120721D.xlsx', index=False)