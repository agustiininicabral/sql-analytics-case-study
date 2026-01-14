WITH m AS (
  SELECT substr(o.order_date,1,7) AS ym,
         SUM(oi.qty*oi.unit_price) AS revenue
  FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
  GROUP BY 1
)
SELECT ym,
       ROUND(revenue,2) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY ym),2) AS running_total
FROM m
ORDER BY ym;
