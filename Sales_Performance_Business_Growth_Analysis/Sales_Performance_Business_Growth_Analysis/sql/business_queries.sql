-- 1. Executive KPI summary
SELECT ROUND(SUM(revenue),2) AS total_revenue,
       ROUND(SUM(profit),2) AS total_profit,
       ROUND(100.0*SUM(profit)/NULLIF(SUM(revenue),0),2) AS profit_margin_pct,
       COUNT(DISTINCT order_id) AS total_orders,
       ROUND(SUM(quantity),0) AS units_sold,
       ROUND(SUM(revenue)/NULLIF(COUNT(DISTINCT order_id),0),2) AS average_order_value
FROM sales;

-- 2. Monthly revenue and profit trend
SELECT year_month, ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(profit),2) AS profit, COUNT(DISTINCT order_id) AS orders
FROM sales GROUP BY year_month ORDER BY year_month;

-- 3. Regional performance ranking
SELECT region, ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit,
       RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM sales GROUP BY region ORDER BY revenue DESC;

-- 4. Category profitability
SELECT category, ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit,
       ROUND(100.0*SUM(profit)/NULLIF(SUM(revenue),0),2) AS margin_pct
FROM sales GROUP BY category ORDER BY profit DESC;

-- 5. Top 10 products
SELECT product, category, SUM(quantity) AS units,
       ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit
FROM sales GROUP BY product, category ORDER BY revenue DESC LIMIT 10;

-- 6. Customer segment value
SELECT customer_segment, COUNT(DISTINCT customer_id) AS customers,
       COUNT(DISTINCT order_id) AS orders, ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(revenue)/NULLIF(COUNT(DISTINCT customer_id),0),2) AS revenue_per_customer
FROM sales GROUP BY customer_segment ORDER BY revenue DESC;

-- 7. Channel performance
SELECT sales_channel, COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit
FROM sales GROUP BY sales_channel ORDER BY revenue DESC;

-- 8. Year-over-year monthly growth (SQLite window function)
WITH monthly AS (
  SELECT year_month, SUM(revenue) AS revenue
  FROM sales GROUP BY year_month
), comparison AS (
  SELECT year_month, revenue,
         LAG(revenue,12) OVER (ORDER BY year_month) AS prior_year_revenue
  FROM monthly
)
SELECT year_month, ROUND(revenue,2) AS revenue,
       ROUND(prior_year_revenue,2) AS prior_year_revenue,
       ROUND(100.0*(revenue-prior_year_revenue)/NULLIF(prior_year_revenue,0),2) AS yoy_growth_pct
FROM comparison ORDER BY year_month;

-- 9. Discount impact
SELECT CASE WHEN discount=0 THEN 'No discount'
            WHEN discount<=0.05 THEN '0-5%'
            WHEN discount<=0.10 THEN '5-10%'
            WHEN discount<=0.15 THEN '10-15%'
            ELSE '15-20%' END AS discount_band,
       COUNT(*) AS orders, ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(profit),2) AS profit,
       ROUND(100.0*SUM(profit)/NULLIF(SUM(revenue),0),2) AS margin_pct
FROM sales GROUP BY discount_band ORDER BY MIN(discount);

-- 10. City-level opportunity scan
SELECT region, city, ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(profit),2) AS profit, COUNT(DISTINCT order_id) AS orders
FROM sales GROUP BY region, city ORDER BY revenue DESC;
