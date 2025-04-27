# -*- encoding: utf-8 -*-
'''
@File    :   Sen_Fuping.py
@Create  :   2025-04-18 23:52:17
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import yaml
import logging
import numpy as np
import pyswarms as ps
from core.runner import SimulationInfo, batch_instantiate, schedule_and_track_jobs

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('main.log')]
)
logger = logging.getLogger(__name__)

sim_info = {
    'obj': 'Sen_Fuping',
    'ROOT_DIR': '/public/home/Shihuaixuan/Run/Haihe_Run/senNewcentral_Fuping',
}
global_info = SimulationInfo(sim_info)
global_info.creat_work_dirs()

yaml_path = os.path.join(sim_info['ROOT_DIR'], 'jobs', f'senNewcentral_XXXX.yaml')
with open(yaml_path, 'r') as f:
    loaded_jobs = yaml.load(f, Loader=yaml.FullLoader)
set_jobs = batch_instantiate(global_info, jobs=loaded_jobs, configs=None)
schedule_and_track_jobs(set_jobs, max_num=5)


import numpy as np
import pyswarms as ps

model_call_count = 0

def objective_function(x):
    global model_call_count
    model_call_count += x.shape[0]
    print(f"模型计算次数: {model_call_count}")
    print(f"当前粒子位置: {x.shape}")

    A = 10
    n_dimensions = x.shape[1]
    print(x)
    return A * n_dimensions + np.sum(x**2 - A * np.cos(2 * np.pi * x), axis=1)

optimizer = ps.single.GlobalBestPSO(
    n_particles=10,
    dimensions=20,
    options={
        'c1': 2.0,
        'c2': 2.0,
        'w': 0.7298,
    },
    bounds=(-1 * np.ones(20), 1 * np.ones(20)),
    ftol=0.001,
    ftol_iter=5,
)


cost, pos = optimizer.optimize(objective_function, iters=50)