from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import time

# 设置Chrome WebDriver路径
chrome_driver_path = 'S:/soft/chromeDriver/chromedriver.exe'

# 创建Chrome WebDriver服务
service = Service(chrome_driver_path)

options = Options()
# options.add_argument('--headless')  # 无界面模式
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)

# 显式等待并点击登录按钮
try:
	# Step 1: Open Baidu homepage
	driver.get('https://www.baidu.com')
	time.sleep(2)  # Wait for the page to load
	driver.maximize_window()

	# Step 2: Print the page source

	# Step 3: Locate and click the login button
	login_button = WebDriverWait(driver, 3).until(
		EC.element_to_be_clickable((By.ID, 's-top-loginbtn'))
	)
	login_button.click()
	time.sleep(3)  # Wait for the login page to load
	print(driver.page_source)
	# Step 4: Locate and fill in the username and password fields, then submit the form
	username_field = driver.find_element(By.ID, 'TANGRAM__PSP_11__userName')  # Update with the correct locator
	password_field = driver.find_element(By.ID, 'TANGRAM__PSP_11__password')  # Update with the correct locator
	agree_button = WebDriverWait(driver, 3).until(
		EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_11__isAgree'))
	)
	agree_button.click()

	username_field.send_keys('15151552733')  # Replace with your Baidu username
	password_field.send_keys('wangminjie')  # Replace with your Baidu password

	# Step 5: Submit the login form
	password_field.send_keys(Keys.RETURN)
	time.sleep(5)  # Wait for the login process to complete

	# Step 6: Navigate to Wenxing Yiyan and ask a question
	driver.get('https://yiyan.baidu.com/')
	time.sleep(3)  # Wait for the page to load

	# Locate the question input field and submit a question
	question_input = driver.find_element(By.XPATH, "//textarea[@placeholder='Ask something']")
	question_input.send_keys('What is the weather like today?')
	question_input.send_keys(Keys.RETURN)

	# Wait for the response and print it out
	time.sleep(5)
	response = driver.find_element(By.XPATH, "//div[@class='response']").text
	print('Response:', response)
except Exception as e:
	print("出现错误：", e)
finally:
	# 关闭浏览器
	driver.quit()
