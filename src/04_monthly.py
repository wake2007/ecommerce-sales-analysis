from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "online_retail_clean.csv"
df = pd.read_csv(DATA_PATH, parse_dates=['InvoiceDate'])
# 从日期里提取”年-月“，存成新列
df["Month"] = df["InvoiceDate"].dt.strftime("%Y-%m")
# 按月份分组求和，再按月份排序
monthly = df.groupby("Month")["Amount"].sum().sort_index()
print(monthly)
plt.figure(figsize=(10, 5))  # 新建画布，10*5英寸
plt.plot(monthly.index, monthly.values, marker="o")  # 画折线，每个点加个原点
plt.title("Monthly Sales Trend (GBP)")  # 标题
plt.xlabel("Month")  # 横轴名字
plt.ylabel("Sales (GBP)")  # 纵轴名字
plt.xticks(rotation=45)  # 横轴标签，倾斜45°放置
plt.grid(alpha=0.3)  # 加网格线，alpha是透明度（0.3淡）
plt.tight_layout()  # 自动调整边距，防止标签被裁掉
FIG_DIR = BASE_DIR / "reports" / "figures"  # 图像存储路径
FIG_DIR.mkdir(parents=True, exist_ok=True)
plt.savefig(FIG_DIR / "monthly_sales_trend.png", dpi=150)  # 将图像存入磁盘
plt.show()
