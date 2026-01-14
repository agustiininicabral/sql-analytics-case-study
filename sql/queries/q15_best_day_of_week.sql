WITH d AS (
  SELECT o.order_id, o.order_date,
         strftime('%w', o.order_date) AS dow,
         SUM(oi.qty*oi.unit_price) AS revenue
  FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
  GROUP BY 1,2,3
)
SELECT dow, ROUND(SUM(revenue),2) AS revenue
FROM d
GROUP BY 1
ORDER BY revenue DESC;
