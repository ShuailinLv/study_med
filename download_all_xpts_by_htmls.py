import shutil 
import os 
import pdb 
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

def download_file(url, file_name, all_filed_xpt_urls):
    try:
        os.system(f'curl -L {url} -o {file_name}')
        print(f'Successfully downloaded {file_name}')
    except Exception as e:
        print(f'Failed to download {file_name}: {e}')
        all_filed_xpt_urls.append(url)

if __name__ == '__main__':
    htmls_path = 'nhanes_htmls'
    db_save_root = r'C:/Users/lvshu/Desktop/2024/NHANES'
    all_htmls = os.listdir(htmls_path)
    
    all_filed_xpt_urls = list()

    for html in all_htmls:
        html_full_path = os.path.join(htmls_path, html)
        year = html_full_path.split(' ')[0].split('\\')[-1]
        data_type = html_full_path.split(' ')[1]
        data_save_path = os.path.join(db_save_root, year, data_type)
        os.makedirs(data_save_path, exist_ok=True)

        download_links = get_download_links_from_file(html_full_path)

        for idx, url in enumerate(download_links, start=1):
            file_name = url.split('/')[-1]  # 生成文件名，可以根据需要修改
            if os.path.exists(os.path.join(data_save_path, file_name)):
                continue
            # print('url=', url)
            download_file(url, os.path.join(data_save_path, file_name), all_filed_xpt_urls)
            
    print("all_filed_xpt_urls=", all_filed_xpt_urls)
    print('please redownload if all_filed_xpt_urls != []')