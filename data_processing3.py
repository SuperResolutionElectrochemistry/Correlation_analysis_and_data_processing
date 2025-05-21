# 计算半波电位
import pandas as pd
import numpy as np
import os

def cal(i):
    return i*1000/0.2475


folder_path = r"Your data path"
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') and os.path.isfile(os.path.join(folder_path, f))]
n = len(csv_files)

print(f"该文件夹下的xlsx文件数量为: {len(csv_files)}")

l_i1 = []

file = pd.read_excel(r'E:\Project\ORR-n电子过程计算公式.xlsx').values
for i in range(len(file)):
    if file[i, 0] == "Potential/V":
        i1 = file[i + 1:, 0]
        l_i1.append(i1)

for a in range(1, n+1):
    file = str(a) + '.xlsx'  # .csv
    datapath = os.path.join(folder_path, file)
    data1 = pd.read_excel(datapath).values
    length = len(data1)
    for i in range(length):
        if data1[i, 0] == "Potential/V":
            i1 = data1[i + 2:, 1]
            for j in range(len(i1)):
                tem = i1[j]
                tem = float(tem)
                newi = cal(tem)
                i1[j] = newi
            l_i1.append(i1)

l_i1_array = np.array(l_i1).T

E = []

for j in range(1,len(l_i1_array[0])):
    e1 = l_i1_array[0][0]
    i1 = l_i1_array[0][j]
    e = l_i1_array[:,0]
    temp = l_i1_array[:,j]
    i1_2 = i1 /2

    cha = l_i1_array[:, j] - i1_2
    cha = np.abs(cha)
    idx = np.argmin(cha)
    E_temp = e[idx]
    E.append('{:.3f}'.format(E_temp))

title = []
for a in range(1, n+1):
    name = str(a) + '.xlsx'
    title.append(name)

E_all = []
E_all.append(title)
E_all.append(E)
E_all = np.array(E_all).T

df = pd.DataFrame(E_all)
df.columns = ['title','E-1/2']
df.to_excel('Your result file', index=False)
