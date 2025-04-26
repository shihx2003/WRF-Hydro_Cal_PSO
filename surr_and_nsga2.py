# -*- encoding: utf-8 -*-
'''
@File    :   surr_and_nsga2.py
@Create  :   2025-04-23 12:43:28
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib

import numpy as np
import pandas as pd

from core.ObjFun import CalObjFun
from util.jobs import jobs2xlsx
from util.read import read_obs
from util.visual import Draw_surr_ydyp
from core.SurrModel import SurrModel
from sklearn.model_selection import train_test_split
import joblib
import os

def load_result(cal_events, obj_fun, filename=None, **kwargs):

    surr_job_ids = [f'surr_{i}' for i in range(1, 201)]
    obj_resut = None
    for event in cal_events:
        jobyaml = f'./jobs/surr_PBias_{event}.yaml'
        frxst_dir = './result/Fuping_surr_PBias'
        obj_values = CalObjFun(frxst_dir, jobyaml)
        obj_values['job_id'] = surr_job_ids
        obj_values = obj_values.rename(columns={obj: f'{event}_{obj}' for obj in obj_fun})

        if obj_resut is None:
            obj_resut = obj_values
        else:
            obj_resut = pd.concat([obj_resut, obj_values.drop(columns='job_id')], axis=1)

    params_values = jobs2xlsx(jobyaml)
    params_values['job_id'] = surr_job_ids

    if filename is not None:
        obj_resut.to_excel(f'./surr/{filename}_objr.xlsx', index=False)
        params_values.to_excel(f'./surr/{filename}_paramsr.xlsx', index=False)

    return obj_resut, params_values
    

cal_events = ['Fuping_20160718', 'Fuping_20190804', 'Fuping_20120721', 'Fuping_20200717', 'Fuping_20130811']
obj_fun = ['PBias', 'CC', 'RMSE', 'NSE', 'KGE']
surr_job_ids = [f'surr_{i}' for i in range(1, 201)]

bool_read = False
if bool_read:
    obj_resut, params_values = load_result(cal_events, obj_fun, filename='surr_PBias')
    obj_resut.to_csv('./surr/surr_PBias_obj.csv', index=False)
    params_values.to_csv('./surr/surr_PBias_params.csv', index=False)
else:
    obj_resut = pd.read_csv('./surr/surr_PBias_obj.csv')
    params_values = pd.read_csv('./surr/surr_PBias_params.csv')

avg_obj = pd.DataFrame()
avg_obj['job_id'] = obj_resut['job_id']
cal_events = ['Fuping_20190804', 'Fuping_20120721', 'Fuping_20200717', 'Fuping_20130811'] #'Fuping_20160718', 
for obj in obj_fun:
    avg_obj[obj] = obj_resut[[f'{event}_{obj}' for event in cal_events]].mean(axis=1)
    obj_resut[obj] = obj_resut[[f'{event}_{obj}' for event in cal_events]].mean(axis=1)


X = params_values.drop(columns='job_id').values

event_obj = {}
for obj in obj_fun:
    event_obj[obj] = [f'{event}_{obj}' for event in cal_events] + [obj]

Y = abs(obj_resut[event_obj['PBias']].copy().values)


x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
model = 'MLP'
model_filename = f'./models/{model}_PBias_surrogate.pkl'
train = True
if train:
    surr_model = SurrModel(model=model, multi=True, random_state=42)
    surr_model.fit(x_train, y_train)
    joblib.dump(surr_model, model_filename)
    print(f"Model saved to {model_filename}")
    y_pred = surr_model.predict(x_test)
    print(y_pred.shape, y_test.shape)
    for i, obj in enumerate(event_obj['PBias']):
        Draw_surr_ydyp(y_test[:, i], y_pred[:, i], filename=f'{model}_{obj}')
else:
    surr_model = joblib.load(model_filename)
    y_pred = surr_model.predict(x_test)
    print(y_pred.shape, y_test.shape)


from pymoo.core.problem import ElementwiseProblem
from core.NSGA2 import NSGA2Runner
class SurrogateModelProblem(ElementwiseProblem):
    def __init__(self, model_filename, n_var, xl, xu):
        """
        :param model_filename: 代理模型的文件名
        :param n_var: 决策变量的数量
        :param xl: 决策变量的下界
        :param xu: 决策变量的上界
        """
        super().__init__(n_var=n_var, n_obj=5, n_constr=0, xl=xl, xu=xu)
        self.model_filename = model_filename
        self.surr_model = joblib.load(model_filename)

    def _evaluate(self, x, out, *args, **kwargs):
        """
        使用代理模型进行预测
        :param x: 输入的决策变量
        :param out: 输出目标值字典
        """
        # 预测目标函数的值，返回的是一个包含 5 个目标函数值的数组
        y_pred = self.surr_model.predict(np.array([x]))  # 预测时需要将 x 转为 2D 数组
        
        # 将预测的目标值赋给 out["F"]
        out["F"] = np.column_stack([y_pred]) 


model_filename = f'./models/{model}_KGE_surrogate.pkl'
params = ['BEXP','SMCMAX','SLOPE','DKSAT','REFKDT']

n_var = len(params)
xl = np.array([0.4, 0.8, 0.0, 0.2, 0.1])  # 决策变量下界，可以根据你的实际情况调整
xu = np.array([1.9, 1.2, 1.0, 10, 4.0])  # 决策变量上界，可以根据你的实际情况调整

# 创建问题实例
problem = SurrogateModelProblem(model_filename, n_var, xl, xu)

# 创建并运行 NSGA2 优化器
runner = NSGA2Runner(problem)
result = runner.run(verbose=True)

# 打印最终的 Pareto 前沿
print("Pareto Front:")
print(result.F)

# 将结果保存到CSV文件中
pareto_solutions = pd.DataFrame(result.X, columns=params)
pareto_objectives = pd.DataFrame(result.F, columns=[f'{obj}_surrogate' for obj in event_obj['KGE']])
pareto_front = pd.concat([pareto_solutions, pareto_objectives], axis=1)
pareto_front.to_csv('./result/pareto_front_surrogate.csv', index=False)
print(f"Pareto front saved to './result/pareto_front_surrogate.csv'")