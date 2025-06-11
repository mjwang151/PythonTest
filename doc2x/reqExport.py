import requests
import json

url = "https://v2.doc2x.noedgeai.com/api/v2/convert/parse"
headers = {
    "Authorization": "Bearer sk-ocbp7s5girz0ue03jm3pxnenrgnaexwj",
    "Content-Type": "application/json",
}

data = {
    "uid": "01931f99-fb28-7238-9c64-7ff7a680234a",
    "to": "md",
    "formula_mode": "normal",
    "filename": "my_markdown.md",
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.text)