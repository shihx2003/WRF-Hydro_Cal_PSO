# WRF-Hydro 参数率定 - PSO 方法

本项目使用 **粒子群优化（PSO）算法** 对 WRF-Hydro 水文模型参数进行率定，以提高模拟精度和水文响应表现。

## 📁 目录结构

```
.
├── core/               # 主要功能模块，如目标函数、优化流程等
│   ├── NSGA2.py
│   ├── ObjFun.py
│   ├── Optimize.py
│   ├── SenAna.py
│   ├── SurrModel.py
│   └── runner/         # 运行任务调度和模拟流程
├── jobs/               # 存储生成的模拟配置文件（.yaml）
├── models/             # 存储 WRF-Hydro 模型相关文件
├── params/             # 参数配置文件
│   ├── calib_params.tbl
│   ├── run_params.yaml
│   └── sens_params.tbl
├── pic/                # 图像输出（如敏感性分析、优化结果图）
├── util/               # 工具脚本
│   ├── jobs.py         # 任务配置转换
│   ├── sample.py       # 参数采样函数
│   ├── visual.py       # 可视化模块
├── run_pso.py          # PSO 主运行脚本
├── runhydro.sh         # 启动脚本（Shell）
```

## 🚀 快速开始

### 1. 环境准备

使用 Anaconda 激活运行环境：

```bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate pso
```

确保以下依赖已经安装：

- `pyswarms`
- `SALib`
- `numpy`
- `pandas`
- `xarray`
- 自定义模块：`core`, `util`

### 2. 运行脚本

#### Shell 脚本：`runhydro.sh`

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

该脚本完成以下操作：

- 拷贝运行模板
- 激活 `conda` 环境
- 启动 `run_pso.py` 任务并记录日志
- 显示后台运行状态

### 3. PSO 率定逻辑（`run_pso.py`）

主流程如下：

1. **定义待率定参数**（如 `BEXP`, `DKSAT`, `MannN` 等）
2. **生成初始样本点**
3. **运行模型并调度多个任务**
4. **读取模拟结果并计算目标函数（KGE + NSE）**
5. **通过 PSO 迭代优化参数**
6. **保存最优参数与目标函数值**

优化结果将保存在：

- `pso_results.txt`：文本记录
- `pso_results.npz`：用于后续分析的 NumPy 格式

## ⚙️ 参数说明

- `params/` 目录下包含参数表和配置脚本
- `obsdir` 指定观测流量数据目录（如 `./Qobs`）
- `sim_info` 中配置 WRF-Hydro 工作目录等信息
- 目标函数组合形式：`0.5 * KGE(-1) + 0.5 * NSE(-1)`

## 📞 联系方式

作者：**shihx2003**  
邮箱：<shihx2003@outlook.com>  

## 📌 注

- 本项目依赖PBS任务调度与 WRF-Hydro 模型的完整配置。
- 推荐在高性能计算平台或服务器中运行以提升效率。
