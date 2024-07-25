import glob 
import pdb 
import os  
import pandas as pd 

# data = pd.read_sas(xpt_full_path, format='xport')

def get_participants_number(data_root, cycle_list):
    seqn_list = list()
    for cycle in cycle_list:
        cycle_full_path = os.path.join(data_root, cycle)
        demographics_full_path = os.path.join(cycle_full_path, 'Demographics')
        # dietary_full_path = os.path.join(cycle_full_path, 'Dietary')
        # examination_full_path = os.path.join(cycle_full_path, 'Examination')
        # laboratory_full_path = os.path.join(cycle_full_path, 'Laboratory')
        # questionnaire_full_path = os.path.join(cycle_full_path, 'Questionnaire')
        demographics_xpt_full_path = glob.glob(os.path.join(demographics_full_path, '*XPT'))[0]
        demographics_data = pd.read_sas(demographics_xpt_full_path)
        seqn_list.extend(demographics_data['SEQN'].tolist())
    all_len_seqn = len(set(seqn_list))
    print('participants_number', all_len_seqn)
    return all_len_seqn

# def get_pfas_paricipants_number(data_root, cycle_list):
#     # Polyflu

def all_xpts_to_csvs(data_root, cycle_list):
    def convert_folder_xpts_to_csvs(folder_full_path):
        xpt_list = glob.glob(os.path.join(folder_full_path, '*XPT'))
        for xpt_path in xpt_list:
            dst_path = xpt_path.replace('.XPT', '.csv')
            if os.path.exists(dst_path):
                print('continue', dst_path)
                continue
            print('saving csv path', dst_path)
            reader = pd.read_sas(xpt_path, format='xport', chunksize=10000)
            chunks = []
            for chunk in reader:
                chunks.append(chunk)
            df = pd.concat(chunks, ignore_index=True)

            df.to_csv(dst_path)

    for cycle in cycle_list:
        cycle_full_path = os.path.join(data_root, cycle)
        demographics_full_path = os.path.join(cycle_full_path, 'Demographics')
        dietary_full_path = os.path.join(cycle_full_path, 'Dietary')
        examination_full_path = os.path.join(cycle_full_path, 'Examination')
        laboratory_full_path = os.path.join(cycle_full_path, 'Laboratory')
        questionnaire_full_path = os.path.join(cycle_full_path, 'Questionnaire')
        
        convert_folder_xpts_to_csvs(demographics_full_path)
        convert_folder_xpts_to_csvs(dietary_full_path)
        convert_folder_xpts_to_csvs(examination_full_path)
        convert_folder_xpts_to_csvs(laboratory_full_path)
        convert_folder_xpts_to_csvs(questionnaire_full_path)
      

if __name__ == '__main__':
    cycle_list = ['2003-2004', '2005-2006', '2007-2008', '2009-2010', '2011-2012', '2013-2014', '2015-2016', '2017-2018']
    data_root = r'D:/2024/NHANES'
    # get_participants_number(data_root, cycle_list)
    all_xpts_to_csvs(data_root, cycle_list)



    
