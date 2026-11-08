# Warehouse & Inbound Logistics Performance — Where Is Flow Losing Time or Money?

**Question:** Where is a distribution flow losing time or money, and what would you change?

**Short answer, computed 2026-11-08 from the data in this repo:** 57.3% of fulfilled orders were late (45,308 of 79,107). First Class was 100% late (scheduled 1 day, actual 2 days, every time) and Second Class was 79.5% late. Standard Class — the cheapest, longest promise — was the most reliable at 39.6% late. Fix the promise first. See `memo/one-page-memo.md` for the full findings.

This is a public-data, end-to-end supply chain analytics project for Business Operations / Supply Chain Operations roles. It is built to show a decision, not just a dashboard.

## Data — public only

No Tesla internal data is used. Everything here is public or simulated, and stated as such.

1. **DataCo Smart Supply Chain for Big Data Analysis — Kaggle**
   - 180,519 order line items, 53 columns, 2015–2018
   - Key fields: `Order_Item_Id`, `DateOrders`, `Days_for_shipping_real`, `Days_for_shipment_scheduled`, `Delivery_Status`, `Late_delivery_risk`, `Shipping_Mode` (Same Day, First Class, Second Class, Standard Class), `Order_Region`, `Order_Item_Quantity`, `Sales`, `Order_Item_Profit_Ratio`
   - Source: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
   - Download it yourself — the raw CSV is **not** committed here because of size. See `data/README.md`.

2. **Bureau of Transportation Statistics — Freight Analysis Framework, FAF5**
   - US freight flows by origin, destination, mode, and commodity. Weight, value, and ton-miles.
   - Use it for the inbound / national context, not as a substitute for order-level delivery data.
   - Source: https://www.bts.gov/faf/faf5

3. **Port of Los Angeles / Port of Long Beach — monthly container volumes (TEU)**
   - Monthly TEU by loaded imports, loaded exports, and empties. Use it as an inbound-volume signal for West Coast flow.
   - Get the latest monthly tables from each port's statistics page and record the download date in `data/README.md`.

## Metrics — definitions used in this repo

- **On-time delivery rate** = orders delivered on or before the scheduled date / completed orders. Late = `Days_for_shipping_real > Days_for_shipment_scheduled`, or `Delivery_Status = 'Late delivery'`. Report both definitions and check they agree.
- **Order cycle time** = shipping date − order date, in days. Break it into: order-to-ship + ship-to-deliver, where the data allows.
- **Delivery gap** = `Days_for_shipping_real − Days_for_shipment_scheduled`, in days. Positive = late.
- **Late-delivery drivers** = on-time rate and average gap by shipping mode, region, product category, and customer segment. Look for a driver that is both large and fixable — e.g. a mode with a scheduled time the operation cannot meet.
- **Order volume forecast** = simple 3-month moving average and linear trend on monthly completed orders, in `python/analysis.py`. This is a baseline, not a production forecast.
- **Inventory metrics — with a caveat:** DataCo has no inventory-on-hand snapshot, so inventory turns, days of supply, and stockout risk **cannot be computed directly from DataCo alone**. In this repo they are calculated only if you supply an inventory file (`data/inventory.csv`, columns: `product_id, on_hand_units, avg_daily_demand, lead_time_days`), or they are marked as simulated. Do not present simulated inventory numbers as observed.

Other operations metrics used in the memo: throughput (completed orders / day), cycle time, and on-time delivery. OEE is named in the memo only where a warehouse / equipment context is relevant — it is not computed from DataCo.

## How to run

```bash
# 1. Download DataCo and place it at:
#    data/DataCoSupplyChain.csv
# 2. Install dependencies
pip install -r python/requirements.txt

# 3. Run the analysis (SQL is in sql/, Python reproduces it and adds the forecast)
python python/analysis.py --input data/DataCoSupplyChain.csv --out outputs/

# Outputs: outputs/kpi_summary.csv, outputs/on_time_by_mode_region.csv,
#          outputs/cycle_time.csv, outputs/late_drivers.csv,
#          outputs/monthly_volume_forecast.csv
```

SQL queries in `sql/` are written for a standard SQL dialect (SQLite / DuckDB / SQL Server with minor tweaks — see comments at the top of each file). The Python script is the reference implementation.

## Deliverables

- `tableau/dashboard-spec.md` — what the Tableau dashboard shows, page by page, with filters and calculated fields
- `memo/one-page-memo.md` — the decision memo: top 3 findings, what to do, estimated impact. Fill in the numbers from `outputs/` only.
- This README, `sql/`, `python/`, and `data/README.md` — the work behind the dashboard

## Assumptions — stated plainly

- DataCo is a simulated / public e-commerce supply chain, 2015–2018. It is **not** Tesla data, and its late-delivery patterns do not describe Tesla.
- Shipping-mode scheduled days in the data may not reflect a real carrier promise — check the mode-level gap before recommending a mode change.
- The forecast is a baseline trend, not a demand plan. Safety-stock work (see `alternatives.md`) needs lead-time variability and a service-level choice.
- Inbound freight context (BTS FAF5, Port LA/Long Beach) is monthly / annual and national — use it for direction and seasonality, not for order-level attribution.

## Alternatives in this repo

See `alternatives.md` for the two follow-on projects:
1. Forecast + safety-stock model — reorder points at different service levels
2. Warehouse slotting / pick-path simulation — ABC slotting and travel-time savings, linking to material handling, storage systems, and ASRS coursework
