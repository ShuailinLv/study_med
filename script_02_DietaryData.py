import pdb 
import pandas as pd
import os 

# # 读取 SAS XPORT 文件 (.xpt)
# xpt_file = r'C:/Users/lvshu/Desktop/2024/NHANES-2003-2004/DietaryData/DR1IFF_C.XPT'

# data = pd.read_sas(xpt_file, format='xport')

# # 将数据写入 CSV 文件
# csv_file = xpt_file.replace('DR1IFF_C.XPT', 'DR1IFF_C.csv')
# data.to_csv(csv_file, index=False)

# print(f"Data has been successfully written to {csv_file}")


dietary_data_path = r'C:/Users/lvshu/Desktop/2024/NHANES-2003-2004/DietaryData'
dietary_xpts = os.listdir(dietary_data_path)

for xpt in dietary_xpts:
    if '.XPT' not in xpt:
        continue
    xpt_full_path = os.path.join(dietary_data_path, xpt)
    csv_full_path = xpt_full_path.replace('.XPT', '.csv')
    data = pd.read_sas(xpt_full_path, format='xport')
    data.to_csv(csv_full_path, index=False)
    print(f"Data has been successfully written to {csv_full_path}")