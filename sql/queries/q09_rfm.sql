WITH base AS (
  SELECT o.customer_id,
         MAX(o.order_date) AS last_order,
         COUNT(DISTINCT o.order_id) AS frequency,
         SUM(oi.qty*oi.unit_price) AS monetary
  FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
  GROUP BY 1
),
recency AS (
  SELECT customer_id,
         (julianday((SELECT MAX(order_date) FROM orders)) - julianday(last_order)) AS recency_days,
         frequency,
         monetary
  FROM base
)
SELECT customer_id,
       ROUND(recency_days,1) AS recency_days,
       frequency,
       ROUND(monetary,2) AS monetary
FROM recency
ORDER BY monetary DESC
LIMIT 50;
