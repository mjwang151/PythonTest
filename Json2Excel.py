import pandas as pd
import json

# 读取 JSON 文件
json_file = 'S:/tmp/output.json'  # 替换为你的 JSON 文件路径
with open(json_file, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 创建一个 Pandas Excel writer 使用 xlsxwriter 引擎
excel_file = 'S:/tmp/output.xlsx'  # 替换为你想保存的 Excel 文件路径
with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    for sheet_name, records in json_data.items():
        df = pd.DataFrame(records)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Excel 文件已保存为 {excel_file}")