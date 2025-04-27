# -*- encoding: utf-8 -*-
'''
@File    :   SurrModel.py
@Create  :   2025-04-24 16:35:30
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge, HuberRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, StackingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor



models = ['LR', 'Ridge', 'Lasso', 'ElasticNet', 'BayesianRidge', 'Huber', 'KNN', 'DT', 'RF', 'GB', 'AdaBoost', 'MLP', 'SVR', 'GP']
def SurrModel(model, multi=False, random_state=42):
    if model == 'LR':
        base_model = LinearRegression()
    elif model == 'Ridge':
        base_model = Ridge(alpha=1.0)
    elif model == 'Lasso':
        base_model = Lasso(alpha=0.1)
    elif model == 'ElasticNet':
        base_model = ElasticNet(alpha=0.1, l1_ratio=0.7)
    elif model == 'BayesianRidge':
        base_model = BayesianRidge()
    elif model == 'Huber':
        base_model = HuberRegressor()
    elif model == 'KNN':
        base_model = KNeighborsRegressor(n_neighbors=5)
    elif model == 'DT':
        base_model = DecisionTreeRegressor(random_state=random_state)
    elif model == 'RF':
        base_model = RandomForestRegressor(n_estimators=100, random_state=random_state)
    elif model == 'GB':
        base_model = GradientBoostingRegressor(random_state=random_state)
    elif model == 'AdaBoost':
        base_model = AdaBoostRegressor(n_estimators=100, random_state=random_state)
    elif model == 'MLP':
        base_model = MLPRegressor(max_iter=100000, random_state=random_state)
    elif model == 'SVR':
        base_model = SVR(kernel='rbf', C=1.0, epsilon=0.1, gamma='scale')
    elif model == 'GP':
        kernel = C(1.0, (1e-4, 1e9)) * RBF(1.0, (1e-4, 1e9))
        base_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=1e-2, random_state=random_state)
    elif model == 'Stacking':
        base_model = StackingRegressor(
            estimators=[('rf', RandomForestRegressor(n_estimators=100)),
                        ('gb', GradientBoostingRegressor())],
            final_estimator=LinearRegression()
        )
    else:
        raise ValueError(f"Unknown model type: {model}")

    if multi:
        return MultiOutputRegressor(base_model)
    else:
        return base_model