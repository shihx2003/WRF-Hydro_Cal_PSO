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

from core.ObjFun import MultObjFun
from util.jobs import jobs2xlsx

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
import seaborn as sns

def load_train_data():
    jobyaml = './jobs/surr_PBias_Fuping_20120721.yaml'
    frxst_dir = './result/Fuping_Sen_20190804'

    params_values = jobs2xlsx(jobyaml)
    obj_values = MultObjFun(frxst_dir, jobyaml)
    print(params_values)
    print(obj_values)
    X = params_values.drop(columns=['Job_id'])
    y = obj_values.drop(columns=['Job_id'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, y_train, X_test, y_test

obj_funs = ['PBias', 'CC', 'RMSE', 'NSE', 'KGE']
if __name__ == '__main__':

    X_train, y_train, X_test, y_test = load_train_data()
    # Define GP surrogate model for each objective function
    print("Training GP surrogate models...")
    gp_models = {}

    # 创建随机森林回归模型
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

    # 对每个目标训练模型
    import matplotlib.pyplot as plt

    for obj in obj_funs:
        rf_model.fit(X_train, y_train[obj])  # 训练模型
        y_pred = rf_model.predict(X_test)  # 预测
        
        mse = mean_squared_error(y_test[obj], y_pred)
        r2 = r2_score(y_test[obj], y_pred)
        
        print(f"Objective {obj}:")
        print(f"  MSE: {mse:.4f}")
        print(f"  R^2: {r2:.4f}")
        
        # 创建散点图
        plt.figure(figsize=(10, 5))
        
        # 左侧：预测值与实际值的散点图
        plt.subplot(1, 2, 1)
        plt.scatter(y_test[obj], y_pred, alpha=0.7)
        plt.plot([y_test[obj].min(), y_test[obj].max()], [y_test[obj].min(), y_test[obj].max()], 'r--')
        plt.xlabel('True Values')
        plt.ylabel('Predictions')
        plt.title(f'{obj} - Actual vs Predicted')
        
        # 右侧：热力图展示特征重要性
        plt.subplot(1, 2, 2)
        importances = pd.Series(rf_model.feature_importances_, index=X_train.columns)
        importances = importances.sort_values(ascending=False)
        sns.heatmap(importances.to_frame().T, annot=True, cmap='viridis', cbar=True)
        plt.title(f'{obj} - Feature Importance')
        plt.tight_layout()
        
        plt.savefig(f'rf_model_{obj}_performance.png')
        plt.show()