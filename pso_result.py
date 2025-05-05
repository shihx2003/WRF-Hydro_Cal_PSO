# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Create  :   2025-04-27 22:01:12
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import numpy as np
import yaml
import pandas as pd
from core.ObjFun import CalObjFun
import gc



# event = 'Fuping_20120721'       # Fuping_20120621， Fuping_20120721 , Fuping_20130811

events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824', ]
njobs = [24, 25, 27, 
         26, 17, 14, 
         29, 14, 11]

# events = ['Fuping_20190804']    re
# njobs = [12]
for i in range(len(events)):
    event = events[i]
    njob = njobs[i]
    jobrun = f'PSO_c_{event}'
    obsdir = 'F:/水文年鉴/'
    result_dir = f'./work/PSO/{jobrun}/result'
    save = f'./work/PSO/{jobrun}/Finial/'
    result = []
    for n in range(1, njob+1):
        job_yaml_path = f'./work//PSO/{jobrun}/jobs/PSO_{n}_{event}.yaml'
        if event == 'Fuping_20120621' or event == 'Fuping_20120721' or event == 'Fuping_20130811':
            print('correct')
            param_obj_values = CalObjFun(result_dir, job_yaml_path, save_path=save+f'PSO_correct_{n}.xlsx',
                                                obsdir=obsdir, draw_pic=False, return_params=True, correct=True)
        else:
            param_obj_values = CalObjFun(result_dir, job_yaml_path, save_path=save+f'PSO_{n}.xlsx',
                                                obsdir=obsdir, draw_pic=False, return_params=True, correct=False)
        Bias = param_obj_values['Bias'].values
        NSE = param_obj_values['NSE'].values
        RMSE = param_obj_values['RMSE'].values
        CC = param_obj_values['CC'].values
        NSE = param_obj_values['NSE'].values
        KGE = param_obj_values['KGE'].values
        # param_obj_values['obj'] = 0.5 * (param_obj_values['KGE'] * (-1)) +  0.5 * (param_obj_values['NSE'] / 100).abs()
        param_obj_values['obj'] = 0.5 * (param_obj_values['KGE'] * (-1)) +  0.5 * (param_obj_values['NSE'] * (-1))  

        result.append(param_obj_values)

    result = pd.concat(result, axis=0)
    result.to_excel(f'./work/PSO/{jobrun}/PSO_{event}.xlsx', index=False)

    # Release memory
    del result
    del param_obj_values
    gc.collect()
    print(f"Finished processing {event} and released memory")