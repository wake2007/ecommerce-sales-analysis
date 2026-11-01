from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"
df = pd.read_excel(DATA_PATH)
print("原始行数:", len(df))
df_clean = df.drop_duplicates()
print("删重复后:", len(df_clean))
#剔除取消单/坏帐单：只保留纯数字的订单号
df_clean=df_clean[df_clean["InvoiceNo"].astype(str).str.isdigit()]
print(len(df_clean))
#剔除数量<=0
df_clean=df_clean[df_clean["Quantity"]>0]
print(len(df_clean))
#剔除单价<=0
df_clean=df_clean[df_clean["UnitPrice"]>0]
print(len(df_clean))