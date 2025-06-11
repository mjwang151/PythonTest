import pandas as pd
import json
# 读取 Excel 文件
excel_file = 'S:/tmp2/模板-1009(1).xlsx'  # 替换为你的 Excel 文件路径
sheets = pd.read_excel(excel_file, sheet_name=None, header=None)  # 第一行作为字段名，第二行忽略
# 将每个 sheet 转换为 JSON 格式
# 初始化数据结构
fields_data = {}
records_data = {}

# 将每个 sheet 的数据分别提取
for sheet_name, df in sheets.items():
    headers = df.iloc[0].tolist()  # 第一行字段名
    comments = df.iloc[1].tolist()  # 第二行中文注释
    df.columns = headers  # 将第一行设置为列名
    df = df[2:]  # 只保留数据部分
    # 将所有值转换为字符串，替换 NaN 为 ''
    df = df.astype(str).replace('nan', '')  # 先转换为字符串再替换
    records = df.to_dict(orient='records')  # 数据记录
    # 存储字段名和注释
    fields_data[sheet_name] = {header: (comment if pd.notna(comment) else '') for header, comment in zip(headers, comments)}
    # 存储记录
    records_data[sheet_name] = records


# 输出字段注释 JSON 数据
with open('S:/tmp2/fields_output.json', 'w', encoding='utf-8') as fields_file:
    json.dump(fields_data, fields_file, ensure_ascii=False, indent=2)

# 输出记录 JSON 数据
with open('S:/tmp2/records_output.json', 'w', encoding='utf-8') as records_file:
    json.dump(records_data, records_file, ensure_ascii=False, indent=2)

input("Press Enter to exit...")
