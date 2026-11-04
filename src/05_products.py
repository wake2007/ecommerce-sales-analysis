from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed" / "online_retail_clean.csv"
df = pd.read_csv(DATA_DIR, parse_dates=["InvoiceDate"])
# 按商品编码分组，分别算销售额和销量，各取前10
is_product = df["StockCode"].astype(str).str.match(r"^\d{5}[A-Za-z]{0,3}$")
# 判断每个编码是不是"真实商品"：5 位数字 + 最多 3 个字母（颜色/尺寸变体）
# 结果是一列 True/False（True = 是商品），用于剔除 POST/DOT/M 等记账用特殊码
df_product = df[is_product]
# 只保留 True 的行（真实商品），剔除邮费/手工录入/礼品券等非商品记录
top_amount = df_product.groupby("StockCode")["Amount"].sum().nlargest(10)
top_qty = df_product.groupby("StockCode")["Quantity"].sum().nlargest(10)
print("=== 销售额 Top 10 ===")
print(top_amount)
print("\n=== 销量 Top 10 ===")
print(top_qty)
#三个聚合，都按StockCode分组
amount=df_product.groupby("StockCode")["Amount"].sum()
qty=df_product.groupby("StockCode")["Quantity"].sum()
name=df_product.groupby("StockCode")["Description"].first()
#三个Series按索引（StockCode）自动对齐，合成一张表
result=pd.DataFrame({"销售额":amount,"销量":qty,"商品名":name})
result["均价"]=result["销售额"]/result["销量"]
top=result.sort_values("销售额",ascending=False).head(10)
# 按销售额降序排序（ascending=False 表示从大到小），取前 10 行，.sort_values("某列")	按某一列的值，ascending=True（默认）= 升序，小 → 大
print("=== Top 10 ===")
print(top)