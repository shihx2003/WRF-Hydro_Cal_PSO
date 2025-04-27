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
    'obj': 'Sen_Fuping',
    'ROOT_DIR': '/public/home/Shihuaixuan/Run/Haihe_Run/senNewcentral_Fuping',
}
global_info = SimulationInfo(sim_info)
global_info.creat_work_dirs()

cal_events = ['test', 
              'Fuping_20110815', 'Fuping_20110824', 'Fuping_20120621', 'Fuping_20120721', 
              'Fuping_20130628', 'Fuping_20130811', 'Fuping_20160718', 'Fuping_20170720', 
              'Fuping_20171007']
for event in cal_events:
    yaml_path = os.path.join(sim_info['ROOT_DIR'], 'jobs', f'senNewcentral_{event}.yaml')
    with open(yaml_path, 'r') as f:
        loaded_jobs = yaml.load(f, Loader=yaml.FullLoader)
    set_jobs = batch_instantiate(global_info, jobs=loaded_jobs, configs=None)
    schedule_and_track_jobs(set_jobs, max_num=5)
