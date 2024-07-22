import os 
import pdb 
import pandas as pd 


def load_xlsx(xlsx_path):
    df = pd.read_excel(xlsx_path)
    column_data = {}
    for header in df.columns:
        column_data[header] = df[header].tolist()
    return column_data

def save_xlsx_data_to_dict(demographics_data, variable_desriptions_dict):
    #  Variable Name', 'Variable Description', 'Data File Name', 'Data File Description', 'Begin Year', 'EndYear', 'Component', 'Use Constraints

    # 创建DataFrame
    # df = pd.DataFrame(data)

    # 写入CSV文件
    # df.to_csv('output.csv', index=False)
    for key in demographics_data:
        if key not in variable_desriptions_dict:
            variable_desriptions_dict[key] = demographics_data[key]
        else:
            variable_desriptions_dict[key].extend(demographics_data[key])


if __name__ == '__main__':
    demographics_data = load_xlsx('all_datas_variables_infos/DemographicsDataVariableList.xlsx')
    dietary_data = load_xlsx('all_datas_variables_infos/DietaryDataVariableList.xlsx')
    examination_data = load_xlsx('all_datas_variables_infos/ExaminationDataVariableList.xlsx')
    laboratory_data = load_xlsx('all_datas_variables_infos/LaboratoryDataVariableList.xlsx')
    questionnaire_data = load_xlsx('all_datas_variables_infos/QuestionnaireDataVariableList.xlsx')
    
    variable_desriptions_dict = {}

    save_xlsx_data_to_dict(demographics_data, variable_desriptions_dict)
    save_xlsx_data_to_dict(dietary_data, variable_desriptions_dict)
    save_xlsx_data_to_dict(examination_data, variable_desriptions_dict)
    save_xlsx_data_to_dict(laboratory_data, variable_desriptions_dict)
    save_xlsx_data_to_dict(questionnaire_data, variable_desriptions_dict)

    df = pd.DataFrame(variable_desriptions_dict)
    df.to_csv('all_data.csv', index=False)

    