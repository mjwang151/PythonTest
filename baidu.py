import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# 打开浏览器
browser = webdriver.Chrome()

try:
	# 访问网页
	browser.get("http://www.baidu.com")

	# 获取所有节点并打印
	result = browser.execute_script("return document.documentElement.innerText")
	print(result)

	# 通过ID选择器查找元素
	search_box = browser.find_element(By.ID, 'kw')

	# 输入搜索内容
	search_box.send_keys('长城')

	# 获取提交节点并点击
	search_button = browser.find_element(By.ID, 'su')
	search_button.click()

	# 等待搜索结果加载完成
	browser.implicitly_wait(5)

	# 获取搜索结果
	result = browser.find_element(By.ID, 'content_left').text
	print(result)

finally:
	# browser.quit()
	print('end')
