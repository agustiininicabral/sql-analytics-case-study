SELECT ROUND(AVG(order_rev),2) AS avg_order_value
FROM (
  SELECT o.order_id, SUM(oi.qty*oi.unit_price) AS order_rev
  FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
  GROUP BY 1
);
