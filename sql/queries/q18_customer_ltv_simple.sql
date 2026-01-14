SELECT c.customer_name,
       ROUND(SUM(oi.qty*oi.unit_price),2) AS ltv
FROM customers c
JOIN orders o ON o.customer_id=c.customer_id
JOIN order_items oi ON oi.order_id=o.order_id
GROUP BY 1
ORDER BY ltv DESC
LIMIT 20;
