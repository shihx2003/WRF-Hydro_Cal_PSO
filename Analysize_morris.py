# -*- encoding: utf-8 -*-
'''
@File    :   Analysize_morris.py
@Create  :   2025-04-19 16:09:52
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
from SALib.analyze import morris as morris_analyze
import os
import seaborn as sns
from SALib.sample import saltelli
from util.read import read_params
import matplotlib.pyplot as plt

# 读取结果文件
results = pd.read_excel('job_kge.xlsx', sheet_name='Sheet1')
kge = results['KGE'].values
kge = np.array(kge, dtype=float)

# 参数设置
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC','NEXP','RSURFEXP']
params_path = r'F:\Haihe\Set\params_sen\params\run_params.yaml'
params_info = read_params(params_path, params)

# 定义问题
problem = {
    'num_vars': len(params_info),
    'names': list(params_info.keys()),
    'bounds': [[param['minValue'], param['maxValue']] for param in params_info.values()],
}
print(problem)

params_values = np.load('./params_value.npy')
morris_results = morris_analyze.analyze(problem, params_values, kge)

# 打印分析结果
print(morris_results)

# 创建 DataFrame 用于存储 Morris 分析结果
df = pd.DataFrame({
    'names': params,  # 参数名称
    'mu': morris_results['mu'],  # 一阶效应
    'mu_star': morris_results['mu_star'],  # 总效应
    'sigma': morris_results['sigma'],  # 标准差
})

df.set_index('names', inplace=True)

# 创建 pic 文件夹（如果不存在的话）
output_dir = "pic"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 可视化：一阶效应（mu）柱状图
plt.figure(figsize=(12, 6))
sns.barplot(x=df.index, y=df['mu'], color='blue', alpha=0.7)
plt.title("First-order Effect (mu)")
plt.xlabel("Parameters")
plt.ylabel("mu Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "mu_Sensitivity.png"))  # 保存图像
plt.show()

# 可视化：总效应（mu_star）柱状图
plt.figure(figsize=(12, 6))
sns.barplot(x=df.index, y=df['mu_star'], color='green', alpha=0.7)
plt.title("Total Effect (mu_star)")
plt.xlabel("Parameters")
plt.ylabel("mu_star Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "mu_star_Sensitivity.png"))  # 保存图像
plt.show()

# 可视化：标准差（sigma）柱状图
plt.figure(figsize=(12, 6))
sns.barplot(x=df.index, y=df['sigma'], color='red', alpha=0.7)
plt.title("Standard Deviation (sigma)")
plt.xlabel("Parameters")
plt.ylabel("sigma Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "sigma_Sensitivity.png"))  # 保存图像
plt.show()

# 可视化：S2（交互效应）的热图
# 在 Morris 方法中，S2 是交互效应，可以通过 sigma 和 mu_star 来探索
# 创建 S2 DataFrame 并处理
# Morris 的交互效应通常是根据 mu_star 和 sigma 来解释的，但直接的 S2 输出不一定存在
s2_df = pd.DataFrame(morris_results['mu_star'] - morris_results['mu'])
s2_df.columns = ['Interaction Effect']
plt.figure(figsize=(10, 6))
sns.heatmap(s2_df, annot=True, cmap='coolwarm', center=0, linewidths=1)
plt.title("Interaction Effect (S2)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "S2_Interaction.png"))  # 保存图像
plt.show()