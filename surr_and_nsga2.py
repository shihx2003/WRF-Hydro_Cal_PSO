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

from util.read import read_params
from util.sample import sample_params
from util.jobs import jobs2yaml
from core import ObjFun

from pymoo.algorithms.moo.nsga2 import NSGA2

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.multioutput import MultiOutputRegressor

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score

def load_train_data():
    # 读取训练数据
    train_data = pd.read_excel('train_data.xlsx')

    target_columns = ['obs1', 'obs2', 'obs3']
    
    X = train_data.drop(columns=target_columns)
    y = train_data[target_columns]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, y_train, X_test, y_test

def surr_model(X_train, y_train, model_type='SVR', **kwargs):
    if model_type == 'SVR':
        model = SVR(kernel='rbf', C=1.0, epsilon=0.2)
    elif model_type == 'RF':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'KNN':
        model = KNeighborsRegressor(n_neighbors=5)
    elif model_type == 'DT':
        model = DecisionTreeRegressor(random_state=42)
    elif model_type == 'MLP':
        model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
    else:
        raise ValueError("Unsupported model type")
    
    # Fit the model
    model.fit(X_train, y_train)

    return model




obj_funs = ['PBias', 'CC', 'RMSE', 'NSE', 'KGE']
