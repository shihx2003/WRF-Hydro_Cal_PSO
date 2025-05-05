# -*- encoding: utf-8 -*-
'''
@File    :   pso_best_heatmap.py
@Create  :   2025-05-04 16:31:20
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取Excel文件
objs = ['Bias', 'PBias', 'NSE', 'RMSE', 'CC', 'KGE', 'MF']
file = './work/PSO/PSO_Best/Fun/PSO_best_results.xlsx'
for obj in objs:
    df = pd.read_excel(file, sheet_name=obj, index_col=0)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=True, cmap="YlGnBu", linewidths=0.5)
    plt.title(obj, fontsize=16)
    plt.show()
