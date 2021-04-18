import time

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
# 打开浏览器
browser = webdriver.Chrome(options=chrome_options)

# 访问网页
browser.get("https://pc.xuexi.cn/points/login.html?ref=https%3A%2F%2Fwww.xuexi.cn%2F")
time.sleep(10)
titles = browser.find_elements_by_class_name('text')
x = 1
for title in titles:
    if x > 20:
        print('已经点击了十篇文章了，程序结束')
        break
    title.click()
    print('第' + str(x) + '次查看网站，此次查看网站内容为：【' + title.text + '】')
    time.sleep(65)
    x += 1






