# -*- encoding: utf-8 -*-
'''
@File    :   pso_cal_process2.py
@Create  :   2025-05-10 14:56:01
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import numpy as np
import pandas as pd

events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824', 'Fuping_20190804re']


# events = ['Fuping_20190804re','Fuping_20130628']
params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT', 'ChSSlp', 'MannN', 'OVROUGHRTFAC', 'RETDEPRTFAC', 'LKSATFAC', 'NEXP', 'RSURFEXP']
best_v = []
for event in events:
    path = f'./work/PSO/PSO_All/cal/PSO_{event}_calpro.xlsx'
    df  = pd.read_excel(path, sheet_name='Sheet2')
    df = df.drop(columns=['Unnamed: 0'])
    # print(df)

    best = df[19]
    best_draw = []
    c_best_value = 999999
    for i in range(len(best)):
        c_value = best[i]
        if c_value < c_best_value:
            c_best_value = c_value
            best_draw.append((i+1, c_best_value))
        else:
            best_draw.append((i+1, c_best_value))
    best_draw_df = pd.DataFrame(best_draw, columns=['Iteration', f'{event[7:]}'])
    best_v.append(best_draw_df)

    result = []
    i = 0
    for _, row in df.iterrows():

        row_df = pd.DataFrame(row.values, index=row.index, columns=[f'Value'])
        row_df['Iteration'] = i+1
        row_df['minf'] = row_df['Value']
        row_df = row_df.drop(columns=['Value'])
        row_df['best'] = best_draw[i][1]
        result.append(row_df)
        i += 1

    result_df = pd.concat(result, axis=0)
    result_df = result_df.reset_index()
    result_df = result_df.drop(columns=['index'])
    # Calculate proportion of minf values in range -0.5 to 1.5
    in_range_count = ((result_df['minf'] >= -0.5) & (result_df['minf'] <= 1.5)).sum()
    total_count = len(result_df['minf'])
    proportion = in_range_count / total_count
    print(f"Event {event}: Proportion of minf in range -0.5 to 1.5: {proportion:.4f}")
    
    # Save proportion to a list (defined outside the loop)
    try:
        proportion_list
    except NameError:
        proportion_list = []
    
    proportion_list.append((event, proportion))
    
    # print(result_df)

    # output_path = f'./work/PSO/PSO_All/cal/PSO_cal_{event}1.xlsx'
    # result_df.to_excel(output_path, index=False)

best_v_df = pd.concat(best_v, axis=1)
print(best_v_df)
best_v_df.to_excel('F:/Haihe/FinalPaperDate/PSO/cal/PSO_All.xlsx', index=False)
print(proportion_list)