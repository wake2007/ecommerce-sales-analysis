-- 1. 总体指标（对应 Pandas 03_overview.py）
SELECT
    ROUND(SUM(amount), 2) AS 总销售额,
    COUNT(DISTINCT invoice_no) AS 订单数,
    COUNT(DISTINCT customer_id) AS 客户数,
    COUNT(DISTINCT stock_code) AS 商品数,
    ROUND(SUM(amount) / COUNT(DISTINCT invoice_no), 2) AS 客单价
FROM order_items;

-- 2. 月度销售趋势（对应 Pandas 04_monthly.py）
SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS month, SUM(amount) AS 月销售额
FROM order_items
GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
ORDER BY month;

-- 3. 畅销商品 Top10（对应 Pandas 05_products.py，已剔除特殊编码）
SELECT stock_code, SUM(amount) AS total
FROM order_items
WHERE stock_code REGEXP '^[0-9]{5}[A-Za-z]{0,3}$'
GROUP BY stock_code
ORDER BY total DESC
LIMIT 10;