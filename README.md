# WRF-Hydro Parameter Calibration Using PSO

This project applies **Particle Swarm Optimization (PSO)** to calibrate parameters of the WRF-Hydro hydrological model, aiming to improve simulation accuracy and hydrologic response.

## 📁 Directory Structure

```
.
├── core/               # Core modules including objective function, optimization process, etc.
│   ├── NSGA2.py
│   ├── ObjFun.py
│   ├── Optimize.py
│   ├── SenAna.py
│   ├── SurrModel.py
│   └── runner/         # Simulation runner and job scheduler
├── jobs/               # Generated simulation configuration files (.yaml)
├── models/             # WRF-Hydro model files
├── params/             # Parameter configuration files
│   ├── calib_params.tbl
│   ├── run_params.yaml
│   └── sens_params.tbl
├── pic/                # Output figures (e.g., sensitivity plots, optimization results)
├── util/               # Utility scripts
│   ├── jobs.py         # Job configuration tools
│   ├── sample.py       # Parameter sampling
│   ├── visual.py       # Visualization tools
├── run_pso.py          # Main PSO calibration script
├── runhydro.sh         # Shell script to launch the workflow
```

## 🚀 Getting Started

### 1. Environment Setup

Activate the Anaconda environment:

```bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate pso
```

Ensure the following dependencies are installed:

- `pyswarms`
- `SALib`
- `numpy`
- `pandas`
- `xarray`
- `logging`
- `seaborn`
- `pandas`
- `xesmf`                # creat precip forcing files
- `joblib`
- `yaml`
- Custom modules: `core`, `util`

### 2. Run the Calibration

#### Shell Script: `runhydro.sh`

```bash
#!/bin/bash

cp -r ../run_source ./run_source
source ~/anaconda3/etc/profile.d/conda.sh
conda activate pso
echo "The environment is activated and script is running."
nohup python3 run_pso.py > ./run_pso.log 2>&1 &
echo "Python script is running in the background. Check the log file for output."
ps aux | grep run_pso.py
```

This script performs:

- Copying source templates
- Activating `conda` environment
- Launching `run_pso.py` and saving logs
- Checking background process

### 3. PSO Calibration Logic (`run_pso.py`)

Workflow overview:

1. **Define calibration parameters** (e.g., `BEXP`, `DKSAT`, `MannN`, etc.)
2. **Generate initial samples**
3. **Run model simulations and manage jobs**
4. **Read results and calculate objective metrics (KGE + NSE)**
5. **Iteratively optimize via PSO**
6. **Save optimal parameters and objective value**

Results will be saved in:

- `pso_results.txt`: readable text format
- `pso_results.npz`: NumPy format for analysis

## ⚙️ Parameter Notes

- Parameter configuration located in `params/`
- `obsdir` specifies observed streamflow directory (e.g., `./Qobs`)
- `sim_info` sets WRF-Hydro working directory and meta-info
- Objective function used: `0.5 * KGE(-1) + 0.5 * NSE(-1)`

## 📞 Contact

Author: **shihx2003**  
Email: <shihx2003@outlook.com>  

## 📌 Notes

- This project relies on the PBS job scheduler and a complete configuration of the WRF-Hydro model.
- Recommended to run on HPC or server environment for performance.

## Documentation Acknowledgement
Parts of this README documentation were generated with the help of ChatGPT.