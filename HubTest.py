import requests
import json

url = "https://app.amarsoft.com/hubservicetest/api/gateway"

headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

data = {
    "transcode": "R11103V3",
    "secretKey": "******",  # 替换为安硕提供的真实密钥
    "account": "****",# 替换为安硕提供的account
    "params": {
        "name": "传递出四点北京分公司",
        "nameType": "1"
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

print("状态码:", response.status_code)
print("响应内容:", response.text)
