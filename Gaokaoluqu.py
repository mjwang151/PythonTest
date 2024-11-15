import requests
from bs4 import BeautifulSoup
import pandas
from sqlalchemy import create_engine
import json

headers = {
    'User-Agent': 'Chrome/90.0.4430.93'
}

url = 'https://static-data.eol.cn/www/2.0/schoolspecialindex/2020/30/32/1/7/1.json'
response_1 = requests.get(url, headers=headers)
result = response_1.text
user_dic = json.loads(result)
print(user_dic['data']['numFound'])
jsonarr = user_dic['data']['item']
for js in jsonarr:
    print(js)













