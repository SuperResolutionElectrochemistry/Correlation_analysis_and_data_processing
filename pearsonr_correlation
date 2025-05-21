import pandas as pd
import scipy.stats as stats
import numpy as np

data = pd.read_excel(r'your data file')

current = data['E1/2']

# 计算元素组合与电流之间的皮尔逊相关系数
correlations = {}
for column in data.columns[:-1]:  
    corr, _ = stats.pearsonr(data[column], current)
    correlations[column] = corr


sorted_correlations = dict(sorted(correlations.items(), key=lambda item: item[1], reverse=True))


print("皮尔逊相关系数从大到小排序:")
for element, correlation in sorted_correlations.items():
    print(f"{element}: {correlation:.3f}")
