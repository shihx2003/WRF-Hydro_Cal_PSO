# -*- encoding: utf-8 -*-
'''
@File    :   WRFHydroJob.py
@Create  :   2025-03-29 15:58:42
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import libraries
import os
import re
import shutil
import yaml
import logging
import subprocess
from datetime import datetime
from util.runner.adjust_params import chan_param, nc_params

logger = logging.getLogger(__name__)

class SimulationInfo:
    """
    A class to manage simulation information and directories.
    
    Parameters
    ----------
    sim_info: dict
        Contains information about the simulation, including directories and parameters.
        
        'obj': str
        'ROOT_DIR': str
    """
    def __init__(self, sim_info:dict):
        """
        Initialize the SimulationInfo object with simulation information.
        """
        self.obj = sim_info['obj']
        self.ROOT_DIR = sim_info['ROOT_DIR']
        self.run_source_dir = os.path.join(self.ROOT_DIR, sim_info.get('run_source_dir','run_source'))
        self.run_dir = os.path.join(self.ROOT_DIR, sim_info.get('run_dir','run'))
        self.result_dir = os.path.join(self.ROOT_DIR, sim_info.get('result_dir','result'))
        self.config_dir = os.path.join(self.ROOT_DIR, sim_info.get('config_dir','configs'))
        self.params_yaml = os.path.join(self.ROOT_DIR, sim_info.get('params_yaml',''), 'params', 'run_params.yaml')

        with open(self.params_yaml, 'r', encoding='utf-8') as file:
            self.params_info = yaml.safe_load(file)
        logger.info(f"Parameters information loaded from {self.params_yaml}")

    def creat_work_dirs(self):
        """
        Check if required directories exist, create them if they don't.
        """
        dirs_to_check = [self.run_dir, self.result_dir, self.config_dir]
            
        for directory in dirs_to_check:
            if not os.path.exists(directory):
                logger.info(f"Directory {directory} does not exist. Creating...")
                try:
                    os.makedirs(directory)
                    logger.info(f"Created directory: {directory}")
                except Exception as e:
                    logger.error(f"Failed to create directory {directory}: {e}")
                    raise
            else:
                logger.debug(f"Directory exists: {directory}")

class ModelRunner:
    """
    A class to manage the WRF-Hydro model simulation.

    Parameters
    ----------
    sim_info: SimulationInfo
        An instance of the SimulationInfo class containing simulation information.
    job_info: dict
        Contains information about the simulation run, including job ID, period, event number, basin,  and parameters.
    config: str
        Path to a configuration file in YAML format.
    """

    def __init__(self, sim_info:SimulationInfo, job_info:dict=None, config:str=None):
        """
        """
        # Determine initialization source (sim_info dictionary or config file)
        if job_info is not None:
            # Initialize from sim_info dictionary
            self.job_id = job_info['job_id']
            self.period = job_info['period']
            self.event_no = str(job_info['event_no'])
            self.basin = job_info.get('basin', 'params_files')
    
            self.ROOT_DIR = sim_info.ROOT_DIR
            self.run_source_dir = sim_info.run_source_dir
            self.src_params_dir = os.path.join(self.run_source_dir, self.basin + '_params')
            self.run_dir = sim_info.run_dir
            self.result_dir = sim_info.result_dir
            self.config_dir = sim_info.config_dir

            self.src_run_dir = os.path.join(self.run_source_dir, self.event_no)
            
            self.params_info = sim_info.params_info
            self.set_params = job_info['set_params']

        elif config is not None:
            # Initialize from config file
            with open(config, 'r', encoding='utf-8') as file:
                config_self = yaml.safe_load(file)
            
            self.job_id = config_self['job_id']
            self.period = config_self['period']
            self.event_no = config_self['event_no']
            self.basin = config_self.get('basin', 'params_files')
            
            self.ROOT_DIR = config_self['ROOT_DIR']
            self.run_source_dir = config_self['run_source_dir']
            self.src_params_dir = config_self['src_params_dir']
            self.run_dir = config_self['run_dir']
            self.result_dir = config_self['result_dir']
            self.config_dir = config_self['config_dir']
            self.src_run_dir = config_self['src_run_dir']
            self.set_params = config_self['set_params']

        else:
            raise ValueError("Either sim_info or config must be provided")
            
        # Common initialization
        self.pbs_id = None
        self.job_dir = None
        self.job_status = None
        self.pbs_script = 'Hydrojob.pbs'
        self.wrfhydrofrxst = 'frxst_pts_out.txt'
    def save_config(self, namemark=''):
        """
        """
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        config_name = self.job_id  + '_' + self.event_no + namemark + '_config.yaml'
        config_file = os.path.join(self.config_dir, config_name)

        with open(config_file, 'w', encoding='utf-8') as file:
            # Create a dictionary with all relevant model parameters
            config_data = {
                
                'job_id': self.job_id,
                'period': self.period,
                'event_no': self.event_no,
                'basin': self.basin,
                
                'ROOT_DIR': self.ROOT_DIR,
                'run_source_dir': self.run_source_dir,
                'src_params_dir': self.src_params_dir,
                'run_dir': self.run_dir,
                'result_dir': self.result_dir,
                'config_dir': self.config_dir,
                'src_run_dir': self.src_run_dir,
                'set_params': self.set_params,

                'pbs_id': self.pbs_id,
                'pbs_exit_code': self.job_status,
                'config_yaml': config_file
            }
            
            # Dump the config data to YAML file
            yaml.dump(config_data, file, default_flow_style=False)
            logger.info(f"Job {self.job_id} configuration saved to {config_file}")
            
    def copy_folder(self):
        """
        """
        if not os.path.exists(self.src_run_dir):
            logger.error(f"src_run_dir {self.src_run_dir} does not exist.")
            self.save_config(namemark='copy_folder')
            raise FileNotFoundError(f"src_run_dir {self.src_run_dir} does not exist.")
        
        i = 0
        job_dir = os.path.join(self.run_dir, self.job_id)
        while os.path.exists(job_dir):
            logger.warning(f"desrin_dir {job_dir} already exists. Choose a new directory.")
            i += 1
            job_dir = os.path.join(self.run_dir, self.job_id) + f"_{i}"
            if i > 5:
                logger.error(f"Failed to create a new job directory after 5 attempts.")
                self.save_config(namemark='copy_folder')
                raise RuntimeError(f"Failed to create a new job directory after 5 attempts.")
            
        os.makedirs(job_dir)
        self.job_dir = job_dir
        logger.info(f"Copying {self.src_run_dir} to {self.job_dir} ...")

        try:
            shutil.copytree(self.src_run_dir, self.job_dir, dirs_exist_ok=True)
            logger.info(f"Copied {self.src_run_dir} to {self.job_dir}")
        except Exception as e:
            logger.error(f"Error copying folder: {e}")
            self.save_config(namemark='copy_folder')
            raise RuntimeError(f"Error copying folder: {e}")

    def inital_params(self, new_params=None):
        """
        NOTE : nc_files = ['Fulldom_hires.nc0', 'hydro2dtbl.nc0', 'soil_properties.nc0', 'GWBUCKPARM.nc0']
        """
        if new_params is not None:
            self.set_params.update(new_params)
            logger.info(f"Model parameters updated: {self.set_params}")

        if self.job_dir is None:
            logger.error("Job directory not set. Please run copy_folder() first.")
            self.save_config(namemark='inital_params')
            raise RuntimeError("Job directory not set. Please run copy_folder() first.")
        
         # set params
        set_nc_param = []
        set_chan_param = {}
        for key, value in self.set_params.items():
            if key == 'Bw' or key == 'HLINK' or key == 'ChSSlp' or key == 'MannN':
                set_chan_param[key] = value
            else:
                if key not in self.params_info:
                    logger.warning(f"Parameter {key} not found in params_info. Skipping.")
                    self.save_config(namemark='inital_params')
                    raise KeyError(f"Parameter {key} not found in params_info.")
                    
                param_info = self.params_info[key]

                if isinstance(param_info['name'], list) and isinstance(param_info['file'], list):
                    pam = {
                        'name': param_info['name'],
                        'file': param_info['file'],
                        'value': value,
                        'adjust': param_info['adjust']
                    }
                elif isinstance(param_info['name'], str) and isinstance(param_info['file'], str):
                    pam = {
                        'name': [param_info['name']],
                        'file': [param_info['file']],
                        'value': value,
                        'adjust': param_info['adjust']
                    }
                else:
                    logger.error(f"Parameter {key} has inconsistent types for name and file.")
                    self.save_config(namemark='inital_params')
                    raise TypeError(f"Parameter {key} has inconsistent types for name and file.")
                set_nc_param.append(pam)
        
        # adjust the params
        # src_params_files = os.path.join(self.run_source_dir, 'params_files')
        if not os.path.exists(self.src_params_dir):
            logger.error(f"Source parameters directory {self.src_params_dir} does not exist.")
            self.save_config(namemark='inital_params')
            raise FileNotFoundError(f"Source parameters directory {self.src_params_dir} does not exist.")
        
        if len(set_nc_param) == 0:
            logger.warning("No nc parameters to set. Run as default param.")
            # Copy the default parameter files
            nc_files = ['Fulldom_hires.nc0', 'hydro2dtbl.nc0', 'soil_properties.nc0', 'GWBUCKPARM.nc0']
            for nc_file in nc_files:
                nc_src_file = os.path.join(self.src_params_dir, nc_file)
                nc_dest_file = os.path.join(self.job_dir, 'DOMAIN', nc_file[:-1])
                if os.path.exists(nc_src_file):
                    shutil.copy(nc_src_file, nc_dest_file)
                    logger.info(f"Copied {nc_src_file} to {nc_dest_file} as default param.")
                    ec_nc = 1
                    logger.info(f'inital nc_params with exit code : {ec_nc}')
                else:
                    logger.error(f"Source file {nc_src_file} does not exist.")
                    self.save_config(namemark='inital_params')
                    raise FileNotFoundError(f"Source file {nc_src_file} does not exist.")
        else:
            ec_nc = nc_params(set_nc_param, self.src_params_dir, os.path.join(self.job_dir, 'DOMAIN'))
            logger.info(f'inital nc_params with exit code : {ec_nc}')

        # Copy the CHANPARM.TBL file
        if len(set_chan_param) == 0:
            logger.warning("No chan parameters to set. Run as default param.")
            chan_src_file = os.path.join(self.src_params_dir, 'CHANPARM.TBL.temp')
            chan_dest_file = os.path.join(self.job_dir, 'CHANPARM.TBL')
            if os.path.exists(chan_src_file):
                shutil.copy(chan_src_file, chan_dest_file)
                logger.info(f"Copied {chan_src_file} to {chan_dest_file} as default param.")
                ec_chan = 1
                logger.info(f'inital chan_params with exit code : {ec_chan}')
            else:
                logger.error(f"Source file {chan_src_file} does not exist.")
                self.save_config(namemark='inital_params')
                raise FileNotFoundError(f"Source file {chan_src_file} does not exist.")
        else:
            ec_chan = chan_param(set_chan_param, self.src_params_dir, self.job_dir)
            logger.info(f'inital chan_params with exit code : {ec_chan}')
        
        # Check if parameters were initialized successfully
        if ec_nc == 1 and ec_chan == 1:
            logger.info("All parameters initialized successfully.")
        else:
            logger.error("Error initializing parameters. with  ec_nc: {ec_nc} and ec_nc: {ec_chan}")
            self.save_config(namemark='inital_params')
            raise RuntimeError("Error initializing parameters.")
        
    def submit_pbs_job(self):
        """
        """
        os.chdir(self.job_dir)
        logger.info(f"Changed working directory to {self.job_dir}")
        pbs_script = os.path.join(self.job_dir, self.pbs_script)
        logger.info(f"Submitting PBS job with script: {pbs_script}")
        
        try:
            result = subprocess.run(['qsub', pbs_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                self.pbs_id = result.stdout.strip()
                logger.info(f"PBS job submitted successfully. Job ID: {self.job_id}. PBS ID: {self.pbs_id}")
            else:
                logger.error(f"Error submitting PBS job: {result.stderr.strip()}")
                self.save_config(namemark='submit_pbs_job')
                raise RuntimeError(f"Error submitting PBS job: {result.stderr.strip()}")
        except Exception as e:
            logger.error(f"Exception occurred while submitting PBS job: {e}")
            self.save_config(namemark='submit_pbs_job')
            raise RuntimeError(f"Exception occurred while submitting PBS job: {e}")
        finally:
            os.chdir(self.ROOT_DIR)
            logger.info(f"Changed back to ROOT_DIR: {self.ROOT_DIR}")

    def check_pbs_job_status(self):
        """
        """
        if self.pbs_id is None:
            logger.error("PBS job ID is not set. Please submit a job first.")
            self.job_status = "NOT_SUBMITTED"
            return

        try:
            result = subprocess.run(['qstat', self.pbs_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                output_lines = result.stdout.strip().split('\n')
                job_info = output_lines[2]
                status = job_info.split()[4]
                self.job_status = status
                logger.info(f"PBS job {self.pbs_id} status: {self.job_status}")
            else:
                self.job_status = "ERROR"
                logger.error(f"Error checking PBS job status: {result.stderr.strip()}")
        except Exception as e:
            self.job_status = "ERROR"
            logger.error(f"Exception occurred while checking PBS job status: {e}")
            self.save_config(namemark='check_pbs_job_status')
            raise RuntimeError(f"Exception occurred while checking PBS job status: {e}")

    def collect_frxst(self, result_dir=None, namemark=''):
        """
        """
        if self.job_id is None:
            logger.error("Job ID is not set. Please submit a job first.")
            return
        if self.job_status not in ["C", "E"]:
            logger.error(f"Job {self.job_id} is not completed or has not encountered an error. Current status: {self.job_status}")
            return
        if result_dir is not None:
            self.result_dir = result_dir
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
        logger.info(f"Collecting results from {self.job_dir} to {self.result_dir} ...")
        result_file = os.path.join(self.job_dir, self.wrfhydrofrxst)
        if not os.path.exists(result_file):
            logger.error(f"Result file {result_file} does not exist.")
            return
        try:
            shutil.copy(result_file, os.path.join(self.result_dir, self.job_id + '_' +self.event_no + namemark + '.txt'))
            logger.info(f"Result file {result_file} copied to {self.result_dir}")
        except Exception as e:
            logger.error(f"Error copying result file: {e}")
            self.save_config(namemark='collect_frxst')
            raise RuntimeError(f"Error copying result file: {e}")

    def run(self):
        """
        """
        self.copy_folder()
        self.inital_params()
        self.submit_pbs_job()

    def cleanup(self):
            """
            """
            if self.job_dir is not None:
                try:
                    pattern_LDASOUT = r"\d{4}\d{2}\d{2}\d{4}\.LDASOUT_DOMAIN3"  # 匹配 'YYYYMMDDHHMM.LDASOUT_DOMAIN3'
                    pattern_diag_hydro = r"diag_hydro\.\d{5}"  # 'diag_hydro.00001'
                    pattern_HYDRO_RST = r"HYDRO_RST\.\d{4}-\d{2}-\d{2}_\d{2}:\d{2}_DOMAIN3"  #'HYDRO_RST.2012-07-11_00:00_DOMAIN3'
                    pattern_RESTART = r"RESTART\.\d{8}\d{2}_DOMAIN3"  # 'RESTART.2012071700_DOMAIN3'

                    file_pattern = re.compile(
                        f"^({pattern_LDASOUT}|{pattern_diag_hydro}|{pattern_HYDRO_RST}|{pattern_RESTART})$"
                    )
                    for filename in os.listdir(self.job_dir):
                        file_path = os.path.join(self.job_dir, filename)
                        
                        if os.path.isfile(file_path) and file_pattern.match(filename):
                            os.remove(file_path)
                            logger.info(f"Removed file: {filename}")
                    if not os.listdir(self.job_dir):
                        shutil.rmtree(self.job_dir)
                        logger.info(f"Removed job directory: {self.job_dir}")

                except Exception as e:
                    logger.error(f"Error during cleaning: {e}")
                    self.save_config(namemark='clean')
                    raise RuntimeError(f"Error during cleaning: {e}")
            else:
                logger.warning("Job directory is not set. Nothing to clean.")

if __name__ == "__main__":
    sim_info = {
        'obj': 'example_obj',
        'ROOT_DIR': '/public/home/Shihuaixuan/Run/wrfhydro_runner_test/wrfhydro_runner-main',
    }

    job_info = {
        'job_id': 'test_10001',
        'period': {'start' : datetime(2020, 1, 1, 0), 'end' : datetime(2020, 1,2, 20)},
        'event_no': 'Fuping_20190804',
        'basin': 'Fuping',
        'set_params': {
            'SMCMAX': 1.0,
            'SLOPE': 0.06,
            'MannN': 0.9
        },
        'pbs_script': 'Hydrojob.pbs',
        'wrfhydrofrxst': 'frxst_pts_out.txt'
    }


    sim_info = SimulationInfo(sim_info)
    sim_info.creat_work_dirs()
    model_runner = ModelRunner(sim_info, job_info)
    model_runner.run()