# -*- encoding: utf-8 -*-
'''
@File    :   collect_sen.py
@Create  :   2025-04-28 13:28:43
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
from util.sample import creat_problem
from core.ObjFun import CalObjFun
method = 'morris'
n_list = [2,4,8,16,32]
# n_list = [2,4,8,16]
events = ['Fuping_20120621', 'Fuping_20130628']
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
objfun_name = ['Bias', 'PBias', 'RMSE', 'CC', 'NSE', 'KGE']
problem_ini = creat_problem(params)
result_dir = f'./work/{method}_n/result/'
obsdir = 'F:/水文年鉴'
save = f'./work/{method}_n/Finial/'

for n in n_list:
    temp_save = []
    for event in events:
        job_yaml_path = f'./work/{method}_n/jobs/{method}_{n}_{event}_{event}.yaml'
        
        if event == 'Fuping_20120621' or event == 'Fuping_20120721' or event == 'Fuping_20130811':
            param_obj_values = CalObjFun(result_dir, job_yaml_path, save_path=save+f'{method}_{n}_{event}_{event}.xlsx',
                                        obsdir=obsdir, draw_pic=False, return_params=True, correct=True)
        else:
            param_obj_values = CalObjFun(result_dir, job_yaml_path, save_path=save+f'{method}_{n}_{event}_{event}.xlsx',
                                        obsdir=obsdir, draw_pic=False, return_params=True, correct=False)
        
        obj = param_obj_values[objfun_name]
        temp_save.append(obj)
    param_obj_values = param_obj_values[params]
    for obj in objfun_name:
        param_obj_values[obj] = (temp_save[0][obj] + temp_save[1][obj])/2
    param_values = param_obj_values[params].values
    obj_values = param_obj_values[objfun_name].values
    param_obj_values.to_excel(save+f'{method}_{n}_avg.xlsx', index=False)

