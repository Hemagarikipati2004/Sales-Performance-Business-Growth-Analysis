from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_clean.csv"

def load_data():
    if not DATA.exists():
        raise FileNotFoundError("Run: python src/clean_data.py")
    return pd.read_csv(DATA, parse_dates=["order_date"])

def kpi_summary(df):
    revenue = df["revenue"].sum()
    profit = df["profit"].sum()
    orders = df["order_id"].nunique()
    return {
        "revenue": revenue,
        "profit": profit,
        "margin_pct": (profit / revenue * 100) if revenue else 0,
        "orders": orders,
        "units": df["quantity"].sum(),
        "aov": revenue / orders if orders else 0,
    }

def monthly_trend(df):
    return (df.groupby("year_month", as_index=False)
              .agg(revenue=("revenue","sum"), profit=("profit","sum"),
                   orders=("order_id","nunique"))
              .sort_values("year_month"))

def top_products(df, n=10):
    return (df.groupby(["product","category"], as_index=False)
              .agg(revenue=("revenue","sum"), profit=("profit","sum"),
                   units=("quantity","sum"))
              .sort_values("revenue", ascending=False).head(n))

if __name__ == "__main__":
    data = load_data()
    print("KPI SUMMARY")
    for key, value in kpi_summary(data).items():
        print(f"{key}: {value:,.2f}")
    print("\nTOP PRODUCTS")
    print(top_products(data).to_string(index=False))
