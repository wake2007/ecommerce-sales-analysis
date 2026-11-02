from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "online_retail_clean.csv"
print(DATA_PATH)
df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"])
print(df)
print(f"总销售额：{df['Amount'].sum():,.2f}")
print(f"订单数：{df['InvoiceNo'].nunique():,}")
print(f"客户数：{df["CustomerID"].nunique():,}")
print(f"商品数：{df["StockCode"].nunique():,}")
print(f"客单价：{df['Amount'].sum()/df['InvoiceNo'].nunique():.2f}")
# 客单价 = 总销售额 ÷ 订单数（分母是订单数，不是行数；一单平均含 26.3 种商品）