-- 02 — Order cycle time, broken into stages where the data allows
-- DateOrders is the order date; shipping date is in the source as a
-- separate date field in some loads — adapt the column names to your load.
-- This query uses the day-count fields that are present in every load:
--   Days_for_shipping_real = actual days to ship/deliver
--   Days_for_shipment_scheduled = scheduled days
-- For a full stage split (order-to-ship + ship-to-deliver), join the
-- order date and shipping date once they are parsed as dates, and
-- compute: ship_date - order_date, and delivery_date - ship_date.

SELECT
  Shipping_Mode,
  COUNT(*) AS orders,
  AVG(Days_for_shipping_real) AS avg_actual_days,
  AVG(Days_for_shipment_scheduled) AS avg_scheduled_days,
  AVG(Days_for_shipping_real - Days_for_shipment_scheduled) AS avg_gap_days,
  MIN(Days_for_shipping_real) AS min_actual_days,
  MAX(Days_for_shipping_real) AS max_actual_days
FROM dataco
WHERE Order_Status = 'COMPLETE'
GROUP BY Shipping_Mode
ORDER BY avg_gap_days DESC;
