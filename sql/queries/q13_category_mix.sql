SELECT p.category,
       ROUND(SUM(oi.qty*oi.unit_price),2) AS revenue
FROM order_items oi JOIN products p ON p.product_id=oi.product_id
GROUP BY 1
ORDER BY revenue DESC;
