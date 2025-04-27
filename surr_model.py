# -*- encoding: utf-8 -*-
'''
@File    :   surr_model.py
@Create  :   2025-04-27 14:18:01
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
from encodings.punycode import T
from re import X
from turtle import mode
import numpy as np
import pandas as pd
from core.ObjFun import CalObjFun
from util.jobs import jobs2xlsx
from sklearn.model_selection import train_test_split
from core.SurrModel import SurrModel
from util.visual import Draw_surr_ydyp
import joblib


def load_sen_date(path, sheet):
    """
    Load the sensitivity date from the file.
    """
    sen_date = pd.read_excel(path, sheet_name=sheet)
    sen_date = sen_date.drop(columns=['job_id'])
    params_values = sen_date[params]
    objfun_values = sen_date[obj_fun]

    return params_values, objfun_values

sen_date = r"F:\Haihe\Run\params_sen\surr\all\surr_date.xlsx"
cal_event = ['Fuping_20120721','Fuping_20130811', 'Fuping_20160718']
obj_fun = ['PBias', 'CC', 'RMSE', 'NSE', 'KGE']
obj_fun = ['PBias', 'CC']
params = ['BEXP', 'SMCMAX', 'SLOPE', 'DKSAT', 'REFKDT']


sheet = 'Fuping_20160718'
params_values, objfun_values = load_sen_date(sen_date, sheet)
X = params_values.values
Y = objfun_values.values

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
models = ['LR', 'Ridge', 'Lasso', 'ElasticNet', 'BayesianRidge', 'Huber', 'KNN', 'DT', 'RF', 'AdaBoost', 'MLP', 'SVR', 'GP']


# for model in models:
#     model_filename = f'./models/{model}_PBias.pkl'
#     train = True
#     if train:
#         surr_model = SurrModel(model=model, multi=True, random_state=42)
#         surr_model.fit(x_train, y_train)
#         joblib.dump(surr_model, model_filename)
#         print(f"Model saved to {model_filename}")
#         y_pred = surr_model.predict(x_test)
#         print(y_pred.shape, y_test.shape)
#         for i, obj in enumerate(obj_fun):
#             Draw_surr_ydyp(y_test[:, i], y_pred[:, i], filename=f'{model}_{obj}')
#     else:
#         surr_model = joblib.load(model_filename)
#         y_pred = surr_model.predict(x_test)
#         print(y_pred.shape, y_test.shape)

model = 'GB'
model_filename = f'./models/{model}_PBias_CC.pkl'
train = False
if train:
    surr_model = SurrModel(model=model, multi=True, random_state=42)
    surr_model.fit(x_train, y_train)
    joblib.dump(surr_model, model_filename)
    print(f"Model saved to {model_filename}")
    y_pred = surr_model.predict(x_test)
    print(y_pred.shape, y_test.shape)
    for i, obj in enumerate(obj_fun):
        Draw_surr_ydyp(y_test[:, i], y_pred[:, i], filename=f'{model}_{obj}')
else:
    surr_model = joblib.load(model_filename)
    y_pred = surr_model.predict(x_test)
    print(y_pred)
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
        super().__init__(n_var=n_var, n_obj=2, n_constr=0, xl=xl, xu=xu)
        self.model_filename = model_filename
        self.surr_model = joblib.load(model_filename)

    def _evaluate(self, x, out, *args, **kwargs):
        """
        使用代理模型进行预测
        :param x: 输入的决策变量
        :param out: 输出目标值字典
        """
        
        y= self.surr_model.predict(np.array([x]))
        y_pred = y.copy()[0]
        y_pred[0] = abs(y_pred[0])  # 第一个值取绝对值
        y_pred[1] = -y_pred[1]      # 第二个值取负值
        out["F"] = np.column_stack([y_pred])


params = ['BEXP','SMCMAX','SLOPE','DKSAT','REFKDT']

n_var = len(params)
xl = np.array([0.4, 0.8, 0.0, 0.2, 0.1])  # 决策变量下界，可以根据你的实际情况调整
xu = np.array([1.9, 1.2, 1.0, 10, 4.0])  # 决策变量上界，可以根据你的实际情况调整

# 创建问题实例
problem = SurrogateModelProblem(model_filename, n_var, xl, xu)
runner = NSGA2Runner(problem)
result = runner.run(verbose=True)
print("Pareto Front:")
print(result.F)

pareto_solutions = pd.DataFrame(result.X, columns=params)
pareto_objectives = pd.DataFrame(result.F, columns=[f'{obj}_nsag2' for obj in obj_fun])
surr_objs = surr_model.predict(pareto_solutions.values)
surr_objs = pd.DataFrame(surr_objs, columns=[f'{obj}_surr' for obj in obj_fun])
pareto_front = pd.concat([pareto_solutions, pareto_objectives, surr_objs], axis=1)
pareto_front.to_csv('./result/pareto_front_surrogate.csv', index=False)
print(f"Pareto front saved to './result/pareto_front_surrogate.csv'")