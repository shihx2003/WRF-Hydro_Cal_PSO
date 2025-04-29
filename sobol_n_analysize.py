# -*- encoding: utf-8 -*-
'''
@File    :   sobol_n_analysize.py
@Create  :   2025-04-28 13:28:43
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from SALib.analyze import sobol
from SALib.analyze import morris

from util.sample import creat_problem
from util.visual import Draw_sobol_S1_ST, Draw_sobol_S2, Draw_morris_mu, Draw_morris_mu_star,  Draw_morris_sigma
from util.read import read_jobs_frxst
from core.ObjFun import CalObjFun
from util.jobs import jobs2xlsx

n_list = [2,4,8,16]
events = ['Fuping_20120621', 'Fuping_20130628']
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
objfun_name = ['Bias', 'PBias', 'RMSE', 'CC', 'NSE', 'KGE']
problem_ini = creat_problem(params)
result_dir = './work/result/sobol_n'
obsdir = 'F:/水文年鉴'
save = './work/sobol_n/'

for n in n_list:
    temp_save = []
    for event in events:
        job_yaml_path = f'./jobs/Finished/sobol_{n}_{event}_{event}.yaml'
        param_obj_values = CalObjFun(result_dir, job_yaml_path, save_path=save+f'sobol_{n}_{event}_{event}.xlsx',
                                      obsdir=obsdir, draw_pic=False, return_params=True)
        
        obj = param_obj_values[objfun_name]
        temp_save.append(obj)
    param_obj_values = param_obj_values[params]
    for obj in objfun_name:
        param_obj_values[obj] = (temp_save[0][obj] + temp_save[1][obj])/2
    param_values = param_obj_values[params].values
    obj_values = param_obj_values[objfun_name].values
    for obj in objfun_name:
        print(f'objfun: {obj}')
        obj_values = param_obj_values[obj].values
        problem = problem_ini.copy()
        # Si = sobol.analyze(problem, obj_values, calc_second_order=True, print_to_console=False)
        # Draw_sobol_S1_ST(problem, Si, filename=f'sobol_{n}_avg_{obj}_S1')
        # Draw_sobol_S2(problem, Si, filename=f'sobol_{n}_avg_{obj}_S2')

        mu = morris.analyze(problem, param_values, obj_values, print_to_console=False)
        Draw_morris_mu(problem, mu, filename=f'morris_{n}_avg_{obj}_mu', abs_mu=True)
        Draw_morris_mu_star(problem, mu, filename=f'morris_{n}_avg_{obj}_mu_star')
        Draw_morris_sigma(problem, mu, filename=f'morris_{n}_avg_{obj}_sigma')
    # param_obj_values.to_excel(save+f'sobol_{n}_{event}_avg.xlsx', index=False)


        # param_values = param_obj_values[params].values
        # obj_values = param_obj_values[objfun_name].values
        # for obj in objfun_name:
        #     print(f'objfun: {obj}')
        #     obj_values = param_obj_values[obj].values
        #     problem = problem_ini.copy()
        #     Si = sobol.analyze(problem, obj_values, calc_second_order=True, print_to_console=False)
        #     Draw_sobol_S1_ST(problem, Si, filename=f'sobol_{n}_{event}_{event}_{obj}_S1.png')
        #     Draw_sobol_S2(problem, Si, filename=f'sobol_{n}_{event}_{event}_{obj}_S2.png')

        #     mu = morris.analyze(problem, param_values, obj_values, print_to_console=False)
        #     Draw_morris_mu(problem, mu, filename=f'morris_{n}_{event}_{event}_{obj}_mu.png')
        #     Draw_morris_mu_star(problem, mu, filename=f'morris_{n}_{event}_{event}_{obj}_mu_star')
        #     Draw_morris_sigma(problem, mu, filename=f'morris_{n}_{event}_{event}_{obj}_sigma')

