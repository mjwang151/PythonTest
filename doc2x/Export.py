import requests
import json

url = 'https://v2.doc2x.noedgeai.com/api/v2/convert/parse/result?uid=01931f99-fb28-7238-9c64-7ff7a680234a'
headers = {'Authorization': 'Bearer sk-ocbp7s5girz0ue03jm3pxnenrgnaexwj'}

response = requests.get(url, headers=headers)
print(response.text)

# 确保响应是有效的，且是JSON格式
if response.status_code == 200:
    try:
        data = response.json()  # 直接解析为JSON
        url = data['data']['url']
        print("URL:", url)
        # 第二次请求，通过获取的URL下载文件
        response = requests.get(url)
        if response.status_code == 200:
            with open('downloaded_file3.zip', 'wb') as f:
                f.write(response.content)
                print("File downloaded successfully.")
        else:
            print(f"Failed to download file, status code: {response.status_code}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")

