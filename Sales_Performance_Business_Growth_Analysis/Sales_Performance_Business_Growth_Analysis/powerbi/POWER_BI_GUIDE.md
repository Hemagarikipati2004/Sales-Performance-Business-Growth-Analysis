# Power BI implementation guide

## Load data
1. Open Power BI Desktop.
2. Select **Get data > Text/CSV**.
3. Import `data/sales_clean.csv`.
4. Select **Transform Data** to verify data types:
   - `order_date`: Date
   - `quantity`: Whole number / Decimal number
   - `unit_price`, `discount`, `revenue`, `cost`, `profit`: Decimal number
   - IDs and category fields: Text
5. Select **Close & Apply**.

## Recommended report pages

### Page 1 — Executive Overview
- KPI cards: Total Revenue, Total Profit, Profit Margin %, Orders, Units Sold, Average Order Value.
- Line chart: Revenue and Profit by `year_month`.
- Bar chart: Revenue by Region.
- Donut chart: Revenue by Category.
- Slicers: Order Date, Region, Category, Sales Channel.

### Page 2 — Product & Category
- Bar chart: Top 10 Products by Revenue.
- Matrix: Category > Product with Revenue, Profit, Units Sold and Margin.
- Scatter chart: Revenue vs Profit by Product.
- Slicers: Category and Region.

### Page 3 — Customer & Channel
- Column chart: Revenue by Customer Segment.
- Bar chart: Orders by Sales Channel.
- Table: Customer Segment, Customers, Orders, Revenue per Customer.

### Page 4 — Regional Growth
- Bar chart: Revenue and Profit by Region.
- Matrix: Region > City.
- Line chart: Monthly Revenue by Region.
- Slicers: Date and Region.

## DAX measures
Create these measures after loading the table named `sales`:

```dax
Total Revenue = SUM(sales[revenue])

Total Profit = SUM(sales[profit])

Total Orders = DISTINCTCOUNT(sales[order_id])

Units Sold = SUM(sales[quantity])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Revenue Previous Year =
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR('Calendar'[Date])
)

Revenue YoY Growth % =
DIVIDE(
    [Total Revenue] - [Revenue Previous Year],
    [Revenue Previous Year],
    0
)

Total Cost = SUM(sales[cost])

Discounted Revenue = SUM(sales[revenue])
```

## Calendar table
Create a calendar table using:

```dax
Calendar =
ADDCOLUMNS(
    CALENDAR(MIN(sales[order_date]), MAX(sales[order_date])),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month", FORMAT([Date], "MMM"),
    "Year Month", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & FORMAT([Date], "Q")
)
```

Set `Calendar` as the Date table using its `Date` column. Create a one-to-many relationship from `Calendar[Date]` to `sales[order_date]`. Sort `Calendar[Month]` by `Calendar[Month Number]`; use `Year Month` for chronological monthly visuals.

## Design suggestions
- Canvas: 16:9.
- Theme: dark navy background, white text, teal/blue accent.
- Keep KPI cards on the top row.
- Use consistent currency formatting (₹) and avoid overcrowding.
- Add clear chart titles and dynamic slicers.
- Add a footer: “Sales Performance & Business Growth Analysis | Demo dataset”.

Note: Power BI Desktop is a separate application. This project provides the clean data and DAX/report specification; the `.pbix` report must be assembled and saved in Power BI Desktop.
