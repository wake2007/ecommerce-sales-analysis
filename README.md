# 基于 Python 与 MySQL 的电商销售数据分析

使用 UCI Online Retail 数据集，完成数据清洗、统计分析、可视化、MySQL 存储与 SQL 分析，
并输出客户 RFM 分层等业务结论。

## 数据来源

- UCI Machine Learning Repository, Dataset 352
- https://archive.ics.uci.edu/dataset/352/online+retail
- 规模：541,909 行 × 8 列；时间 2010-12-01 至 2011-12-09
- 粒度：一行 = 一笔订单中的一种商品

## 技术栈

- Python 3.12、Pandas、NumPy、Matplotlib
- MySQL 5.7、PyMySQL

## 项目结构

```
├── src/            # 分析脚本（01~08）
├── sql/            # SQL 查询
├── data/           # raw 原始数据 / processed 清洗结果
├── docs/           # 数据说明、清洗规则、分析结论
├── reports/        # 图表
└── requirements.txt
```

## 如何复现

1. 安装依赖：`pip install -r requirements.txt`
2. 下载数据到 `data/raw/`（见"数据来源"）
3. 按顺序运行 `src/` 下的脚本：01 → 02 → ... → 08
4. 在 MySQL 建库建表（见 `sql/` 与 `docs/`），导入数据
5. 运行 `sql/分析查询.sql` 复现分析

## 核心结论

1. 总销售额 £10,631,048.74，客单价 £532.64（批发客户占比大）
2. 11 月为全年峰值，符合圣诞采购季
3. 商品分三层：高价品撑利润、中价品走量、低价品引流
4. 前 20% 客户贡献 74.7% 收入（二八定律）
5. RFM 分层：重要价值客户（32.9%）贡献 76% 收入