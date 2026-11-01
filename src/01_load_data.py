from pathlib import Path  # Path把路径从一张纸条变成一把工具
import pandas as pd

# resolve():变成绝对路径
# parent[]:从脚本位置往上取几级 例如：从 01_load_data.py 找 parents[1]，方向是 脚本 → src → 项目根
# 脚本 = .py文件
BASE_DIR = Path(__file__).resolve().parents[1]  # 把【我这个脚本自己的位置】转成绝对路径，往上退两级，得到一个目录路径；
# 把它装进一个叫BASE_DIR的盒子，BASE_DIR-->根的目录
print(BASE_DIR)
DATA_PATH = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"  # 把数据的路径放进DATA_PATH的盒子里面
print(DATA_PATH)

df = pd.read_excel(DATA_PATH)
print(df.shape, end='\n\n')
print(df.dtypes, end='\n\n')
print(df.isna().sum(), end='\n\n')  # 统计每一列中为空的总数
print(df.head(), end='\n\n')
print(df.duplicated().sum(), end='\n\n')  # 统计重复的行的总和
# duplicated()作用：按行比较：凡是跟前面某行完全一样的，就标 True；第一次出现的标 False。它只打标记，一个字节都不删。
print(df[df.duplicated()].head(), end='\n\n')  # 列出重复的行
print((df["Quantity"] < 0).sum(), end='\n\n')
print((df['Quantity'] == 0).sum(), end='\n\n')
print((df["UnizhetPrice"] <= 0).sum(), end='\n\n')
print((df["InvoiceNo"].astype(str).str.startswith("C").sum()))
