# -*- encoding: utf-8 -*-
'''
@File    :   params.py
@Create  :   2025-04-19 15:52:28
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import yaml

def read_params(path,params):
    params_info = {}
    params_ymal = yaml.safe_load(open(path, 'r', encoding='utf-8'))
    for param in params:
        if param in params_ymal.keys():
            params_info[param] = params_ymal[param]
        else:
            print(f"Parameter '{param}' not found in the YAML file.")
    
    return params_info