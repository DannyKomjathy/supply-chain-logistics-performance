# Memo — Warehouse & Inbound Logistics Performance

**Question:** Where is a distribution flow losing time or money, and what would you change?
**Data:** DataCo Smart Supply Chain, 180,519 order lines (2015–2018). Analysis cut: fulfilled orders only — COMPLETE + CLOSED, n = 79,107. In-flight, canceled, and suspected-fraud orders excluded. Downloaded via the Hugging Face mirror of the Kaggle dataset (`alalfi/SupplyChainDataset`, file `DataCoSupplyChainDataset1.csv`); original Kaggle source is `shashwatwork/dataco-smart-supply-chain-for-big-data-analysis`. No Tesla internal data.

## Headline
**57.3% of fulfilled orders were late — 45,308 of 79,107. On-time rate was 42.7%. Average delivery gap was +0.56 days (actual 3.48 days vs. scheduled 2.92 days).**

The problem is not where orders go, and it is not seasonal. It is how they are promised.

## Finding 1 — First Class is 100% late, by design in the data
- **First Class: 12,324 orders, 100.0% late, avg gap +1.00 day exactly.** Scheduled 1 day, actual 2 days, every time.
- **Second Class: 15,459 orders, 79.5% late, avg gap +1.96 days.** Scheduled 2 days, actual 3.96 days.
- **Standard Class: 47,036 orders, 39.6% late, avg gap −0.01 days.** Scheduled 4 days, actual 3.99 days — the cheapest, longest-promise mode is the most reliable.
- **Same Day: 4,288 orders, 48.2% late, avg gap +0.48 days.** Scheduled 0 days, actual 0.48 days.
- **What to do:** Fix the promise, not just the carrier. Re-set First Class to a 2-day promise (or move that volume to Standard where a 4-day promise is met), and re-set Second Class to 4 days. A 1-day promise the operation meets 0% of the time is a planning error, not a carrier failure.

## Finding 2 — Region and category are not the drivers
- All 23 regions sit between 54.1% and 61.4% late. The worst, South of USA (61.4%, n=1,733), is only ~7 points above the best, Canada (54.1%, n=410).
- The largest product categories by volume — Cleats, Men's Footwear, Women's Apparel — all sit at 56–58% late.
- **What to do:** Do not chase a regional fix. Fix the shipping-mode promise first; it explains the gap, region does not.

## Finding 3 — Late is flat over time; volume is not
- Monthly late rate was 52.7–60.0% from Jan 2015 to Jan 2018, with no improvement trend.
- Monthly fulfilled volume was ~2,100–2,400 orders/month through Sep 2017, then drops to ~925–995/month Oct 2017–Jan 2018. Treat that tail as incomplete data coverage in the source file, not a demand drop, and do not forecast from it.
- **What to do:** Staff / plan to ~2,300 fulfilled orders/month on the pre-Oct-2017 baseline, and investigate the Oct 2017 coverage break before using later months for planning.

## Estimated impact — counterfactual, not a guarantee
If First + Second Class (27,783 orders, 24,620 late today) performed at Standard Class's 39.6% late rate, late orders in this sample would fall by about **13,618 — from 45,308 to about 31,690 — and the overall late rate would fall from 57.3% to 40.1%.**

That assumes the mode change / promise change actually delivers Standard-level performance, which this data alone cannot prove. It is the size of the prize, not a promise.

## Assumptions
- Public / simulated DataCo data, 2015–2018 — not Tesla.
- Fulfilled = COMPLETE + CLOSED. Delivery gap = actual days − scheduled days; late = gap > 0. This matches Delivery_Status = "Late delivery" on this cut.
- Order-to-ship time in this file equals the shipping days field — there is no separate processing stage to split out.
- Inventory turns / days of supply are not computed from DataCo alone (see README).
- Forecast is a 3-month moving-average baseline.
