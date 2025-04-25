# -*- encoding: utf-8 -*-
'''
@File    :   div_Fuping_20160718.py
@Create  :   2025-04-26 00:18:03
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''
import numpy as np
import pandas as pd 

from util.read import read_jobs_yaml
import os
import shutil

def cp_Fuping_20160718(jobs_yaml_path, resut_dir):
    """
    jobs_yaml_path = f'./jobs/sen2central_Fuping_20160718.yaml'
    resut_dir = f'./result/Fuping_central_sample'
    """

    jobs_ids, _ = read_jobs_yaml(jobs_yaml_path)
    for i in range(len(jobs_ids)):
        origin_name = f'{jobs_ids[i]}_Fuping_20160718.txt'
        new_name = origin_name.replace('20160718', '20160724')
        original_path = f'./{resut_dir}/{origin_name}'
        new_path = f'./{resut_dir}/{new_name}'
            
        if os.path.exists(original_path):
            try:
                shutil.copy(original_path, new_path)
                print(f"Copied {origin_name} to {new_name}")
            except Exception as e:
                print(f"Error copying {origin_name}: {e}")
        else:
            print(f"File not found: {original_path}")

