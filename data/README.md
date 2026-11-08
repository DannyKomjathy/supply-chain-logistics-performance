# Data — how to get it

Do **not** commit large raw CSVs to the repo.

## DataCo Smart Supply Chain
- Original Kaggle: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
- Downloaded 2026-11-08 via the Hugging Face mirror: https://huggingface.co/datasets/alalfi/SupplyChainDataset (file `DataCoSupplyChainDataset1.csv`, 181k rows shown on HF; 180,519 rows in the file downloaded)
- File: `DataCoSupplyChain.csv` — 180,519 rows, 53 columns, 2015–2018
- Place it at `data/DataCoSupplyChain.csv` — it is in `.gitignore` and must NOT be committed (81 MB, contains customer PII columns)
- Kaggle download requires a Kaggle account; the HF mirror was used here because it is public without a Kaggle login. Record the download date here: 2026-11-08

## BTS Freight Analysis Framework (FAF5)
- https://www.bts.gov/faf/faf5
- Download the regional CSV (FAF5.7.1), filter to the modes / commodities relevant to your inbound story, and save a small extract at `data/faf5_extract.csv` with a note on the filter used.
- FAF5 is estimates, 2017–2024 with forecasts to 2050 — use it for context, not order-level claims.

## Port of LA / Port of Long Beach monthly TEU
- Get the latest monthly statistics tables from each port's official statistics page.
- Save a tidy monthly file at `data/port_teu_monthly.csv` with columns: `month, port, loaded_imports_teu, loaded_exports_teu, empty_teu, total_teu`
- Record download date and source URL here: ____

## Inventory (optional, for sql/04)
- If you want inventory turns / days of supply, supply `data/inventory.csv`:
  `product_id, on_hand_units, avg_daily_demand, lead_time_days`
- Without this file, do not report inventory turns as observed.
