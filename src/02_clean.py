from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"
df = pd.read_excel(DATA_PATH)
print("原始行数:", len(df))
df_clean = df.drop_duplicates()
print("删重复后:", len(df_clean))
