# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Create  :   2025-04-23 19:58:40
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib

from core import ObjFun
import pandas as pd
import numpy as np

obj = ObjFun.MultObjFun('F:/Haihe/Run/params_sen/result/Fuping_Sen_20190804', 'F:/Haihe/Run/params_sen/jobs/sen_jobs_Fuping_20190804.yaml', './test.xlsx')
print(obj)