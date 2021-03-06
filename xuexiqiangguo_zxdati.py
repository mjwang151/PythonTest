import os
import time

from selenium import webdriver

# taskkill /F /im chromedriver.exe

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
# 打开浏览器
browser = webdriver.Chrome(options=chrome_options)

# 访问网页
browser.get("https://pc.xuexi.cn/points/login.html?ref=https%3A%2F%2Fwww.xuexi.cn%2F")
browser.maximize_window()
js = "var q=document.documentElement.scrollTop=900"
browser.execute_script(js)

time.sleep(10)
titles = browser.find_elements_by_class_name('linkItem')[1].click()
time.sleep(1)
# 定位當前頁面
browser.switch_to.window(browser.window_handles[1])
browser.find_elements_by_class_name('text-title')[1].click()
browser.switch_to.window(browser.window_handles[2])
meiRiTitle = browser.find_elements_by_class_name('title')
for title in meiRiTitle:
    if title.text == '专项答题':
        title.click()
        break
time.sleep(3)
zxTitle = browser.find_elements_by_class_name('item-title')
zxButton = browser.find_elements_by_class_name('ant-btn')
i = 1
for axT in zxTitle:
    print('开始答题：' + axT.text)
    zxButton[i].click()
    for i in range(1, 11):
        print('开始回答第' + str(i) + '道题目。')
        time.sleep(2)
        tiMuType = browser.find_elements_by_class_name('q-header')[0].text[0:3]
        # 点击显示提示信息
        browser.find_elements_by_class_name('tips')[0].click()
        time.sleep(2)
        tips_tmp = []
        tips = browser.find_elements_by_class_name('line-feed')[0].find_elements_by_xpath("//font")
        for ji in range(len(browser.find_elements_by_class_name('line-feed')[0].find_elements_by_xpath("//font"))):
            print(str(ji) + ':' + str(
                len(browser.find_elements_by_class_name('line-feed')[0].find_elements_by_xpath("//font"))))
            tips_tmp.append(
                browser.find_elements_by_class_name('line-feed')[0].find_elements_by_xpath("//font")[ji].text)
        print('缓存到的提示信息:' + str(tips_tmp))
        tips_msg = browser.find_elements_by_class_name('line-feed')[0].text
        time.sleep(2)
        # 点击隐藏提示信息
        browser.find_elements_by_class_name('tips')[0].click()
        time.sleep(2)
        if tiMuType == '多选题':
            print('此题为多选题:')
            ansCount = 0
            xXian = browser.find_elements_by_class_name('q-answer')
            for xx in xXian:
                for tip in tips_tmp:
                    if tip == xx.text[3:]:
                        print('多选题答案是:' + xx.text + '，提示为：' + tip)
                        xx.click()
                        ansCount += 1
            if ansCount == 0:
                browser.find_elements_by_class_name('q-answer')[0].click()
        elif tiMuType == '单选题':
            print('此题为单选题:')
            ansCount = 0
            xXian = browser.find_elements_by_class_name('q-answer')
            for xx in xXian:
                for tip in tips_tmp:
                    if tip == '':
                        continue
                    if tip == xx.text[3:]:
                        print('单选题答案是:' + xx.text + '，提示为：' + tip)
                        xx.click()
                        ansCount += 1
                        break
            if ansCount == 0:
                browser.find_elements_by_class_name('q-answer')[0].click()
        else:
            print('此题为填空题:')
            xXian = browser.find_elements_by_class_name('blank')
            x = 0
            for xx in xXian:
                if len(tips_tmp) <= x:
                    xx.send_keys('不知道')
                else:
                    xx.send_keys(tips_tmp[x])
                x += 1
        print('答题结束，准备跳转...')
        browser.find_elements_by_class_name('ant-btn')[0].click()
        isYesVal = browser.find_elements_by_class_name('answer')
        if len(isYesVal) > 0:
            print('此题答错，正确答案为：' + browser.find_elements_by_class_name('answer')[0].text)
            browser.find_elements_by_class_name('ant-btn')[0].click()
    # browser.switch_to.window(browser.window_handles[2])
    i += 1
