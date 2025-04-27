# -*- encoding: utf-8 -*-
'''
@File    :   nsga2.py
@Create  :   2025-04-27 15:09:40
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import numpy as np
import pandas as pd
import joblib
from core.NSGA2 import NSGA2

model = 'GP'
model_filename = f'./models/{model}_PBias.pkl'
surr_model = joblib.load(model_filename)

