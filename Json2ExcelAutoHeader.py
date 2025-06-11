# file: Json2ExcelAutoHeader.py

import pandas as pd
import json
# 输入文件格式为 [{},{}]这种格式
with open('/Volumes/S1/tmp/a.txt', 'r', encoding='utf-8') as f:
    records_data = json.load(f)

excel_file = '/Volumes/S1/tmp/output.xlsx'

if not isinstance(records_data, list) or not records_data:
    raise ValueError("records_output.json 应为非空的列表格式 list[dict]")

# 保证字段顺序来自第一条记录
headers = list(records_data[0].keys())
df = pd.DataFrame(records_data, columns=headers)

# 写入 Excel：只生成一个 Sheet，使用默认表头
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name="Sheet1", index=False)

print(f"Excel 文件已保存到: {excel_file}")
input("Press Enter to exit...")