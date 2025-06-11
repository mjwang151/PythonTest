import json

# 假设 data 是字典对象
data = {
    "code": "success",
    "data": {
        "status": "success",
        "progress": 100,
        "result": {
            "version": "v2",
            "pages": [
                {"url": "", "page_idx": 0, "page_width": 1654, "page_height": 2339, "md": "公司"},
                {"url": "", "page_idx": 1, "page_width": 1654, "page_height": 2339, "md": "## 重要提"},
                {"url": "", "page_idx": 2, "page_width": 1654, "page_height": 2339, "md": "\n\n## 九、是否存在半数以上"},
                {"url": "", "page_idx": 3, "page_width": 1654, "page_height": 2339, "md": "\n\n## 目录\n\n第一节 释义 ."},
                {"url": "", "page_idx": 4, "page_width": 1654, "page_height": 2339, "md": "## 第一节 释"}
            ]
        }
    }
}


pages = data['data']['result']['pages']
md_values = []
# 遍历 pages 列表
for page in pages:
    md_values.append(page['md'])

result = ''.join(md_values)
print(result)
