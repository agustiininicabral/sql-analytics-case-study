SELECT c.segment,
       ROUND(SUM(oi.qty*(oi.unit_price-oi.unit_cost)),2) AS margin
FROM orders o
JOIN customers c ON c.customer_id=o.customer_id
JOIN order_items oi ON oi.order_id=o.order_id
GROUP BY 1
ORDER BY margin DESC;
