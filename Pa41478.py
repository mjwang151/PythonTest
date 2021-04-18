import time

from selenium import webdriver

movie = input("请输入电影名称:")
# 打开浏览器
dirver = webdriver.Chrome()
# 访问网页
dirver.get("http://www.41478.net")
time.sleep(1)
# 获取输入框节点
dirver.switch_to.frame(dirver.find_element_by_xpath("//iframe[@id='lineFrame']"))
dirver.switch_to.frame("zzapi")
dirver.find_element_by_id('wd').send_keys(movie)
dirver.find_elements_by_xpath("//button[last()]")[0].click()
