import pandas as pd
import json

# 读取 JSON 文件
with open('S:/tmp/fields_output.json', 'r', encoding='utf-8') as fields_file:
    fields_data = json.load(fields_file)

with open('S:/tmp/records_output.json', 'r', encoding='utf-8') as records_file:
    records_data = json.load(records_file)
# 初始化 Excel 写入对象
excel_file = 'S:/tmp/output.xlsx'  # 替换为你想保存的 Excel 文件路径
with pd.ExcelWriter(excel_file) as writer:
    for sheet_name, records in records_data.items():
        # 获取字段名和注释
        fields = fields_data[sheet_name]
        headers = list(fields.keys())
        comments = list(fields.values())
        # 创建 DataFrame
        df = pd.DataFrame(records, columns=headers)  # 确保 DataFrame 有列名
        # 在 DataFrame 的顶部插入字段名和注释
        df.loc[-2] = comments  # 添加注释行
        df.index = df.index + 2  # 调整索引
        df.sort_index(inplace=True)  # 排序索引
        df.loc[-1] = headers  # 添加字段名行
        df.index = df.index + 1  # 调整索引
        df.sort_index(inplace=True)  # 排序索引
        # 写入到 Excel 中
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

print(f"Excel 文件已保存到: {excel_file}")
input("Press Enter to exit...")