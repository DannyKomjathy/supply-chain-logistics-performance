-- 03 — Late-delivery drivers
-- Compare on-time rate by mode, region, product category, and segment.
-- A driver is worth acting on only if it is both (a) large in orders
-- and (b) worse than the overall rate. Sort by late orders, not just rate.

-- By shipping mode
SELECT
  Shipping_Mode,
  COUNT(*) AS orders,
  SUM(CASE WHEN Days_for_shipping_real > Days_for_shipment_scheduled THEN 1 ELSE 0 END) AS late_orders,
  1.0 * SUM(CASE WHEN Days_for_shipping_real > Days_for_shipment_scheduled THEN 1 ELSE 0 END) / COUNT(*) AS late_rate
FROM dataco
WHERE Order_Status = 'COMPLETE'
GROUP BY Shipping_Mode
ORDER BY late_orders DESC;

-- By region (run separately, or UNION with a driver label)
-- By product category: replace Shipping_Mode with Product_Category
--   in the query above, and compare late_rate vs. the overall late rate.
