SELECT p.category, p.product_name,
       ROUND(SUM(oi.qty*oi.unit_price),2) AS revenue
FROM order_items oi
JOIN products p ON p.product_id=oi.product_id
GROUP BY 1,2
ORDER BY revenue DESC
LIMIT 10;
