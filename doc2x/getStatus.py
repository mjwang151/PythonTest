import requests
import json

url = 'https://v2.doc2x.noedgeai.com/api/v2/parse/status?uid=01931f99-fb28-7238-9c64-7ff7a680234a'
headers = {'Authorization': 'Bearer sk-3gf9xueo5fgemhhi8sm8gbk35vw8wnra'}
response = requests.get(url, headers=headers)
print(response.text)
# 确保响应是有效的，且是JSON格式
# if response.status_code == 200:
#     try:
# 		data = response.json()
# 		pages = data['data']['result']['pages']
# 		md_values = []
# 		# 遍历 pages 列表
# 		for page in pages:
# 		    md_values.append(page['md'])
# 		result = ''.join(md_values)
# 		print(result)
#     except json.JSONDecodeError:
#         print("Failed to decode JSON from the response.")