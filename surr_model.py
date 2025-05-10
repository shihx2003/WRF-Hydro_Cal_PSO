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

sen_date = r"F:\Haihe\Run\params_sen\work\sobol_n\Finial\allavg.xlsx"
cal_event = ['Fuping_20120721','Fuping_20130811', 'Fuping_20160718']
obj_fun = ['Bias', 'PBias', 'RMSE', 'CC', 'NSE', 'KGE']
params = ['BEXP', 'ChSSlp', 'DKSAT',  'MannN', 'OVROUGHRTFAC', 'REFKDT', 'RETDEPRTFAC', 'SLOPE', 'SMCMAX', 'LKSATFAC', 'NEXP', 'RSURFEXP']

params_obj_values= pd.read_excel(sen_date, sheet_name='Sheet1')
X = params_obj_values[params].values
Y = params_obj_values[obj_fun].values
print(X.shape, Y.shape)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
models = ['LR', 'Ridge', 'Lasso', 'ElasticNet', 'BayesianRidge', 'Huber', 'KNN', 'DT', 'RF', 'AdaBoost', 'MLP', 'SVR', 'GP']

models = ['RF']

for model in models:
    model_filename = f'./models/{model}.pkl'
    train = True
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
        print(y_pred.shape, y_test.shape)
