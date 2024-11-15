import requests
from bs4 import BeautifulSoup


def options(data):
    headers = {
        'User-Agent': 'Chrome/90.0.4430.93'
    }
    url = 'https://book.douban.com/chart?subcat=F&icn=index-topchart-fiction'
    response_1 = requests.get(url, headers=headers)
    html = response_1.text
    print(response_1.status_code)
    soup = BeautifulSoup(html, 'lxml')
    soup.find('a', class_='fleft')
    allA = soup.findAll('a', class_='fleft')
    for axT in allA:
        print(axT.text)
        print(axT['href'])
    divList = soup.findAll('div', class_='media__body')
    for divN in divList:
        name = divN.find('a', class_='fleft').text
        author = divN.find('p', class_='subject-abstract').text
        score = divN.find('span', class_='font-small').text
        print(name, author, score)


options(1)
