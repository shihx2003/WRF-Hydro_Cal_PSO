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
import util.wrfhydrofrxst as whf
from util.correct import correct_sim

def read_obs(basin, events, obsdir='/public/home/Shihuaixuan/Data/Qobs',**kwargs):
    """
    Read observation data from Excel files.

    Parameters
    -----------
    basin : str
        The name of the basin (e.g., 'Fuping').
    events : str or list of str
        The event number(s) to read (e.g., '20190804' or ['20190804', '20190805']).
    obsdir : str, optional
        The directory where the observation files are located. Default is '/public/home/Shihuaixuan/Data/Qobs'.
    **kwargs : keyword arguments
        Additional arguments to pass to the function.
        - sheetname : str, optional
            The name of the sheet in the Excel file to read. Default is 'Sheet1'.
    
    Returns
    --------
    obs_events : dict
        A dictionary containing the observation data for each event.
    obs_info : dict
        A dictionary containing the start and end times for each event.
    """
    sheetname = kwargs.get('sheetname', 'Sheet1')
    info = pd.read_excel(f"{obsdir}/Haihe_Floods_Interp_1H/{basin}_FloodEvents/{basin}_Flood_Info.xlsx", sheet_name=sheetname)
    obs_events = {}
    obs_info = {}
    if not isinstance(events, list):
        events = [events]

    for enent_no in events:
        enent_no = int(enent_no)
        flood_info = info[info['No'] == enent_no]
        start_time = flood_info.iloc[0]['start_date']
        end_time = flood_info.iloc[0]['end_date']
        obs = pd.read_excel(f"{obsdir}/Haihe_Floods_Interp_1H/{basin}_FloodEvents/{basin}_{enent_no}.xlsx", sheet_name='Sheet1')
        obs = obs.rename(columns={'Q': 'obs'})
        obs['Date'] = pd.to_datetime(obs['Date'])
        
        obs_events[str(enent_no)] = obs
        obs_info[str(enent_no)] = [start_time, end_time]

    return obs_events, obs_info

def read_params_info(path, params):
    params_info = {}
    params_ymal = yaml.safe_load(open(path, 'r', encoding='utf-8'))
    for param in params:
        if param in params_ymal.keys():
            params_info[param] = params_ymal[param]
        else:
            print(f"Parameter '{param}' not found in the YAML file.")
    
    return params_info

def read_jobs_yaml(path):
    jobs_yaml = yaml.safe_load(open(path, 'r', encoding='utf-8'))
    jobs_id = list(jobs_yaml.keys())

    return jobs_id, jobs_yaml


def read_jobs_frxst(dir, jobsyaml_path, **kwargs):

    return_obs = kwargs.get('return_obs', False)
    draw_pic = kwargs.get('draw_pic', False)
    obsdir = kwargs.get('obsdir', '/public/home/Shihuaixuan/Data/Qobs')
    correct = kwargs.get('correct', False)

    job_ids, jobs_yaml = read_jobs_yaml(jobsyaml_path)
    eventname = jobs_yaml.get(job_ids[0]).get('event_no')
    basin, no = eventname.split('_')[0], eventname.split('_')[1]

    obs_events, obs_info = read_obs(basin, no, obsdir=obsdir)

    jobs_frxst = {}
    for job_id in job_ids:
        
        frxst_name = f'{job_id}_{basin}_{no}'
        sim = whf.Readfrxst_pts_out(os.path.join(dir, f'{frxst_name}.txt'), station = {'1': basin})
        if correct:
            sim = correct_sim(sim, f'{basin}_{no}')
        else:
            sim = whf.ConvertTimeZone(sim, 'UTC', 'Asia/Shanghai')
        # sim = whf.ConvertTimeZone(sim, 'Asia/Shanghai', 'UTC')
        sim = sim[(sim['Date'] >= obs_info[no][0]) & (sim['Date'] <= obs_info[no][1])]

        sim = sim.rename(columns={f'{basin}_{frxst_name}': job_id})
        jobs_frxst[job_id] = sim

        if draw_pic:
            whf.DrawStreamFlow(obs_events[no], sim, f'{job_id}_{basin}_{no}')

    if return_obs:
        return jobs_frxst, obs_events[no], obs_info[no]
    else:
        return jobs_frxst




if __name__ == '__main__':
    # Example usage
    jobs_frxst = read_jobs_frxst('F:/Haihe/Run/params_sen/result/Fuping_Sen_20190804', 'F:/Haihe/Run/params_sen/jobs/sen_jobs_Fuping_20190804.yaml')
    print(jobs_frxst)