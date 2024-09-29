import pandas as pd
import json
# 读取 Excel 文件
excel_file = 'S:/tmp/模板.xlsx'  # 替换为你的 Excel 文件路径
sheets = pd.read_excel(excel_file, sheet_name=None, header=0)  # 第一行作为字段名，第二行忽略

# 将每个 sheet 转换为 JSON 格式，直接为 Python 列表
json_data = {
    sheet_name: df.fillna('').iloc[1:].to_dict(orient='records')
    for sheet_name, df in sheets.items()
}

# 输出 JSON 数据
print(json.dumps(json_data, ensure_ascii=False, indent=2))

# 如果需要保存到文件，可以使用：
with open('S:/tmp/output.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=2)