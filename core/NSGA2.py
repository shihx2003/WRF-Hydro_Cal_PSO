# -*- encoding: utf-8 -*-
'''
@File    :   NSGA2.py
@Create  :   2025-04-24 18:46:03
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
import numpy as np
import os

class NSGA2Runner:
    def __init__(self, problem, population_size=100, n_gen=200, crossover_prob=0.9, mutation_prob=0.1):
        """
        初始化NSGA-II优化器
        :param problem: 优化问题,必须是pymoo的Problem子类
        :param population_size: 种群大小 (默认: 100)
        :param n_gen: 迭代代数 (默认: 200)
        :param crossover_prob: 交叉概率 (默认: 0.9)
        :param mutation_prob: 变异概率 (默认: 0.1)
        """
        self.problem = problem
        self.population_size = population_size
        self.n_gen = n_gen
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

        self.algorithm = NSGA2(
            pop_size=population_size,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=crossover_prob, eta=15),
            mutation=PM(prob=mutation_prob, eta=20),
            eliminate_duplicates=True
        )
        self.termination = get_termination("n_gen", n_gen)

    def run(self, verbose=False, save_results=False, output_dir="result"):
        """
        运行优化过程
        :param verbose: 是否打印优化过程 (默认: False)
        :param save_results: 是否保存结果到CSV (默认: True)
        :param output_dir: 结果保存目录 (默认: "results")
        :return: 优化结果对象
        """
        res = minimize(
            self.problem,
            self.algorithm,
            self.termination,
            seed=1,
            save_history=False,
            verbose=verbose
        )
        if save_results:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            np.savetxt(f"{output_dir}/pareto_front.csv", res.F, delimiter=",")
            np.savetxt(f"{output_dir}/pareto_vars.csv", res.X, delimiter=",")
            
        return res

