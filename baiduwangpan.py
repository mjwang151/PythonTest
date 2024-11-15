import requests
from bs4 import BeautifulSoup
import pymysql
import re
import uuid

proxies = {
    'url': 'http://121.230.91.67:8022',
    'url': 'http://119.120.20.24:9999'
}

headers = {
    'User-Agent': 'Chrome/90.0.4430.93'
}
url2 = 'http://wjsou.com/s2.jsp?q=%E5%AE%89%E7%A1%95%E4%BF%A1%E6%81%AF'
url3 = 'https://www.pan131.com/yun/安硕信息/?pn=1'
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='sys', charset='utf8')
cur = conn.cursor()


def getData(key):
    i = 0
    while True:
        i = i + 1
        print('爬取数据【' + key + '】第【' + str(i) + '】页')
        url1 = 'http://wjsou.com/apiother.jsp?from=0&q=' + key + '&page=' + str(i)
        html = requests.get(url1, headers=headers, proxies=proxies)
        soup = BeautifulSoup(html.text, 'lxml')
        h4list = soup.find_all('a', class_='fname')
        print()
        if len(h4list) == 0:
            print('爬到了第' + str(i) + '页，数据终止.')
            i = 0
            break
        for h4b in h4list:
            fileTile = h4b.text
            fileurl = h4b['href']
            fileid = re.findall(r"&shareid=(.*)", fileurl)
            id = ''
            if len(fileid) > 0:
                id = fileid[0]
            else:
                fileid = re.findall(r"shareid=(.*)&", fileurl)
                if len(fileid) > 0:
                    id = fileid[0]
            # create table baidu_file(serialno varchar(100)   primary key,reqname varchar(200), id varchar(100),fileurl varchar(3000),fileTitle varchar(4000))
            sql = 'replace into baidu_file (`serialno`,`reqname`,`id`,`fileurl`,`fileTitle`) values (%s,%s,%s,%s,%s)'
            params = []
            params.append(uuid.uuid1())
            params.append(key)
            params.append(id)
            params.append(fileurl)
            params.append(fileTile)

            cur.execute(sql, params)
            conn.commit()


def getKeyFromTxt():
    with open('keywords.txt', 'r', encoding='UTF-8') as f:
        textNew = f.readlines()
        return textNew


textNew = getKeyFromTxt()
for line in textNew:
    getData(line)

cur.close()
conn.close()
