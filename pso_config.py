# -*- encoding: utf-8 -*-
'''
@File    :   pso_config.py
@Create  :   2025-04-28 16:14:35
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import yaml
import numpy as np
from util.sample import central_problem, central_sample
from util.jobs import jobs2yaml
from core.ObjFun import CalObjFun
jobrun = 'test'
job_yaml_path = f'./work//PSO/{jobrun}/jobs/senNewcentral_Fuping_20130811.yaml'
result_dir = './work/PSO/test/result'
obsdir = 'F:/水文年鉴/'
save = f'./work/PSO/{jobrun}/Finial/'
param_obj_values = CalObjFun(result_dir, job_yaml_path, save_path=save+f'PSO_test.xlsx',
                                        obsdir=obsdir, draw_pic=True, return_params=True, correct=True)