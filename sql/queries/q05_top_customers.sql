SELECT c.segment, c.customer_name,
       ROUND(SUM(oi.qty*oi.unit_price),2) AS revenue
FROM orders o
JOIN customers c ON c.customer_id=o.customer_id
JOIN order_items oi ON oi.order_id=o.order_id
GROUP BY 1,2
ORDER BY revenue DESC
LIMIT 10;
