import os
import pandas as pd
import numpy as np

folder_path = r"your data path"
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') and os.path.isfile(os.path.join(folder_path, f))]
n = len(csv_files)

print(f"该文件夹下的文件数量为: {len(csv_files)}")


l_i1i2 = []

for a in range(1, n+1):
    file = str(a) + '.xlsx'  # .csv
    datapath = os.path.join(folder_path, file)
    # data = pd.read_csv(datapath, on_bad_lines="skip")
    data1 = pd.read_excel(datapath).values
    length = len(data1)
    for i in range(length):
        if data1[i,0] == "Potential/V":
            text = data1[i+2:,:]
            l_i1i2.append(text[:,0])
            break
    break


def cal_n (t1, t2):
    n = 4*t1/(t1 + t2/0.37)
    return n

def cal_H20(ti, t2):
    H20 = -200*(t2/0.37)/(ti + t2/0.37)
    return H20


for a in range(1, n+1):
    file = str(a) + '.xlsx'  # .csv
    datapath = os.path.join(folder_path, file)
    data2 = pd.read_excel(datapath).values
    length = len(data2)
    for i in range(length):
        if data2[i, 0] == "Potential/V":
            text = data2[i + 2:, :]
            i1 = text[:, 1]
            i2 = text[:, -1]
            for j in range(len(i1)):
                temp1 = i1[j]
                temp1 = float(temp1)
                temp2 = i2[j]
                temp2 = float(temp2)
                n = cal_n(temp1, temp2)
                H20 = cal_H20(temp1, temp2)
                i1[j] = n
                i2[j] = H20
                # print(1)
            l_i1i2.append(i1)
            l_i1i2.append(i2)
            break
data2_array = np.array(l_i1i2).T

df = pd.DataFrame(data2_array)
columns = ['Potential/V']
for i in range(1, int((len(data2_array[0])-1)/2+1)):   # len(data2_array[0]) = 161
    columns.extend([f'n{i}', f'H2O%{i}'])

df.columns = columns

df.to_excel('your output file', index=False)
