import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV, Ridge
from sklearn.model_selection import GridSearchCV


df = pd.read_excel(r'E:\AMsystem\Project\SXY-subject2\data\最新-元素种类-半波电位数据库.xlsx', sheet_name='组合2')
X2 = df[['Ni-Mn-Cu', 'Co-Mn-Cu', 'Co-Ni-Cu', 'Co-Ni-Mn', 'Fe-Mn-Cu', 'Fe-Ni-Cu', 'Fe-Ni-Mn',
          'Fe-Co-Cu', 'Fe-Co-Mn', 'Fe-Co-Ni', 'Pt-Pd', 'Pt-Ir', 'Pt-Ru', 'Pt-Rh', 'Pd-Ru',
          'Pd-Ir', 'Pd-Rh', 'Ru-Ir', 'Ru-Rh', 'Ir-Rh']]
y2 = df['E1/2']

# 标准化
scaler = StandardScaler()
X_scaled2 = scaler.fit_transform(X2)

# Lasso 模型
lasso = LassoCV(cv=5, random_state=0, alphas=[0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000])
lasso.fit(X_scaled2, y2)
lasso_coef = lasso.coef_

# Ridge 模型
ridge = Ridge()
param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
ridge_cv = GridSearchCV(ridge, param_grid, cv=5)
ridge_cv.fit(X_scaled2, y2)
ridge_coef = ridge_cv.best_estimator_.coef_

# 特征组合
features = X2.columns.tolist()

# 构建 DataFrame 并排序（按 Lasso 排序）
lasso_df = pd.DataFrame({'Feature': features, 'Importance': lasso_coef})
ridge_df = pd.DataFrame({'Feature': features, 'Importance': ridge_coef})
