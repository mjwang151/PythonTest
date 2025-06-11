import pandas as pd

# 读取 Excel 文件
df = pd.read_excel("/Volumes/S1/tmp/chain3.xlsx")

# 获取相同 `entname`, `mapped_chain_name`, `mapped_node_name` 组的最大和最小 level
grouped = df.groupby(["entname", "mapped_chain_name", "mapped_node_name"])["level"]
min_level = grouped.transform("min")
max_level = grouped.transform("max")

# 过滤出介于最大和最小之间的 level
filtered_df = df[(df["level"] > min_level) & (df["level"] < max_level)]

# 保存结果
filtered_df.to_excel("/Volumes/S1/tmp/filtered_data.xlsx", index=False)