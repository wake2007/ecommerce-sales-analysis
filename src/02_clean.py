from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"
df = pd.read_excel(DATA_PATH)
print("原始行数:", len(df))
df_clean = df.drop_duplicates()
print("删重复后:", len(df_clean))
# 剔除取消单/坏账单：只保留纯数字的订单号
df_clean = df_clean[df_clean["InvoiceNo"].astype(str).str.isdigit()]
print(f"剔除取消单/坏账单后：{len(df_clean)}")
# 剔除数量<=0
df_clean = df_clean[df_clean["Quantity"] > 0]
print(f"剔除数量<=0后：{len(df_clean)}")
# 剔除单价<=0
df_clean = df_clean[df_clean["UnitPrice"] > 0]
print(f"剔除单价<=0后：{len(df_clean)}")
# 派生新列：每行销售额 = 数量 * 单价
df_clean["Amount"] = df_clean["Quantity"] * df_clean["UnitPrice"]
print(f"总销售额：{df_clean['Amount'].sum():.2f}")
print(f"订单数：{df_clean['InvoiceNo'].nunique()}")
# 保存清洗结果
OUT_DIR = BASE_DIR / "data" / "processed"  # 找到（创建）路径
OUT_DIR.mkdir(parents=True,
              exist_ok=True)  # 在磁盘中创建文件夹（mkdir=make directory）,parents=True:上级目录缺失时一起创建（别人 clone 项目后 data/processed 可能都不存在）,exist_ok=True:目录已存在时安静跳过（否则第二次运行会抛 FileExistsError）
OUT_PATH = OUT_DIR / "online_retail_clean.csv"  # 算出要保存的完整文件路径（目录+文件名）。注意：这行只是算路径，不碰磁盘
df_clean.to_csv(OUT_PATH, index=False)  # 把清洗后的表写成CSV。index=Fales 防止把行号0，1，2...写进文件
print("已保存：", OUT_PATH)
