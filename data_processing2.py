# 将每一组n和H2O%作图
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# 从 Excel 文件读取数据
df = pd.read_excel('your data file')


plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 22
plt.rcParams['axes.linewidth'] = 3  


def create_color_gradient(start_color, end_color, num_steps):
    cmap = LinearSegmentedColormap.from_list("custom_cmap", [start_color, end_color], N=num_steps)
    return cmap(np.arange(num_steps))
num_plots = int((df.shape[-1]-1)/2)

for i in range(int((df.shape[-1]-1)/2)):
    v = df['Potential/V']
    n = df[f'n{i+1}']
    H20 = df[f'H2O%{i+1}']

    index_0_3 = np.where(v == 0.2)[0][0]
    index_0_8 = np.where(v == 0.7)[0][0]

    v = v[index_0_3:index_0_8]
    n = n[index_0_3:index_0_8]
    H20 = H20[index_0_3:index_0_8]

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))
    # --------------
    v_new1 = v[::15]
    n_new1 = n[::15]
    ax1.plot(v_new1, n_new1, color=create_color_gradient('#00C8C8', '#1E3CFF', num_plots)[i], marker='o', markersize=8)

    v_new2 = v[::5]
    H20_new2 = H20[::5]
    ax2.plot(v_new2, H20_new2, color=create_color_gradient('#E4418B', '#FCA3A3', num_plots)[i], marker='o', markersize=5)
    

    # 在整个图像的左上角添加标号 (i+1)
    fig.text(0.04, 0.95, f'({i + 1})', fontsize=22, fontweight='bold', verticalalignment='top',
             horizontalalignment='left')

    
    ax2.set_xlabel(r'$\mathregular{Potential\ (V\ \mathit{vs}\ RHE)}$', fontsize=36)
    ax1.set_ylabel(r'$\mathregular{\mathit{n}}$', fontsize=36, fontstyle='italic')
    ax2.set_ylabel(r'$\mathregular{H_2O_2\ (\%)}$', fontsize=36)

    # 隐藏上边图的横轴刻度线
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    # 限制n图的纵坐标范围为1到5
    ax1.set_ylim(2.5, 4.5)
    # ax2.set_ylim(0, 15)
    # ------------------
    max_H20 = max(H20_new2)
    if max_H20>0 and max_H20<1:
        ax2.set_ylim(0, 10)
    elif max_H20 >=1 and max_H20<5:
        ax2.set_ylim(0, 20)
    elif max_H20 >=5 and max_H20 < 10:
        ax2.set_ylim(0, 30)
    else:
        ax2.set_ylim(0, 40)
    # ------------------


    # 调整子图间距
    plt.subplots_adjust(hspace=0.1)

    # plt.savefig(os.path.join('your folder', 'plot-'+ str(i+1) + '.png'))

    plt.show()
