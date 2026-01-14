WITH oc AS (
  SELECT customer_id, COUNT(*) AS orders_cnt
  FROM orders GROUP BY 1
),
t AS (SELECT COUNT(*) AS total_customers FROM oc),
r AS (SELECT COUNT(*) AS repeat_customers FROM oc WHERE orders_cnt > 1)
SELECT
  t.total_customers,
  r.repeat_customers,
  ROUND(r.repeat_customers*100.0/NULLIF(t.total_customers,0),2) AS repeat_rate_pct
FROM t, r;
