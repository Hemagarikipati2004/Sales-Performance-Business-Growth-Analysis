from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "sales_raw.csv"
CLEAN = ROOT / "data" / "sales_clean.csv"
DB = ROOT / "data" / "sales.db"
REPORT = ROOT / "outputs" / "data_quality_report.txt"

def clean_sales():
    df = pd.read_csv(RAW)
    original_rows = len(df)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    numeric = ["quantity", "unit_price", "discount", "revenue", "cost", "profit"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["city"] = df["city"].fillna("Unknown")
    df["sales_channel"] = df["sales_channel"].fillna("Unknown")
    df["quantity"] = df["quantity"].fillna(df["quantity"].median())
    df["discount"] = df["discount"].fillna(0).clip(0, 1)
    df = df.dropna(subset=["order_id", "order_date", "revenue", "profit"])
    df = df.drop_duplicates(subset=["order_id"])
    df["quantity"] = df["quantity"].clip(lower=0)
    df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
    df["profit"] = (df["revenue"] - df["cost"]).round(2)
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.strftime("%b")
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df.to_csv(CLEAN, index=False, date_format="%Y-%m-%d")

    with sqlite3.connect(DB) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_category ON sales(category)")

    report = [
        "SALES DATA QUALITY REPORT",
        "=========================",
        f"Rows before cleaning: {original_rows}",
        f"Rows after cleaning: {len(df)}",
        f"Duplicate order IDs remaining: {df['order_id'].duplicated().sum()}",
        f"Missing values remaining: {int(df.isna().sum().sum())}",
        f"Date range: {df['order_date'].min().date()} to {df['order_date'].max().date()}",
        f"Cleaned CSV: {CLEAN}",
        f"SQLite database: {DB}",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    clean_sales()
