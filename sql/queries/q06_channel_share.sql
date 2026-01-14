WITH r AS (
  SELECT o.channel,
         SUM(oi.qty*oi.unit_price) AS revenue
  FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
  GROUP BY 1
),
t AS (SELECT SUM(revenue) AS total FROM r)
SELECT r.channel,
       ROUND(r.revenue,2) AS revenue,
       ROUND(r.revenue*100.0/NULLIF(t.total,0),2) AS share_pct
FROM r CROSS JOIN t
ORDER BY revenue DESC;
