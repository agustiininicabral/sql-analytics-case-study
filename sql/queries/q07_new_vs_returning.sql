WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders GROUP BY 1
),
tag AS (
  SELECT o.order_id, o.customer_id, o.order_date,
         CASE WHEN o.order_date = f.first_date THEN 'new' ELSE 'returning' END AS cust_type
  FROM orders o JOIN first_order f ON f.customer_id=o.customer_id
)
SELECT substr(order_date,1,7) AS ym,
       cust_type,
       COUNT(DISTINCT order_id) AS orders
FROM tag
GROUP BY 1,2
ORDER BY 1,2;
