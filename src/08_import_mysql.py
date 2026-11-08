from pathlib import Path
import pandas as pd
import pymysql
from db_config import DB_CONFIG

BASE_PATH = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_PATH / "data" / "processed" / "online_retail_clean.csv"
df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"])
# CustomerID转成“可控整数”，避免出现12346.0这种浮点数
df["CustomerID"] = df['CustomerID'].astype("Int64")
# 关键：pandas的NaN要转成None，MySQL才认（None=NULL）
df = df.astype(object).where(pd.notna(df), None)
# 转成元组列表，列顺序必须和INSERT语句一致
records = df[["InvoiceNo", "StockCode", "Description", "Quantity",
              "InvoiceDate", "UnitPrice", "CustomerID", "Country", "Amount", ]].values.tolist()
# .values —— 扔掉列名和行号，只剩纯数据,.tolist() —— 转成 Python 列表,df[[...]]：按你手写的先后顺序取列，顺序完全由你控制
conn = pymysql.connect(**DB_CONFIG)  # 连接数据库：**DB_CONFIG 把配置字典展开成参数（相当于 host="localhost", user="root", ...）
cur = conn.cursor()  # 创建游标：之后所有 execute(sql) / fetchall() 都靠它执行
sql = """INSERT INTO order_items(invoice_no,stock_code,description,quantity,invoice_date,unit_price,customer_id,country,amount)
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
# 分批插入，每批5000行，打印进度
BATCH = 5000  # 每批插 5000 行，避免 52 万行一次性插入撑爆内存 / 超过包大小上限
for i in range(0, len(records), BATCH):  # 分批循环：i 从 0 开始每次跳 5000，作为每批的起点
    cur.executemany(sql, records[i:i + BATCH])  # 切出这一批（最多 5000 行）批量插入
    conn.commit()  # 每批插完立刻提交，真正写进数据库（不 commit 可能不保存）
    print(f"已导入{min(i + BATCH, len(records))}/{len(records)}行")  # 打印进度；min() 防止最后一轮 i+BATCH 超过总行数
conn.close()  # 循环全部结束后，关闭数据库连接
print("导入完成")
