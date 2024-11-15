import requests
from bs4 import BeautifulSoup

result = ''

headers = {
    'User-Agent': 'Chrome/90.0.4430.93'
}
for i in range(13):
    url = 'https://www.qiushibaike.com/text/page/{i+1}/'
    response_1 = requests.get(url, headers=headers)
    html = response_1.text
    print(response_1.status_code)
    soup = BeautifulSoup(html, 'lxml')
    divList = soup.findAll('div', class_='content')
    for div in divList:
        text = div.find('span').text.strip()
        result += text
        result += '\n\n'
        print('==' + text)
        print('*' * 50)
# res_file = open('duanzi.txt', 'w',encoding='utf-8')
# res_file.write(result)
# res_file.close()
with open('duanzi.txt', 'w', encoding='utf-8') as f:
    f.write(result)
