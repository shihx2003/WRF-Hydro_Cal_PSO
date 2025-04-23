# -*- encoding: utf-8 -*-
'''
@File    :   jobid_csv.py
@Create  :   2025-04-19 12:48:14
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import yaml
import pandas as pd
import os
import numpy as np

with open('./jobs/sen_jobs.yaml', 'r', encoding='utf-8') as f:
    loaded_jobs = yaml.load(f, Loader=yaml.FullLoader)

rows = []
for sen_id, sen_data in loaded_jobs.items():
    set_params = sen_data['set_params']
    row = {'Job_id': sen_id}
    row.update(set_params)
    rows.append(row)
df = pd.DataFrame(rows)
df.to_excel('job_info.xlsx', index=False)
print(df)