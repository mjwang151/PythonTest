import requests
import pymysql


def options(data):
    url = "https://app.amarsoft.com/hubservicetest/api/gateway"
    headers = {'content-type': "application/json;charset=utf-8", 'Accept': 'application/json'}
    res = requests.post(url=url, json=data, headers=headers)
    return res.text


data = {"transcode": "R11103V3", "userid": "11", "orGid": "EDS", "account": "EDS", "source": "EDS","params": {"name": "重庆雨汇食品有限公司","nametype":"1"}}
retData = options(data)
print(retData)
# 打开文件并写入
with open("S:/tmp2/hub.txt", "w") as file:
    file.write(retData)


