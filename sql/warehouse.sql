-- 1) Clean fact table (analytics-ready)
CREATE TABLE IF NOT EXISTS fact_sales (
    order_id      BIGINT,
    order_date    DATE,
    product       TEXT,
    quantity      INT,
    price         NUMERIC,
    country       TEXT,
    load_date     TEXT,
    revenue       NUMERIC
);

-- 2) Rebuild fact table from raw (simple approach for portfolio)
TRUNCATE TABLE fact_sales;

INSERT INTO fact_sales (order_id, order_date, product, quantity, price, country, load_date, revenue)
SELECT
    order_id,
    order_date::date,
    product,
    quantity::int,
    price::numeric,
    country,
    load_date,
    (quantity::numeric * price::numeric) AS revenue
FROM sales_raw;

-- 3) Views recruiters like (SQL analytics)

-- Revenue by country (latest load_date)
CREATE OR REPLACE VIEW v_revenue_by_country AS
SELECT
    country,
    SUM(revenue) AS total_revenue
FROM fact_sales
GROUP BY country
ORDER BY total_revenue DESC;

-- Top 5 products by revenue
CREATE OR REPLACE VIEW v_top_products AS
SELECT
    product,
    SUM(revenue) AS total_revenue
FROM fact_sales
GROUP BY product
ORDER BY total_revenue DESC
LIMIT 5;

-- 7-day moving average revenue per country (window function)
CREATE OR REPLACE VIEW v_country_daily_revenue_ma7 AS
SELECT
    country,
    order_date,
    SUM(revenue) AS daily_revenue,
    AVG(SUM(revenue)) OVER (
        PARTITION BY country
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS daily_revenue_ma7
FROM fact_sales
GROUP BY country, order_date
ORDER BY country, order_date;
