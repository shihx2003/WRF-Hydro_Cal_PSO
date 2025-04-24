# -*- encoding: utf-8 -*-
'''
@File    :   VisualSi.py
@Create  :   2025-04-22 22:20:54
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

pic_dir = './pic/'
if not os.path.exists(pic_dir):
    os.makedirs(pic_dir)

def Draw_sobol_S1_ST(problem, Si, filename='sobol_S1_ST', figsize=(18, 6), conf=False):
    param_names = problem['names']
    S1, S1_conf, ST, ST_conf = Si['S1'], Si['S1_conf'], Si['ST'], Si['ST_conf']
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    if conf:
        axes[0].barh(param_names, S1, xerr=S1_conf, 
            color='skyblue', ecolor='tomato', capsize=5)
        axes[1].barh(param_names, ST, xerr=ST_conf, 
                    color='lightgreen', ecolor='tomato', capsize=5)
    else:
        axes[0].barh(param_names, S1, color='skyblue')
        axes[1].barh(param_names, ST, color='lightgreen')

    axes[0].set_title('First-order Sobol indices (S1)', fontsize=14)
    axes[0].set_xlabel('Sensitivity Index', fontsize=12)
    axes[0].set_xlim(min(S1)-0.1, max(S1) * 1.1)  # Set max x value with 10% margin
    axes[0].axvline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[1].set_title('Total-order Sobol indices (ST)', fontsize=14)
    axes[1].set_xlabel('Sensitivity Index', fontsize=12)
    axes[1].set_xlim(min(ST)-0.1, max(ST) * 1.1)  # Set max x value with 10% margin
    axes[1].axvline(0, color='gray', linestyle='--', linewidth=0.8)
    
    plt.tight_layout()
    plt.savefig(f'./pic/{filename}.png', dpi=300)
    plt.close()

def Draw_sobol_S2(problem, Si, filename='sobol_S2', figsize=(12, 10), conf=False):
    params = problem['names']
    S2_matrix = Si['S2']
    S2_conf_matrix = Si['S2_conf']
    S2_matrix = np.nan_to_num(S2_matrix, nan=np.nan)
    S2_conf_matrix = np.nan_to_num(S2_conf_matrix, nan=np.nan)
    S2_df = pd.DataFrame(S2_matrix, columns=params, index=params)
    S2_conf_df = pd.DataFrame(S2_conf_matrix, columns=params, index=params)
    plt.figure(figsize=figsize)
    heatmap = sns.heatmap(S2_df, annot=True, cmap="YlGnBu", fmt='.2f', linewidths=0.5,
                          cbar_kws={'label': 'S2 (Second-order Sensitivity Index)'}, 
                          mask=np.isnan(S2_df),
                          square=True)
    if conf:
        for y in range(S2_df.shape[0]):
            for x in range(S2_df.shape[1]):
                if not np.isnan(S2_df.iloc[y, x]):
                    heatmap.text(x + 0.5, y + 0.5, f"{S2_conf_df.iloc[y, x]:.2f}", 
                                 color="black", ha="center", va="center", fontsize=9)
    plt.title('Second-order Sobol Interactions (S2)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    plt.savefig(f'./pic/{filename}.png', dpi=300)
    plt.close()

def Draw_morris_mu(problem, Si, filename='morris_mu', figsize=(12, 8)):
    mu = Si['mu']
    params = problem['names']
    
    mu_df = pd.DataFrame(mu, index=params, columns=["mu"])

    plt.figure(figsize=figsize)
    sns.barplot(y=mu_df.index, x=mu_df["mu"], hue=mu_df.index, palette="viridis", legend=False)
    plt.title('Morris Sensitivity Analysis - mu (Mean Effect)', fontsize=14)
    plt.ylabel('Parameters', fontsize=12)
    plt.xlabel('mu', fontsize=12)

    plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)

    plt.tight_layout()
    plt.savefig(f'./pic/{filename}.png', dpi=300)
    plt.close()



def Draw_morris_mu_star(problem, Si, filename='morris_mu_star', figsize=(12, 8)):
    mu_star = Si['mu_star']
    params = problem['names']
    
    mu_star_df = pd.DataFrame(mu_star, index=params, columns=["mu_star"])

    plt.figure(figsize=figsize)
    sns.barplot(y=mu_star_df.index, x=mu_star_df["mu_star"], hue=mu_star_df.index, palette="viridis", legend=False)
    plt.title('Morris Sensitivity Analysis - mu_star (Normalized Mean Effect)', fontsize=14)
    plt.ylabel('Parameters', fontsize=12)
    plt.xlabel('mu_star', fontsize=12)

    plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)

    plt.tight_layout()
    plt.savefig(f'./pic/{filename}.png', dpi=300)
    plt.close()

def Draw_morris_sigma(problem, Si, filename='morris_sigma', figsize=(12, 8)):
    sigma = Si['sigma']
    params = problem['names']
    
    sigma_df = pd.DataFrame(sigma, index=params, columns=["sigma"])

    plt.figure(figsize=figsize)
    sns.barplot(y=sigma_df.index, x=sigma_df["sigma"], hue=sigma_df.index, palette="viridis", legend=False)
    plt.title('Morris Sensitivity Analysis - sigma (Standard Deviation)', fontsize=14)
    plt.ylabel('Parameters', fontsize=12)
    plt.xlabel('sigma', fontsize=12)

    plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)

    plt.tight_layout()
    plt.savefig(f'./pic/{filename}.png', dpi=300)
    plt.close()

from sklearn.metrics import mean_squared_error, r2_score

def Draw_surr_ydyp(y_test, y_pred, filename, **kwargs):
    figsize = kwargs.get('figsize', (10, 10))

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    plt.figure(figsize=figsize)
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.title('Actual vs Predicted')

    plt.text(0.05, 0.95, f'R² = {r2:.4f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
    plt.text(0.05, 0.85, f'RMSE = {rmse:.4f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

    plt.grid(True)
    plt.tight_layout()
    # Set uniform axis limits with a bit of padding
    min_val = min(min(y_test), min(y_pred))
    max_val = max(max(y_test), max(y_pred))
    margin = (max_val - min_val) * 0.1  # 10% margin
    plt.xlim(min_val - margin, max_val + margin)
    plt.ylim(min_val - margin, max_val + margin)
    plt.savefig(f'./pic/{filename}.png', dpi=300)
    plt.close()