-- 04 — Inventory metrics — ONLY with an inventory file
-- DataCo has no inventory-on-hand snapshot, so these metrics cannot
-- be computed from DataCo alone. Use this query only if you supply
-- data/inventory.csv as a table `inventory` with:
--   product_id, on_hand_units, avg_daily_demand, lead_time_days
--
-- Inventory turns = annual demand / average inventory
-- Days of supply = on_hand_units / avg_daily_demand
-- Stockout risk (simple flag) = days_of_supply < lead_time_days

SELECT
  product_id,
  on_hand_units,
  avg_daily_demand,
  lead_time_days,
  on_hand_units / NULLIF(avg_daily_demand, 0) AS days_of_supply,
  CASE WHEN on_hand_units / NULLIF(avg_daily_demand, 0) < lead_time_days
       THEN 'AT RISK' ELSE 'OK' END AS stockout_flag
FROM inventory
ORDER BY days_of_supply ASC;
