"""Warehouse & inbound logistics performance — DataCo analysis.

Reproduces the SQL in sql/ and adds a simple monthly volume forecast.
Run:
    python python/analysis.py --input data/DataCoSupplyChain.csv --out outputs/

Outputs (CSV, in --out):
    kpi_summary.csv, on_time_by_mode_region.csv, cycle_time.csv,
    late_drivers.csv, monthly_volume_forecast.csv

Column mapping: the Hugging Face mirror of the Kaggle DataCo file uses
  Days_for_shipping_(real), Days_for_shipment_(scheduled),
  order_date_(DateOrders), shipping_date_(DateOrders)
which are renamed here to real / scheduled / order_date / ship_date.

Fulfilled orders = Order_Status in (COMPLETE, CLOSED). In-flight
(PENDING, PROCESSING, PENDING_PAYMENT, ON_HOLD, PAYMENT_REVIEW),
CANCELED and SUSPECTED_FRAUD are excluded because their delivery
outcome is not final. PII columns (customer name, email, password,
street, etc.) are never loaded.

Assumptions are in the repo README. Do not present outputs as Tesla data.
"""
import argparse
import pathlib

import pandas as pd

USE_COLS = [
    "Order_Item_Id", "Order_Status",
    "Days_for_shipping_(real)", "Days_for_shipment_(scheduled)",
    "Delivery_Status", "Late_delivery_risk",
    "Shipping_Mode", "Order_Region", "Category_Name",
    "order_date_(DateOrders)", "shipping_date_(DateOrders)",
    "Sales", "Order_Item_Quantity", "Order_Profit_Per_Order",
]
RENAME = {
    "Days_for_shipping_(real)": "Days_for_shipping_real",
    "Days_for_shipment_(scheduled)": "Days_for_shipment_scheduled",
    "order_date_(DateOrders)": "DateOrders",
    "shipping_date_(DateOrders)": "Shipping_Date",
}
FULFILLED = ["COMPLETE", "CLOSED"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="outputs")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input, low_memory=False, usecols=USE_COLS).rename(columns=RENAME)

    completed = df[df["Order_Status"].isin(FULFILLED)].copy()
    completed["delivery_gap"] = (
        completed["Days_for_shipping_real"] - completed["Days_for_shipment_scheduled"]
    )
    completed["is_late"] = completed["delivery_gap"] > 0
    completed["is_on_time"] = completed["delivery_gap"] <= 0

    kpi = pd.DataFrame([{
        "orders_total": len(df),
        "orders_fulfilled": len(completed),
        "on_time_rate": completed["is_on_time"].mean(),
        "late_rate": completed["is_late"].mean(),
        "late_orders": int(completed["is_late"].sum()),
        "avg_delivery_gap_days": completed["delivery_gap"].mean(),
        "avg_actual_days": completed["Days_for_shipping_real"].mean(),
        "avg_scheduled_days": completed["Days_for_shipment_scheduled"].mean(),
        "total_sales_fulfilled": completed["Sales"].sum(),
    }])
    kpi.to_csv(out / "kpi_summary.csv", index=False)

    by_mode_region = (
        completed.groupby(["Order_Region", "Shipping_Mode"])
        .agg(orders=("Order_Item_Id", "count"),
             on_time_rate=("is_on_time", "mean"),
             avg_gap_days=("delivery_gap", "mean"))
        .reset_index()
        .sort_values("on_time_rate")
    )
    by_mode_region.to_csv(out / "on_time_by_mode_region.csv", index=False)

    cycle = (
        completed.groupby("Shipping_Mode")
        .agg(orders=("Order_Item_Id", "count"),
             avg_actual_days=("Days_for_shipping_real", "mean"),
             avg_scheduled_days=("Days_for_shipment_scheduled", "mean"),
             avg_gap_days=("delivery_gap", "mean"))
        .reset_index()
        .sort_values("avg_gap_days", ascending=False)
    )
    cycle.to_csv(out / "cycle_time.csv", index=False)

    drivers = (
        completed.groupby("Shipping_Mode")
        .agg(orders=("Order_Item_Id", "count"),
             late_orders=("is_late", "sum"),
             late_rate=("is_late", "mean"))
        .reset_index()
        .sort_values("late_orders", ascending=False)
    )
    drivers.to_csv(out / "late_drivers.csv", index=False)

    # Monthly volume + simple baseline forecast (3-month moving average).
    # Note: Oct 2017–Jan 2018 volume drops sharply in the source file;
    # treat that tail as incomplete coverage, not a demand drop.
    completed["order_month"] = pd.to_datetime(
        completed["DateOrders"], errors="coerce"
    ).dt.to_period("M").dt.to_timestamp()
    monthly = (
        completed.groupby("order_month")
        .agg(orders=("Order_Item_Id", "count"),
             late_rate=("is_late", "mean"))
        .reset_index().sort_values("order_month")
    )
    monthly["forecast_3m_ma"] = monthly["orders"].rolling(3).mean().shift(1)
    monthly.to_csv(out / "monthly_volume_forecast.csv", index=False)

    print(kpi.to_string(index=False))
    print(f"\nWrote outputs to {out}/")


if __name__ == "__main__":
    main()
