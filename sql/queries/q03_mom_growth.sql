WITH m AS (
  SELECT substr(o.order_date,1,7) AS ym,
         SUM(oi.qty*oi.unit_price) AS revenue
  FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
  GROUP BY 1
),
g AS (
  SELECT ym,
         revenue,
         LAG(revenue) OVER (ORDER BY ym) AS prev_revenue
  FROM m
)
SELECT ym,
       ROUND(revenue,2) AS revenue,
       ROUND(prev_revenue,2) AS prev_revenue,
       ROUND((revenue - prev_revenue),2) AS mom_abs,
       ROUND( (revenue - prev_revenue) * 100.0 / NULLIF(prev_revenue,0), 2) AS mom_pct
FROM g
ORDER BY ym;
