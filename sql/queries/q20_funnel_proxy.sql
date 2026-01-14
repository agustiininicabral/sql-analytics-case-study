-- Proxy funnel: customers created -> customers ordered -> customers repeat
WITH total AS (SELECT COUNT(*) AS customers_created FROM customers),
ordered AS (SELECT COUNT(DISTINCT customer_id) AS customers_ordered FROM orders),
repeat AS (
  SELECT COUNT(*) AS customers_repeat
  FROM (SELECT customer_id FROM orders GROUP BY 1 HAVING COUNT(*) > 1)
)
SELECT
  total.customers_created,
  ordered.customers_ordered,
  repeat.customers_repeat,
  ROUND(ordered.customers_ordered*100.0/NULLIF(total.customers_created,0),2) AS ordered_pct,
  ROUND(repeat.customers_repeat*100.0/NULLIF(total.customers_created,0),2) AS repeat_pct
FROM total, ordered, repeat;
