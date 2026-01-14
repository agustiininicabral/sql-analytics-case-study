WITH cohort AS (
  SELECT customer_id, substr(MIN(order_date),1,7) AS cohort_ym
  FROM orders
  GROUP BY 1
),
activity AS (
  SELECT o.customer_id, substr(o.order_date,1,7) AS act_ym
  FROM orders o
  GROUP BY 1,2
),
joined AS (
  SELECT c.cohort_ym, a.act_ym,
         (CAST(substr(a.act_ym,1,4) AS INT)*12 + CAST(substr(a.act_ym,6,2) AS INT)) -
         (CAST(substr(c.cohort_ym,1,4) AS INT)*12 + CAST(substr(c.cohort_ym,6,2) AS INT)) AS month_n,
         COUNT(DISTINCT a.customer_id) AS active_customers
  FROM cohort c JOIN activity a ON a.customer_id=c.customer_id
  GROUP BY 1,2,3
),
cohort_size AS (
  SELECT cohort_ym, COUNT(DISTINCT customer_id) AS cohort_customers
  FROM cohort GROUP BY 1
)
SELECT j.cohort_ym, j.month_n, j.active_customers,
       cs.cohort_customers,
       ROUND(j.active_customers*100.0/NULLIF(cs.cohort_customers,0),2) AS retention_pct
FROM joined j
JOIN cohort_size cs ON cs.cohort_ym=j.cohort_ym
WHERE j.month_n BETWEEN 0 AND 6
ORDER BY j.cohort_ym, j.month_n;
