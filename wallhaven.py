import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Chrome/90.0.4430.93'
}

def get_img(url, name):
    res = requests.get(url)
    if res.status_code == 200:
        with open('images/'+name+'.png', 'wb') as f:
            f.write(res.content)
        print(name+'.png下载成功')
    else:
        print(name+'.png下载失败')
#解析详情页
def parse_img_detail(wb_data):
    soupOne = BeautifulSoup(wb_data, 'lxml')
    url_name = soupOne.find('img', id='wallpaper')['src']
    name_name = soupOne.find('img', id='wallpaper')['data-wallpaper-id']
    print('图片url：'+url_name)
    return url_name,name_name

url = 'https://wallhaven.cc/latest?page=1'
response_1 = requests.get(url, headers=headers)
html = response_1.text
print(response_1.status_code)
soup = BeautifulSoup(html, 'lxml')
allImg = soup.find('section', class_='thumb-listing-page').find('ul').find_all('li')
for img in allImg:
    curl = img.find('a')['href']
    print(curl)
    wb_data = requests.get(curl, headers=headers).text
    url_name,name_name = parse_img_detail(wb_data)
    get_img(url_name, name_name)




