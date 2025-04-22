# -*- encoding: utf-8 -*-
'''
@File    :   analysize.py
@Create  :   2025-04-19 15:47:00
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from SALib.analyze import sobol as sobol_analyze
import os
import seaborn as sns
from SALib.sample import saltelli
from util.read import read_params
import matplotlib.pyplot as plt

results = pd.read_excel('job_kge.xlsx', sheet_name='Sheet1')

kge = results['KGE'].values
kge = np.array(kge, dtype=float)


params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
params_path = r'F:\Haihe\Set\params_sen\params\run_params.yaml'
params_info = read_params(params_path, params)

problem = {
    'num_vars': len(params_info),
    'names': list(params_info.keys()),
    'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
}
print(problem)
Si = sobol_analyze.analyze(problem, kge, calc_second_order=True, print_to_console=True)

print(Si)

# 创建 DataFrame 用于存储 S1 和 ST
df = pd.DataFrame({
    'names': params,  # 参数名称
    'S1': Si['S1'],
    'ST': Si['ST']
})
df.set_index('names', inplace=True)

# 创建 pic 文件夹（如果不存在的话）
output_dir = "pic"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 可视化：一阶灵敏度指数（S1）柱状图
plt.figure(figsize=(12, 6))
sns.barplot(x=df.index, y=df['S1'], color='blue', alpha=0.7)
plt.title("First-order Sensitivity Index (S1)")
plt.xlabel("Parameters")
plt.ylabel("S1 Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "S1_Sensitivity.png"))  # 保存图像
plt.show()

# 可视化：总阶灵敏度指数（ST）柱状图
plt.figure(figsize=(12, 6))
sns.barplot(x=df.index, y=df['ST'], color='green', alpha=0.7)
plt.title("Total-order Sensitivity Index (ST)")
plt.xlabel("Parameters")
plt.ylabel("ST Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "ST_Sensitivity.png"))  # 保存图像
plt.show()

s2_df = pd.DataFrame(Si['S2'])
s2_df.columns = [f"Param_{i+1}" for i in range(s2_df.shape[1])]

# 使用热图显示 S2
plt.figure(figsize=(10, 6))
sns.heatmap(s2_df, annot=True, cmap='coolwarm', center=0, linewidths=1)
plt.title("Two-Factor Sensitivity (S2)")
plt.show()