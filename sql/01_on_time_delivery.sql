-- 01 — On-time delivery rate by region and shipping mode
-- Table: dataco (DataCoSupplyChain.csv loaded as a table)
-- Columns used: Order_Item_Id, Order_Region, Shipping_Mode,
--   Days_for_shipping_real, Days_for_shipment_scheduled,
--   Delivery_Status, Order_Status
-- Note: exclude CANCELED / PENDING orders from the on-time rate unless
--   you explicitly want a cancellation view. Report the exclusion.

SELECT
  Order_Region,
  Shipping_Mode,
  COUNT(*) AS orders,
  SUM(CASE WHEN Days_for_shipping_real <= Days_for_shipment_scheduled THEN 1 ELSE 0 END) AS on_time_orders,
  1.0 * SUM(CASE WHEN Days_for_shipping_real <= Days_for_shipment_scheduled THEN 1 ELSE 0 END) / COUNT(*) AS on_time_rate,
  AVG(Days_for_shipping_real - Days_for_shipment_scheduled) AS avg_delivery_gap_days
FROM dataco
WHERE Order_Status = 'COMPLETE'
GROUP BY Order_Region, Shipping_Mode
ORDER BY on_time_rate ASC, orders DESC;
