import json
import time
import requests as rq

base_url = "https://v2.doc2x.noedgeai.com"
secret = "sk-ocbp7s5girz0ue03jm3pxnenrgnaexwj"

def preupload():
    url = f"{base_url}/api/v2/parse/preupload"
    headers = {
        "Authorization": f"Bearer {secret}"
    }
    res = rq.post(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data["code"] == "success":
            return data["data"]
        else:
            raise Exception(f"get preupload url failed: {data}")
    else:
        raise Exception(f"get preupload url failed: {res.text}")

def put_file(path: str, url: str):
    with open(path, "rb") as f:
        res = rq.put(url, data=f) # body为文件二进制流
        if res.status_code != 200:
            raise Exception(f"put file failed: {res.text}")

def get_status(uid: str):
    url = f"{base_url}/api/v2/parse/status?uid={uid}"
    headers = {
        "Authorization": f"Bearer {secret}"
    }
    res = rq.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data["code"] == "success":
            return data["data"]
        else:
            raise Exception(f"get status failed: {data}")
    else:
        raise Exception(f"get status failed: {res.text}")

upload_data = preupload()
print(upload_data)
url = upload_data["url"]
uid = upload_data["uid"]

put_file("s:/tmp2/ceshi2.pdf", url)
print(uid)
# while True:
#     status_data = get_status(uid)
#     print(status_data)
#     if status_data["status"] == "success":
#         result = status_data["result"]
#         with open("result.json", "w") as f:
#             json.dump(result, f)
#         break
#     elif status_data["status"] == "failed":
#         detail = status_data["detail"]
#         raise Exception(f"parse failed: {detail}")
#     elif status_data["status"] == "processing":
#         # processing
#         progress = status_data["progress"]
#         print(f"progress: {progress}")
#         time.sleep(3)
