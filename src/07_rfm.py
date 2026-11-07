from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed" / "online_retail_clean.csv"
df = pd.read_csv(DATA_DIR, parse_dates=["InvoiceDate"])
df = df.dropna(subset=["CustomerID"])  # 删除游客客户
df["CustomerID"] = df["CustomerID"].astype(int)  # 编号转整型
# 参考日期：把数据最后一天当作”现在“
analysis_date = df["InvoiceDate"].max()
# R：每个客户最近一次购买距离“现在”多少天
# 每个客户"最后一次下单"的时间（按客户分组，取日期最大值 = 最晚一天）
last_purchase = df.groupby("CustomerID")["InvoiceDate"].max()  # 类型：series
# r = 用"分析日期"减去每个客户最后下单日，得到"多久没买了"的天数
# 注意：analysis_date 是单个日期，会广播到整列逐个相减；
#       .dt.days 把 Timedelta（0 days）转成纯数字（0）
r = (analysis_date - last_purchase).dt.days
# F：订单数
f = df.groupby("CustomerID")["InvoiceNo"].nunique()
# M：消费总额
m = df.groupby("CustomerID")["Amount"].sum()
# 合成表
rfm = pd.DataFrame({"R": r, "F": f, "M": m})
print(rfm.head())
print(rfm.describe())
# 打分：高于中位数 = 1（好），低于 = 0（差）
rfm["R_score"] = (rfm["R"] <= rfm["R"].median()).astype(int)  # R 越小越好
rfm["F_score"] = (rfm["F"] >= rfm["F"].median()).astype(int)  # F 越大越好
rfm["M_score"] = (rfm["M"] >= rfm["M"].median()).astype(int)  # M 越大越好
# 组合成分层标签，如“111”=R高 F高 M高
rfm["segment"] = (rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str))
print(rfm["segment"].value_counts().sort_index())  # 统计 8 类客户各有多少人，并按标签顺序（000→111）排列，方便对照命名表
print('\n', rfm.head())
# 把8个标签映射成有业务含义的名字
SEGMENT_NAMES = {"111": "重要价值客户",
                 "101": "重要发展客户",
                 "011": "重要保持客户",
                 "001": "重要挽留客户",
                 "110": "一般价值客户",
                 "100": "新客户",
                 "010": "一般保持客户",
                 "000": "流失客户"}  # 类型：字典

rfm["segment_name"] = rfm["segment"].map(SEGMENT_NAMES)  # .map(字典)——把一列的值“翻译”成别的值（查字典翻译），注意：原列不被覆盖，“翻译“生成新列segment_name
print('\n', rfm.head())
# 统计每类客户的人数，人均消费，总收入
summary = rfm.groupby("segment_name").agg(人数=("M", "count"),
                                          人均消费=("M", "mean"),
                                          总收入=("M",
                                                  "sum"), )  # summary以"segment_name"分组，生成新的df表；尾随逗号可有可无，但建议加：让“多行列表/参数”容易增删，且 Git diff 更干净。它是 Python 界的通行风格。
summary = summary.sort_values("总收入", ascending=False)  # 降序
print('\n', summary.round(0))  # .round(n),保留n位小数，不改变数据类型，所以.round（0）会呈现4338.0
# 新增两列：人数占比、收入占比（部分 ÷ 整体，由代码自动算，不手写）
summary["人数占比"] = summary["人数"] / summary["人数"].sum()
summary["收入占比"] = summary["总收入"] / summary["总收入"].sum()

print('\n',summary.round(2))
