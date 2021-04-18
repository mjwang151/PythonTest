from selenium import webdriver

# 打开浏览器
browser = webdriver.Chrome()
# 访问网页
browser.get("http://www.baidu.com")
#获取所有节点
result = browser.find_element_by_id('wrapper').text
print(result)
#获取输入框节点
browser.find_element_by_id('kw').send_keys('长城')
#获取提交节点
browser.find_element_by_id('su').click()

