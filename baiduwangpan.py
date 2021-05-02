import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Chrome/90.0.4430.93'
}
url2 = 'http://wjsou.com/s2.jsp?q=%E5%AE%89%E7%A1%95%E4%BF%A1%E6%81%AF'


def getData(key):
    i = 0
    while True:
        i = i + 1
        url1 = 'http://wjsou.com/apiother.jsp?from=0&q=' + key + '&page=' + str(i)
        html = requests.get(url1, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        h4list = soup.find_all('a', class_='fname')
        print()
        if len(h4list) == 0:
            print('爬到了第' + str(i) + '页，数据终止.')
            i = 0
            break
        for h4b in h4list:
            fileTile = h4b.text
            fileid = h4b['id']
            fileurl = h4b['href']
            print(fileurl)
            print(fileTile)


getData('安硕信息')
