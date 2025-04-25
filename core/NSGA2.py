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
        :param problem: 优化问题，必须是pymoo的Problem子类
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

        # 初始化算法
        self.algorithm = NSGA2(
            pop_size=population_size,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=crossover_prob, eta=15),
            mutation=PM(prob=mutation_prob, eta=20),
            eliminate_duplicates=True
        )

        # 设置终止条件（基于最大代数）
        self.termination = get_termination("n_gen", n_gen)

    def run(self, verbose=False, save_results=True, output_dir="results"):
        """
        运行优化过程
        :param verbose: 是否打印优化过程 (默认: False)
        :param save_results: 是否保存结果到CSV (默认: True)
        :param output_dir: 结果保存目录 (默认: "results")
        :return: 优化结果对象
        """
        # 运行优化
        res = minimize(
            self.problem,
            self.algorithm,
            self.termination,
            seed=1,
            save_history=False,
            verbose=verbose
        )

        # 保存结果
        if save_results:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 保存Pareto前沿解
            np.savetxt(f"{output_dir}/pareto_front.csv", res.F, delimiter=",")
            # 保存对应的变量值
            np.savetxt(f"{output_dir}/pareto_vars.csv", res.X, delimiter=",")
            
        return res

# 示例问题定义（用户需要自定义自己的问题）
class MyProblem(Problem):
    """
    示例问题：ZDT1标准测试问题
    2个目标，30个变量，无约束
    """
    def __init__(self, n_var=30):
        super().__init__(n_var=n_var, 
                         n_obj=2, 
                         n_ieq_constr=0,
                         xl=np.zeros(n_var),
                         xu=np.ones(n_var))
        
    def _evaluate(self, X, out, *args, **kwargs):
        # 第一个目标函数
        f1 = X[:, 0]
        
        # 计算g(x)
        g = 1 + 9.0 / (self.n_var - 1) * np.sum(X[:, 1:], axis=1)
        
        # 第二个目标函数
        h = 1 - np.sqrt(f1 / g)
        f2 = g * h
        
        out["F"] = np.column_stack([f1, f2])

# 测试用代码
if __name__ == "__main__":
    # 示例用法
    problem = MyProblem(n_var=30)
    optimizer = NSGA2Runner(problem, 
                          population_size=100,
                          n_gen=200)
    
    # 运行优化
    result = optimizer.run(verbose=True)
    
    # 可视化结果（需要pymoo的额外依赖）
    try:
        from pymoo.visualization.scatter import Scatter
        print("Pareto前沿解集形状:", result.F.shape)
        Scatter().add(result.F).show()
    except ImportError:
        print("可视化需要pymoo的visualization模块")
