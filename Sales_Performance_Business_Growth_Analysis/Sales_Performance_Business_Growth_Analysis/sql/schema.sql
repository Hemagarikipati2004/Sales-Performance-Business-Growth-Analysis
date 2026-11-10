-- SQLite schema reference. The ETL script creates the table automatically.
CREATE TABLE IF NOT EXISTS sales (
  order_id TEXT PRIMARY KEY,
  order_date TEXT NOT NULL,
  customer_id TEXT,
  customer_segment TEXT,
  region TEXT,
  city TEXT,
  sales_channel TEXT,
  category TEXT,
  product TEXT,
  quantity REAL,
  unit_price REAL,
  discount REAL,
  revenue REAL,
  cost REAL,
  profit REAL,
  order_year INTEGER,
  order_month INTEGER,
  month_name TEXT,
  year_month TEXT
);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date);
CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region);
CREATE INDEX IF NOT EXISTS idx_sales_category ON sales(category);
