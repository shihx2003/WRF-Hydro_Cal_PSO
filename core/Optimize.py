# -*- encoding: utf-8 -*-
'''
@File    :   Optimize.py
@Create  :   2025-04-27 16:30:03
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pyswarms as ps

model_call_count = 0

import numpy as np
import pyswarms as ps

import time
# 全局最优解应该在原点(0,0,...,0)，最优值为0
def objective_function(x):
    global model_call_count
    model_call_count += x.shape[0]
    
    # Rastrigin 函数的定义
    A = 10
    n_dimensions = x.shape[1]
    return A * n_dimensions + np.sum(x**2 - A * np.cos(2 * np.pi * x), axis=1)

# 调整后的参数设置
optimizer = ps.single.GlobalBestPSO(
    n_particles=10,
    dimensions=20,
    options={
        'c1': 2.0,  # cognitive parameter
        'c2': 2.0,  # social parameter
        'w': 0.7298,
    },
    bounds=(-1 * np.ones(20), 1 * np.ones(20)),
    ftol=0.001,
    ftol_iter=5,
    init_pos=np.random.uniform(-0.01, 0.01, (50, 20)),
)


cost, pos = optimizer.optimize(objective_function, iters=50)

print(f"最优解: {pos}")
print(f"最小值: {cost}")
print(f"最优解: {pos}")
print(f"最小值: {cost}")
print(f"目标函数被调用了 {model_call_count} 次")