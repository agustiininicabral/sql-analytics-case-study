WITH order_prod AS (
  SELECT order_id, product_id
  FROM order_items
  GROUP BY 1,2
),
pairs AS (
  SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS together_orders
  FROM order_prod a
  JOIN order_prod b ON a.order_id=b.order_id AND a.product_id < b.product_id
  GROUP BY 1,2
)
SELECT p1.product_name AS product_1,
       p2.product_name AS product_2,
       together_orders
FROM pairs
JOIN products p1 ON p1.product_id=pairs.p1
JOIN products p2 ON p2.product_id=pairs.p2
ORDER BY together_orders DESC
LIMIT 10;
