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
import logging
from SALib import ProblemSpec
import numpy as np
import pyswarms as ps

from core.ObjFun import Bias, CalObjFun
from util.jobs import jobs2yaml
from core.runner import SimulationInfo, batch_instantiate, schedule_and_track_jobs
from util.sample import creat_problem, central_sample

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('main.log')]
)
logger = logging.getLogger(__name__)


########################################################################################


# central_point_2 = {
#         'BEXP': 1.784630061,# 1.743162898
#         'SMCMAX': 0.825325479, # 0.856252672
#         'SLOPE': 0.421888441, # 0.302460859
#         'DKSAT': 4.009223693, # 3.734114511
#         'REFKDT': 1.34958373, # 2.427428199
#     }
											
central_point = {
        'BEXP': 1.857353169,
        'SMCMAX': 0.848071996,
        'SLOPE': 0.36779211,
        'DKSAT': 5.765174227,
        'REFKDT': 1.56732966,
        'ChSSlp': 3.244338311,
        'MannN': 0.9518489,
        'OVROUGHRTFAC': 0.219936395, 
    }

fix_params = {

    }

# params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT']
# params = ['ChSSlp', 'MannN', 'OVROUGHRTFAC', 'RETDEPRTFAC', 'LKSATFAC', 'NEXP', 'RSURFEXP']
params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT', 'ChSSlp', 'MannN', 'OVROUGHRTFAC']

obsdir = '/public/home/Shihuaixuan/Data/Qobs'
iters_count = 0
n_particles = 20
n_iterations = 50
inin_pramas = central_sample(params, central_point, n_particles, 0.1, return_problem=False)
problem = creat_problem(params)
central_bounds = [[bouns[0] for bouns in problem['bounds']],[bouns[1] for bouns in problem['bounds']]]

sim_info = {
    'obj': 'Sen_Fuping',
    'ROOT_DIR': '/public/home/Shihuaixuan/Run/Haihe_Run/PSO_Run',
}
global_info = SimulationInfo(sim_info)
global_info.creat_work_dirs()

def run_model(x):
    global iters_count
    iters_count += 1
    # jobs = jobs2yaml(params, x, eventname='Fuping_20120621', jobname=f'PSO_{iters_count}', fixed_parmas=fix_params)
    jobs = jobs2yaml(params, x, eventname='Fuping_20120621', jobname=f'PSO_{iters_count}')
    set_jobs = batch_instantiate(global_info, jobs=jobs, configs=None)
    schedule_and_track_jobs(set_jobs, max_num=5)
    jobymal = os.path.join(sim_info['ROOT_DIR'], 'jobs', f'PSO_{iters_count}_Fuping_20120621.yaml')
    resultdir = os.path.join(sim_info['ROOT_DIR'], 'result')
    obj_values = CalObjFun(resultdir, jobymal, obsdir=obsdir)  #df

    Bias = obj_values['Bias'].values
    PBias = obj_values['PBias'].values
    RMSE = obj_values['RMSE'].values
    CC = obj_values['CC'].values
    NSE = obj_values['NSE'].values
    KGE = obj_values['KGE'].values

    # obj = 0.5 * KGE *(-1) + 0.5 * abs(PBias / 100)
    obj = 0.5 * KGE *(-1) + 0.5 * NSE *(-1)
    logger.info(f"Iteration {iters_count}: Objective value: {obj}, Parameters: {x}")
    return obj

optimizer = ps.single.GlobalBestPSO(
    n_particles=n_particles,
    dimensions=len(params),
    options={
        'c1': 2.0,
        'c2': 2.0,
        'w': 0.7298,
    },
    bounds=central_bounds,
    ftol=0.0002,
    ftol_iter=10,
    init_pos = inin_pramas
)

cost, pos = optimizer.optimize(run_model, iters=n_iterations)

# Save optimization results
result_file = os.path.join(sim_info['ROOT_DIR'], 'pso_results.txt')
with open(result_file, 'w') as f:
    f.write(f"Best cost (objective value): {cost}\n")
    f.write("Best parameters:\n")
    for i, param in enumerate(params):
        f.write(f"{param}: {pos[i]}\n")

# Also save as numpy array for potential further analysis
np.savez(os.path.join(sim_info['ROOT_DIR'], 'pso_results.npz'),
         cost=cost,
         best_position=pos,
         param_names=np.array(params))

logger.info(f"Optimization completed. Best cost: {cost}")
logger.info(f"Best parameters: {dict(zip(params, pos))}")