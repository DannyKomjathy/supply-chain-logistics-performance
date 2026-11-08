# Tableau Dashboard Spec — Warehouse & Inbound Logistics Performance

**Audience:** a hiring manager / operations lead. Lead with the decision, not the chart count.

## Page 1 — Executive view (the decision page)
- KPIs, large and top-left: On-time delivery rate, Late orders, Avg delivery gap (days), Completed orders, Avg cycle time
- On-time rate by shipping mode (bar, sorted worst first)
- On-time rate by region (map or bar)
- Monthly orders + 3-month forecast (line)
- Filters: year, region, shipping mode, product category
- Calculated fields:
  - `Delivery Gap = [Days_for_shipping_real] - [Days_for_shipment_scheduled]`
  - `Is Late = [Delivery Gap] > 0`
  - `On-Time Rate = SUM(IF NOT [Is Late] THEN 1 ELSE 0 END) / COUNT([Order_Item_Id])`

## Page 2 — Where time is lost
- Cycle time by shipping mode (avg actual vs. avg scheduled, side-by-side)
- Delivery-gap distribution (histogram, -2 to +5 days)
- Late drivers: late rate and late orders by mode, region, and product category
- A short text box: "The driver to fix first is ___ because ___" — fill in after the analysis

## Page 3 — Inbound context
- Port of LA / Long Beach monthly TEU (loaded imports, loaded exports, empties)
- BTS FAF5: freight weight / value by mode, national context only
- Monthly DataCo order volume, with the forecast
- Note on the page: inbound data is monthly / national — it explains direction, it does not prove order-level causation

## Design notes
- One question per page, one headline finding per page
- No more than 3 filters per page
- Put the metric definition in a tooltip / footnote on every KPI
- Export the memo (`memo/one-page-memo.md`) as the companion to the dashboard — the dashboard alone is not the deliverable
