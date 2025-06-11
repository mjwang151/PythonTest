import pandas as pd
import json
from openpyxl import Workbook
from openpyxl.styles import Border, Side

# 读取 JSON 文件
with open('S:/tmp/国民经济行业分类_2017_.json', 'r', encoding='utf-8') as json_file:
    records_data = json.load(json_file)

# 创建 Excel 文件
excel_file = 'S:/tmp/国民经济行业分类_2017_.xlsx'  # 替换为你想保存的 Excel 文件路径
wb = Workbook()
ws = wb.active
ws.title = 'Data'


# 添加表头
headers = [
    'ind_grade1_code', 'ind_grade1_name',
    'ind_grade2_code', 'ind_grade2_name',
    'ind_grade3_code', 'ind_grade3_name',
    'ind_grade4_code', 'ind_grade4_name'
]
ws.append(headers)

# 定义一个函数来递归处理数据
def process_record(record, ind_grade1_code="", ind_grade1_name="", ind_grade2_code="", ind_grade2_name="", ind_grade3_code="", ind_grade3_name="", ind_grade4_code="", ind_grade4_name="", level=1):
    current_code = record.get('code', '')
    current_name = record.get('name', '')

    if level == 1:
        ind_grade1_code = current_code
        ind_grade1_name = current_name
    elif level == 2:
        ind_grade2_code = current_code
        ind_grade2_name = current_name
    elif level == 3:
        ind_grade3_code = current_code
        ind_grade3_name = current_name
    elif level == 4:
        ind_grade4_code = current_code
        ind_grade4_name = current_name

    # 添加到工作表
    ws.append([
        ind_grade1_code, ind_grade1_name,
        ind_grade2_code, ind_grade2_name,
        ind_grade3_code if level > 2 else '', ind_grade3_name if level > 2 else '',
        ind_grade4_code if level > 3 else '', ind_grade4_name if level > 3 else ''
    ])

    # 处理下一层
    if 'children' in record and record['children']:
        for child in record['children']:
            process_record(child, ind_grade1_code, ind_grade1_name, ind_grade2_code, ind_grade2_name, ind_grade3_code, ind_grade3_name, ind_grade4_code, ind_grade4_name, level + 1)
    else:
        # 如果没有子节点，仍然写入当前节点的信息
        ws.append([
            ind_grade1_code, ind_grade1_name,
            ind_grade2_code, ind_grade2_name,
            '', ''  # 第三层和第四层为空
        ])

# 处理根层数据
for record in records_data:
    process_record(record)

# 保存 Excel 文件
wb.save(excel_file)

print(f"Excel 文件已保存到: {excel_file}")