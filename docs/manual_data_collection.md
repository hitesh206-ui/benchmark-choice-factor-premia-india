# Manual Data Collection Guide

This project avoids committing large raw datasets to GitHub. Raw files should be downloaded locally and stored under `data/raw/`.

## Minimum viable raw file

The fastest way to test the empirical pipeline is to create:

```text
data/raw/prices.csv
```

Minimum required columns:

```text
date,symbol,close
```

Recommended columns:

```text
date,symbol,close,volume,traded_value,market_cap,universe,book_value_equity
```

## Step 1: Price-volume data

Use NSE historical price-volume or bhavcopy style files.

Target fields:

- trade date
- symbol
- close price
- traded quantity or volume
- traded value, if available

After downloading, standardize the file into:

```text
date,symbol,close,volume,traded_value
```

## Step 2: Create first empirical universe

For the first version, use a broad liquid universe rather than relying only on current index constituents.

Recommended first universe label:

```text
liquid_nse_universe
```

A stock can be included if it passes a traded-value filter for that month.

## Step 3: Market capitalization

Market capitalization is required for:

- size factor
- value-weighted portfolios

Add a column:

```text
market_cap
```

If shares outstanding are available, market cap can be calculated as:

```text
close_price * shares_outstanding
```

## Step 4: Book value or price-to-book

Book value is required for the value factor.

Add either:

```text
book_value_equity
```

or construct:

```text
book_to_market = book_value_equity / market_cap
```

Important: accounting data must be lagged to avoid look-ahead bias. Do not use financial statements before they were publicly available.

## Step 5: Benchmark comparison files

For Nifty 50, Nifty 100, and Nifty 500 comparisons, collect constituent files if available.

Target format:

```text
date,symbol,universe
```

Example:

```text
2024-12-31,RELIANCE,nifty_50
2024-12-31,TCS,nifty_50
```

## Recommended first empirical path

1. Start with `data/raw/prices.csv`.
2. Build `data/processed/monthly_panel.csv`.
3. Validate the monthly panel.
4. Construct momentum and low-volatility first.
5. Add market cap and size factor.
6. Add value factor only after book-value timing is reliable.
7. Add Nifty 50 / 100 / 500 comparison after constituent data is stable.

## Important warnings

- Do not upload large raw files to GitHub.
- Do not use current constituents for the full historical period without calling it survivorship-biased.
- Do not use accounting values before their public filing date.
- Do not overstate results from a pilot sample.
