# How to Run the Project

This guide explains the planned workflow once public data files are downloaded locally.

## 1. Create a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Add raw public data locally

Place raw downloaded files in:

```text
data/raw/
```

Raw data files are ignored by Git and should not be committed.

## 3. Build monthly stock panel

Expected minimum input columns:

```text
date
symbol
close
```

Optional columns:

```text
volume
traded_value
```

Example:

```bash
python scripts/build_monthly_panel.py \
  --input data/raw/prices.csv \
  --output data/processed/monthly_panel.csv
```

## 4. Build factor returns

The monthly panel should include:

```text
date
symbol
universe
return_1m
market_cap
```

Optional for value factor:

```text
book_value_equity
```

Example equal-weighted run:

```bash
python scripts/build_factor_returns.py \
  --input data/processed/monthly_panel.csv \
  --output outputs/factor_returns/factor_returns_equal_weighted.csv
```

Example value-weighted run:

```bash
python scripts/build_factor_returns.py \
  --input data/processed/monthly_panel.csv \
  --output outputs/factor_returns/factor_returns_value_weighted.csv \
  --value-weighted
```

## 5. Analyze factor returns

```bash
python scripts/analyze_factor_returns.py \
  --input outputs/factor_returns/factor_returns_equal_weighted.csv \
  --output outputs/tables/factor_summary_equal_weighted.csv
```

## 6. Use notebooks for exploration

The notebooks provide a guided workflow:

```text
notebooks/01_data_collection.ipynb
notebooks/02_data_cleaning.ipynb
notebooks/03_factor_construction.ipynb
notebooks/04_results_analysis.ipynb
notebooks/05_robustness_checks.ipynb
```

## Important limitation

The scripts are templates until the exact raw data format is finalized. Once the source files are selected, column names and cleaning rules should be adjusted carefully.
