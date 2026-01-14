SELECT
  ROUND(SUM(qty*unit_price),2) AS revenue,
  ROUND(SUM(qty*unit_cost),2) AS cost,
  ROUND(SUM(qty*(unit_price-unit_cost)),2) AS margin
FROM order_items;
