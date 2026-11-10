# Sales Performance & Business Growth Analysis

An end-to-end advanced data analytics project using Python, SQL, Streamlit and Power BI.

## Project goals
- Measure revenue, profit, margin, order volume and average order value.
- Identify monthly growth patterns and high-performing regions/products.
- Compare customer segments and sales channels.
- Prepare clean, reusable data for a Power BI report.
- Turn analysis into actionable business recommendations.

## Folder structure
```
Sales_Performance_Business_Growth_Analysis/
├── app.py
├── requirements.txt
├── data/
│   ├── sales_raw.csv
│   └── sales_clean.csv          # created by the ETL script
├── src/
│   ├── clean_data.py
│   └── analysis.py
├── sql/
│   ├── schema.sql
│   └── business_queries.sql
├── powerbi/
│   └── POWER_BI_GUIDE.md
├── outputs/
│   └── (generated reports)
└── README.md
```

## 1. Requirements
- Python 3.10 or later
- VS Code
- Internet connection for installing Python packages
- Optional: Power BI Desktop (Windows) for the Power BI report

## 2. Setup on Windows (VS Code)
Open the extracted project folder in VS Code. In Terminal > New Terminal, run:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the same terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Confirm that the terminal prompt begins with `(.venv)`.

## 3. Clean the dataset
Run this from the main project folder:
```powershell
python src/clean_data.py
```
This creates `data/sales_clean.csv`, a SQLite database at `data/sales.db`, and a short quality report at `outputs/data_quality_report.txt`.

## 4. Launch the interactive dashboard
```powershell
streamlit run app.py
```
The browser should open automatically. If it does not, open the local URL printed in the terminal (usually http://localhost:8501).

## 5. SQL analysis
The ETL script creates the SQLite database and loads the cleaned `sales` table.
To run the supplied SQL:
- Open `data/sales.db` with DB Browser for SQLite, or
- Use the Python SQLite command line / a database client.
- Run `sql/business_queries.sql` after the table exists.

## 6. Power BI
Follow `powerbi/POWER_BI_GUIDE.md`. Import `data/sales_clean.csv` or connect to `data/sales.db`. The clean CSV is the easiest option.

## 7. Key metric definitions
- Total Revenue = SUM(revenue)
- Total Profit = SUM(profit)
- Profit Margin % = Total Profit / Total Revenue * 100
- Total Orders = DISTINCTCOUNT(order_id)
- Units Sold = SUM(quantity)
- Average Order Value = Total Revenue / Total Orders
- Revenue Growth % = (Current Period Revenue - Previous Period Revenue) / Previous Period Revenue * 100
- Target Achievement % = Actual Revenue / Revenue Target * 100

The dashboard uses an illustrative monthly revenue target of 105% of the prior-year same-month revenue, with a fallback target for the first year. Treat this as a demonstration assumption, not a real company target.

## 8. Suggested portfolio description
**Sales Performance & Business Growth Analysis | Python, SQL, Power BI**
Built an end-to-end sales analytics solution to clean and analyze 6,000 order records, track revenue and profitability KPIs, compare regional and product performance, and explore business growth trends through an interactive dashboard. Used Python and Pandas for ETL, SQLite for SQL analysis, Streamlit for interactive reporting, and prepared a Power BI-ready dataset.

## Notes
- The included data is synthetic and created for learning/demo purposes; it is not real customer or company data.
- This is a data analytics project, not a machine-learning prediction project.
