import requests
from bs4 import BeautifulSoup
import pandas
from sqlalchemy import create_engine

headers = {
    'User-Agent': 'Chrome/90.0.4430.93'
}

url = 'http://www.compassedu.hk/qs_'
response_1 = requests.get(url, headers=headers)
html = response_1.content.decode(encoding=response_1.apparent_encoding)
soup = BeautifulSoup(html, 'lxml')
table = soup.find('table', id='rk')
resList = pandas.read_html(table.prettify())
data = resList[0]
del (data['Free'])
data.to_csv('result.csv', index='false')
conn = create_engine('mysql+pymysql://root:root@192.168.56.101:3306/mysql?charset=utf8')
data.to_sql('univer2020', con=conn, if_exists='append', index=False)
