from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed" / "online_retail_clean.csv"
df = pd.read_csv(DATA_DIR, parse_dates=["InvoiceDate"])
# 客服分析必须有ID，先剔除没有ID的（游客单）
df = df.dropna(subset=["CustomerID"])
# 按客户聚合三个指标
amount = df.groupby("CustomerID")["Amount"].sum()  # 每个客户消费总额
order = df.groupby("CustomerID")["InvoiceNo"].nunique()  # 订单数
qty = df.groupby("CustomerID")["Quantity"].sum()  # 购买件数
cust = pd.DataFrame({"消费总额": amount, "订单数": order, "购买件数": qty})
print(f"客户总数：{len(cust)}")
print(cust.describe())
print(f"\n消费总额的平均：{cust["消费总额"].mean():.2f}\n消费总额的中位数：{cust["消费总额"].median():.2f}")
# 按消费额从高到低排
top_customers = cust["消费总额"].sort_values(ascending=False)
# 前20%客户有多少人
n_top = int(len(top_customers) * 0.2)
# 前20%客户的收入/全部收入
top_share = top_customers[0:n_top].sum() / top_customers.sum()
print(f"前 20% 客户（{n_top} 人）贡献了 {top_share:.1%} 的收入")
repeat =  (cust["订单数"]>=2).sum() #复购率
print(f"复购客户：{repeat}人，占比{repeat/len(cust):.1%}")