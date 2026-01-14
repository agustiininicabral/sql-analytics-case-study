WITH c AS (
  SELECT customer_id, COUNT(*) AS orders_cnt
  FROM orders GROUP BY 1
)
SELECT orders_cnt, COUNT(*) AS customers
FROM c
GROUP BY 1
ORDER BY orders_cnt;
