import os

import requests
import json
from datetime import datetime

# 接口地址
url = "http://172.20.2.2/hubdeeplinkv3/external/api/record/add"
export_url = "http://10.2.13.108:3000/export?recordNo=#recordNo&queryName=test&baseUrl=http://172.20.2.2"
# export_url = "http://172.20.3.97:3000/export?recordNo=#recordNo&queryName=test&baseUrl=http://172.20.2.2"
webhook_key = "0ff836c6-980b-48fe-b2db-52956b678a3f"

# 请求体参数
payload = {
    "documentName": "大模型限流报告",
    "reSerialNo": "1981548441662128130",
    "userId":"mjwang",
    "belongOrgId": "1",
    "belongTenantId": "1"

}
# 请求头
headers = {
    "Content-Type": "application/json"
}
try:
    # 发送 POST 请求
    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
    # 输出结果
    print("状态码：", response.status_code)
    print("返回内容：", response.text)
    # 转为 JSON 对象
    data = response.json()
    # 提取 result 字段
    result = data.get("message", {}).get("result")
    print("返回 result 字段值：", result)
    final_export_url = export_url.replace('#recordNo',result)

    # 生成当前日期（格式：yyyyMMdd）
    current_date = datetime.now().strftime("%Y%m%d")

    # 拼接文件名
    file_name = f"大模型限流报告{current_date}.docx"
    try:
        print(f"正在下载文件：{final_export_url}")
        file_resp = requests.get(final_export_url, timeout=30)
        file_resp.raise_for_status()

        with open(file_name, "wb") as f:
            f.write(file_resp.content)

        print(f"文件下载完成：{file_name}")
    except Exception as e:
        print("文件下载失败：", e)
        exit(1)

    # === Step 3: 上传文件到企业微信群机器人 ===
    upload_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_key}&type=file"

    try:
        with open(file_name, "rb") as f:
            files = {"file": (os.path.basename(file_name), f, "application/octet-stream")}
            upload_resp = requests.post(upload_url, files=files, timeout=10)
            upload_data = upload_resp.json()
            print("上传返回：", upload_data)
            if upload_data.get("errcode") != 0:
                print("上传失败：", upload_data)
                exit(1)

            media_id = upload_data.get("media_id")
            print("上传成功，media_id =", media_id)
    except Exception as e:
        print("文件上传失败：", e)
        exit(1)

    # === Step 4: 发送文件消息 ===
    send_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    msg_payload = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }
    try:
        send_resp = requests.post(send_url, json=msg_payload, timeout=10)
        print("发送结果：", send_resp.text)
    except Exception as e:
        print("发送文件消息失败：", e)

    # === Step 5: 删除本地文件 ===
    try:
        os.remove(file_name)
        print(f"已删除临时文件：{file_name}")
    except Exception as e:
        print(f"删除文件失败：{e}")
except requests.exceptions.RequestException as e:
    print("请求失败：", e)