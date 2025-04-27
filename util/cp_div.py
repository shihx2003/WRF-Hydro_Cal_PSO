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

def cp_frxst(jobs_yaml_path, eventname, source, trarget, resut_dir):
    """
    jobs_yaml_path = f'./jobs/sen2central_Fuping_20160718.yaml'
    resut_dir = f'./result/Fuping_central_sample'
    """

    jobs_ids, _ = read_jobs_yaml(jobs_yaml_path)
    for i in range(len(jobs_ids)):
        origin_name = f'{jobs_ids[i]}_{eventname}.txt'
        new_name = origin_name.replace(source, trarget)
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


def cp_yaml(jobs_yaml_path, source, trarget, resut_dir='./jobs'):
    """
    jobs_yaml_path = f'./jobs/sen2central_Fuping_20160718.yaml'
    resut_dir = f'./result/Fuping_central_sample'
    """
    # Parse the original file name
    original_yaml_name = os.path.basename(jobs_yaml_path)

    new_yaml_name = original_yaml_name.replace(source, trarget)
    new_yaml_path = os.path.join(resut_dir, new_yaml_name)
    with open(jobs_yaml_path, 'r') as file:
        content = file.read()
    modified_content = content.replace(source, trarget)
    with open(new_yaml_path, 'w') as file:
        file.write(modified_content)
    
    print(f"Created modified YAML file: {new_yaml_path}")

