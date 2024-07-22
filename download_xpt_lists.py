import pdb 
import os 
from bs4 import BeautifulSoup 

def get_download_links_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 找到所有的<a>标签，并筛选出带有href属性且链接以某些格式结尾的标签
        download_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.endswith(('.XPT')):  # 根据需要调整文件类型
                print('href', href)
                download_links.append('https://wwwn.cdc.gov' + href)
        
        return download_links
    except Exception as e:
        print(f'Failed to parse HTML file: {e}')
        return []

# 示例本地HTML文件路径
html_file_path = r'C:/Users/lvshu/Desktop/2024/NHANES-2007-2008/LaboratoryData/2007-2008 Laboratory Data - Continuous NHANES.html'
html_file_path = r'C:/Users/lvshu/Desktop/2024/NHANES-2007-2008/QuestionnaireData/2007-2008 Questionnaire Data - Continuous NHANES.html'
html_file_name = html_file_path.split('/')[-1]
dst_save_root = html_file_path.replace(html_file_name, '')
# 获取下载链接
download_links = get_download_links_from_file(html_file_path)

# # 示例下载链接列表
# download_links = [
#     'https://wwwn.cdc.gov/Nchs/Nhanes/2007-2008/PBCD_E.XPT',
#     'https://wwwn.cdc.gov/Nchs/Nhanes/2007-2008/CHLMDA_E.XPT',
#     'https://wwwn.cdc.gov/Nchs/Nhanes/2007-2008/HDL_E.XPT',
#     'https://wwwn.cdc.gov/Nchs/Nhanes/2007-2008/TRIGLY_E.XPT',
#     # 添加更多链接
# ]

def download_file(url, file_name):
    try:
        os.system(f'curl -L {url} -o {file_name}')
        print(f'Successfully downloaded {file_name}')
    except Exception as e:
        print(f'Failed to download {file_name}: {e}')

for idx, url in enumerate(download_links, start=1):
    file_name = url.split('/')[-1]  # 生成文件名，可以根据需要修改
    if os.path.exists(os.path.join(dst_save_root, file_name)):
        continue
    download_file(url, os.path.join(dst_save_root, file_name))