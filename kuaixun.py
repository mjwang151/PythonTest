import time
from selenium import webdriver
import os
import re
#引入chromedriver.exe
chromedriver = "C:/Users/59851/AppData/Local/Programs/Python/Python38/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

#设置浏览器需要打开的url
url = "https://www.jin10.com/"
# 使用for循环不停的刷新页面，也可以每隔一段时间刷新页面
for i in range(1,100000):
    browser.get(url)
    result= browser.page_source
    gold_price = ""
    gold_price_change = ""
    try:
        gold_price = re.findall('<div id="XAUUSD_B" class="jin-price_value" style=".*?">(.*?)</div>',result)[0]
        gold_price_change = re.findall('<div id="XAUUSD_P" class="jin-price_value" style=".*?">(.*?)</div>',result)[0]
    except:
        gold_pric = "------"
        gold_price_change = "------"

    print(gold_price)
    print(gold_price_change)
    time.sleep(1)
