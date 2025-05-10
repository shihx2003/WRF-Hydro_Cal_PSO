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
from core.runner import SimulationInfo, batch_instantiate, schedule_and_track_jobs

log_dir = './logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'mian.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

sim_info = {
    'obj': 'PSO_Run_Best_re',
    'ROOT_DIR': '/public/home/Shihuaixuan/Run/Haihe_Run/PSO_Run_Best_re',
}
global_info = SimulationInfo(sim_info)
global_info.creat_work_dirs()

events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824']
for event in events:
    yaml_path = os.path.join(sim_info['ROOT_DIR'], 'jobs', f'PSO_best_re_{event}_{event}.yaml')
    with open(yaml_path, 'r') as f:
        loaded_jobs = yaml.load(f, Loader=yaml.FullLoader)
    set_jobs = batch_instantiate(global_info, jobs=loaded_jobs, configs=None)
    schedule_and_track_jobs(set_jobs, max_num=6)

