import json 
import os 
import pdb 
import pandas as pd 
import difflib
import json 
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

def similarity(str1, str2):
    if not (isinstance(str1, str) and isinstance(str2, str)):
        return 0
    seq = difflib.SequenceMatcher(None, str1, str2)
    return seq.ratio()  # 返回一个介于0到1之间的数，表示相似度百分比

def load_xlsx(xlsx_path):
    df = pd.read_excel(xlsx_path)
    column_data = {}
    for header in df.columns:
        column_data[header] = df[header].tolist()
    return column_data


def get_match_filename_from_db_dict(target_variable, db_dict, folder_name=''):
    ret_variable_names, ret_variable_descriptions, ret_data_file_names, ret_folder_names, ret_sim_scores = [], [], [], [], []

    variable_names = db_dict['Variable Name']
    variable_descriptions = db_dict['Variable Description']
    data_file_names = db_dict['Data File Name']

    for i, _ in enumerate(variable_descriptions):
        # 将句子转换为向量
        if isinstance(variable_descriptions[i], float):
            continue
        print(variable_descriptions[i])
        embedding1 = model.encode(target_variable, convert_to_tensor=True)
        embedding2 = model.encode(variable_descriptions[i], convert_to_tensor=True)

        # 计算语义相似度
        similarity = util.pytorch_cos_sim(embedding1, embedding2)
        if float(similarity[0][0].data) < 0.1:
            continue
        print('------------------------------------------------', similarity, target_variable, '-- vs --', '\"', variable_descriptions[i], '\"')
        ret_variable_names.append(variable_names[i])
        ret_variable_descriptions.append(variable_descriptions[i])
        ret_data_file_names.append(data_file_names[i])
        ret_folder_names.append(folder_name)
        tp = str(float(similarity[0][0].data))
        ret_sim_scores.append(tp)
    return ret_variable_names, ret_variable_descriptions, ret_data_file_names, ret_folder_names, ret_sim_scores

def sort_result_xpt_file_names_by_sim_score(result_xpt_file_names):
    
    sim_score_list = []
    sim_score_dict = {}
    for i, _ in enumerate(result_xpt_file_names):
        sim_score, variable_name, variable_description, data_file_name, folder_name  = result_xpt_file_names[i]
        if sim_score not in sim_score_dict:
            sim_score_list.append(sim_score)
            sim_score_dict[sim_score] = i
        else:
            sim_score = float(sim_score)
            sim_score += 0.0000000000000000001
            sim_score = str(sim_score)
            sim_score_list.append(sim_score)
            sim_score_dict[sim_score] = i
    
    list.sort(sim_score_list, reverse=True)
    
    ret_result_xpt_file_names = []
    for ss in sim_score_list:
        index = sim_score_dict[ss]
        ret_result_xpt_file_names.append(result_xpt_file_names[index])
    return ret_result_xpt_file_names

if __name__ == '__main__':
    demographics_data = load_xlsx('all_datas_variables_infos/DemographicsDataVariableList.xlsx')
    dietary_data = load_xlsx('all_datas_variables_infos/DietaryDataVariableList.xlsx')
    examination_data = load_xlsx('all_datas_variables_infos/ExaminationDataVariableList.xlsx')
    laboratory_data = load_xlsx('all_datas_variables_infos/LaboratoryDataVariableList.xlsx')
    questionnaire_data = load_xlsx('all_datas_variables_infos/QuestionnaireDataVariableList.xlsx')

    variables = open('au2024-variables-used.txt').readlines()
    variables = [i.split('\n')[0] for i in variables]
    
    
    all_json_dict = {}
    for variable in variables:
        # demographics_data
        result_xpt_file_names = []
        variable_names, ret_variable_descriptions, data_file_names, folder_names, sim_scores = get_match_filename_from_db_dict(variable, demographics_data, folder_name='DemographicsData')
        if len(variable_names) != 0:
            for i, _ in enumerate(variable_names):
                result_xpt_file_names.append([sim_scores[i], ret_variable_descriptions[i], variable_names[i], data_file_names[i], 'DemographicsData'])
        
        # dietary_data
        variable_names, ret_variable_descriptions, data_file_names, folder_names, sim_scores = get_match_filename_from_db_dict(variable, dietary_data, folder_name='DietaryData')
        if len(variable_names) != 0:
            for i, _ in enumerate(variable_names):
                result_xpt_file_names.append([sim_scores[i], ret_variable_descriptions[i], variable_names[i], data_file_names[i], 'DietaryData'])
        
        # examination_data
        variable_names, ret_variable_descriptions, data_file_names, folder_names, sim_scores = get_match_filename_from_db_dict(variable, examination_data, folder_name='ExaminationData')
        if len(variable_names) != 0:
            for i, _ in enumerate(variable_names):
                result_xpt_file_names.append([sim_scores[i], ret_variable_descriptions[i], variable_names[i], data_file_names[i], 'ExaminationData'])
        
        # laboratory_data
        variable_names, ret_variable_descriptions, data_file_names, folder_names, sim_scores = get_match_filename_from_db_dict(variable, laboratory_data, folder_name='LaboratoryData')
        if len(variable_names) != 0:
            for i, _ in enumerate(variable_names):
                result_xpt_file_names.append([sim_scores[i], ret_variable_descriptions[i], variable_names[i], data_file_names[i], 'LaboratoryData'])
        
        # questionnaire_data
        variable_names, ret_variable_descriptions, data_file_names, folder_names, sim_scores = get_match_filename_from_db_dict(variable, questionnaire_data, folder_name='QuestionnaireData')
        if len(variable_names) != 0:
            for i, _ in enumerate(variable_names):
                result_xpt_file_names.append([sim_scores[i], ret_variable_descriptions[i], variable_names[i], data_file_names[i], 'QuestionnaireData'])

        result_xpt_file_names = sort_result_xpt_file_names_by_sim_score(result_xpt_file_names)
        all_json_dict[variable] = result_xpt_file_names
    # 将字典写入JSON文件
    with open("preprocess_result_04.json", 'w', encoding='utf-8') as json_file:
        json.dump(all_json_dict, json_file, ensure_ascii=False, indent=4)



    

