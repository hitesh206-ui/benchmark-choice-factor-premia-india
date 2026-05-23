# How to Run the Project

This guide explains the workflow once public data files are downloaded locally.

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

You can also run:

```bash
make install
```

## 2. Add raw public data locally

Place raw downloaded files in:

```text
data/raw/
```

Raw data files are ignored by Git and should not be committed.

The default script examples assume a local file named:

```text
data/raw/prices.csv
```

Expected minimum columns:

```text
date
symbol
close
```

Useful optional columns:

```text
volume
traded_value
market_cap
universe
book_value_equity
```

## 3. Build monthly stock panel

```bash
python scripts/build_monthly_panel.py \
  --input data/raw/prices.csv \
  --output data/processed/monthly_panel.csv
```

Or:

```bash
make build-panel
```

## 4. Validate monthly panel

```bash
python scripts/validate_monthly_panel.py \
  --input data/processed/monthly_panel.csv \
  --output outputs/tables/monthly_panel_validation.json
```

Or:

```bash
make validate-panel
```

## 5. Build factor returns

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

Or:

```bash
make build-factors
```

Example value-weighted run:

```bash
python scripts/build_factor_returns.py \
  --input data/processed/monthly_panel.csv \
  --output outputs/factor_returns/factor_returns_value_weighted.csv \
  --value-weighted
```

## 6. Validate factor returns

```bash
python scripts/validate_factor_returns.py \
  --input outputs/factor_returns/factor_returns_equal_weighted.csv \
  --output outputs/tables/factor_returns_validation.json
```

Or:

```bash
make validate-factors
```

## 7. Analyze factor returns

```bash
python scripts/analyze_factor_returns.py \
  --input outputs/factor_returns/factor_returns_equal_weighted.csv \
  --output outputs/tables/factor_summary_equal_weighted.csv
```

Or:

```bash
make analyze
```

## 8. Use notebooks for exploration

The notebooks provide a guided workflow:

```text
notebooks/01_data_collection.ipynb
notebooks/02_data_cleaning.ipynb
notebooks/03_factor_construction.ipynb
notebooks/04_results_analysis.ipynb
notebooks/05_robustness_checks.ipynb
```

## Minimum empirical version

The fastest empirically useful version should first use:

```text
monthly returns
traded value / volume
liquidity-filtered broad NSE universe
momentum factor
low-volatility factor
summary statistics
drawdown and cumulative-return charts
```

Then add:

```text
market capitalization
size factor
book value or price-to-book
value factor
benchmark constituent comparisons
```

## Important limitation

The scripts are templates until the exact raw data format is finalized. Once source files are selected, column names and cleaning rules should be adjusted carefully.
