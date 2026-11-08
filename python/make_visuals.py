"""Make dashboard visuals from outputs/ — PNGs in visuals/.

Run after python/analysis.py. No raw customer data is plotted.
"""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
VIS = ROOT / "visuals"
VIS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "axes.titlesize": 12, "axes.labelsize": 10})

# 1 — On-time rate by shipping mode
cycle = pd.read_csv(OUT / "cycle_time.csv")
cycle["on_time_rate"] = 1 - cycle["late_rate"] if "late_rate" in cycle else None
# cycle_time.csv has no late_rate; recompute from late_drivers
drivers = pd.read_csv(OUT / "late_drivers.csv")
m = cycle.merge(drivers[["Shipping_Mode", "late_rate"]], on="Shipping_Mode")
m = m.sort_values("late_rate", ascending=False)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(m["Shipping_Mode"], m["late_rate"] * 100, color="#c0392b")
for i, v in enumerate(m["late_rate"] * 100):
    ax.text(v + 1, i, f"{v:.1f}% late", va="center")
ax.set_xlim(0, 125)
ax.set_xlabel("Late deliveries (% of fulfilled orders)")
ax.set_title("Late rate by shipping mode — First Class is 100% late")
ax.invert_yaxis()
fig.tight_layout()
fig.savefig(VIS / "late_rate_by_shipping_mode.png")
plt.close(fig)

# 2 — Scheduled vs actual days by mode
fig, ax = plt.subplots(figsize=(8, 4.5))
x = range(len(m))
ax.bar([i - 0.2 for i in x], m["avg_scheduled_days"], width=0.4, label="Scheduled days")
ax.bar([i + 0.2 for i in x], m["avg_actual_days"], width=0.4, label="Actual days")
ax.set_xticks(list(x))
ax.set_xticklabels(m["Shipping_Mode"])
ax.set_ylabel("Days")
ax.set_title("Scheduled vs. actual shipping days by mode")
ax.legend()
fig.tight_layout()
fig.savefig(VIS / "scheduled_vs_actual_by_mode.png")
plt.close(fig)

# 3 — Monthly volume + late rate
monthly = pd.read_csv(OUT / "monthly_volume_forecast.csv", parse_dates=["order_month"])
fig, ax1 = plt.subplots(figsize=(9, 4.5))
ax1.plot(monthly["order_month"], monthly["orders"], marker="o", ms=3, label="Fulfilled orders / month")
ax1.plot(monthly["order_month"], monthly["forecast_3m_ma"], label="3-month moving-average forecast", linestyle="--")
ax1.set_ylabel("Orders per month")
ax1.set_title("Monthly fulfilled orders — flat late rate, volume drop after Sep 2017 is data coverage")
ax1.legend(loc="upper left")
ax2 = ax1.twinx()
ax2.plot(monthly["order_month"], monthly["late_rate"] * 100, color="#c0392b", alpha=0.6, label="Late %")
ax2.set_ylabel("Late %")
fig.tight_layout()
fig.savefig(VIS / "monthly_volume_and_late_rate.png")
plt.close(fig)

print(f"Wrote visuals to {VIS}/")
for p in sorted(VIS.glob("*.png")):
    print(" -", p.name)
