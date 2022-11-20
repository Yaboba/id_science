import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

def get_profiles(inn: int=7604011791,)->list:
    url = f'https://api.idscience.ru/v2/profile/org/{inn}'
    response = requests.get(url=url)
    info = json.loads(response.content)
    return info['profiles']

def parser_html(id: int)->dict:
    url = f'https://www.idscience.ru/profile/?{id}'
    response = requests.get(url=url)
    html_doc = response.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = {}

    title = soup.title.get_text()
    fio = title[:title.find('|') - 1]

    list_znach = soup.find_all('a', class_='punktir')
    for i in list_znach:
        data[i['title']] = i.get_text()
    data['id_science'] = id
    data['fio'] = fio

    return data

def main():
    id_list = get_profiles()
    data = {'id_science':[], 'fio':[], 'ORCiD':[],
            'РИНЦ SPIN-код':[], 'Scopus Author ID':[],
            'ResearcherID':[], 'Google Scholar ID':[],
            'Profile Page':[], 'Personal Site':[]}
    for id in id_list:
        person_info = parser_html(id)
        for key in data:
            if key in person_info:
                data[key].append(person_info[key])
            else:
                data[key].append('-')
    df = pd.DataFrame(data)
    df.to_excel('result.xlsx', index=False)

if __name__=='__main__':
    main()
