import shutil
import os 
import pdb 
import pandas as pd 
import shutil 

def load_xlsx(xlsx_path):
    df = pd.read_excel(xlsx_path)
    column_data = {}
    for header in df.columns:
        column_data[header] = df[header].tolist()
    return column_data


def copy_data_to_dst_folder(target_index_data, dst_path, src_data_root=''):
    
    data_file_name_list = target_index_data['Data File Name']

    src_data_folders = os.listdir(src_data_root)
    src_data_folder_paths = []
    for i in src_data_folders:
        if os.path.isfile(os.path.join(src_data_root, i)):
            continue 
        src_data_folder_paths.append(os.path.join(src_data_root, i))

    for data_file_name in data_file_name_list:
        data_file_name = data_file_name + '.XPT'
        for src_data_folder_path in src_data_folder_paths:
            file_full_path = os.path.join(src_data_folder_path, data_file_name)
            if os.path.exists(file_full_path):
                file_dst_full_path = os.path.join(dst_path, data_file_name)
                shutil.copy(file_full_path, file_dst_full_path)
                data = pd.read_sas(file_dst_full_path, format='xport')
                csv_full_path = file_dst_full_path.replace('.XPT', '.csv')
                data.to_csv(csv_full_path, index=False)


if __name__ == '__main__':
    target_index_data = load_xlsx('0_target_data.xlsx')
    dst_path = r'C:/Users/lvshu/Desktop/2024/au2024data'
    os.makedirs(dst_path, exist_ok=True)
    copy_data_to_dst_folder(target_index_data, dst_path, src_data_root=r'C:/Users/lvshu/Desktop/2024/NHANES-2003-2004')   
    