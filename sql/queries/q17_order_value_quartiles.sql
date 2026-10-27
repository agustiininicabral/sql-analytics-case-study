WITH ov AS (
  SELECT o.order_id, SUM(oi.qty*oi.unit_price) AS order_value
  FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
  GROUP BY 1
),
r AS (
  SELECT order_value,
         NTILE(4) OVER (ORDER BY order_value) AS quartile
  FROM ov
)
SELECT quartile,
       ROUND(MIN(order_value),2) AS min_value,
       ROUND(MAX(order_value),2) AS max_value,
       COUNT(*) AS orders
FROM r
GROUP BY 1
ORDER BY quartile;
