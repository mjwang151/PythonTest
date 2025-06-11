import pandas as pd
import json

# 读取 Excel 文件
excel_file = 'S:/tmp2/B301V2数据样例.xlsx'  # 替换为你的 Excel 文件路径

# 只读取一个指定的 sheet，例如 'Sheet1'
sheet_name = 'Sheet1'  # 替换为你想要读取的 sheet 名称
df = pd.read_excel(excel_file, sheet_name=sheet_name, header=0)  # 第一行作为字段名

# 将所有值转换为字符串，替换 NaN 为 ''
df = df.fillna('').astype(str)  # 替换 NaN 为 '' 并转换为字符串

# 将每一行数据转换为 JSON 对象，并逐行写入文件
output_file = 'S:/tmp2/records_output.json'
with open(output_file, 'w', encoding='utf-8') as records_file:
    for record in df.to_dict(orient='records'):
        json.dump(record, records_file, ensure_ascii=False)
        records_file.write('\n')  # 每个 JSON 对象占一行

print(f"数据已成功导出到 {output_file}")
