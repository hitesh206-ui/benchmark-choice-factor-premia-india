# Data Sources

This project is designed around freely accessible public data. No paid databases such as Bloomberg, Refinitiv, Capital IQ, FactSet, Prowess, PitchBook, or Mergermarket should be required.

## Required data categories

### 1. Stock prices and returns

Needed for monthly and daily return calculations.

Potential public sources:

- NSE historical price-volume archives
- NSE bhavcopy files
- NSE security-wise price-volume data
- Yahoo Finance, used only as a fallback or cross-check where appropriate

### 2. Benchmark and index data

Needed to define benchmark universes and compare returns.

Potential public sources:

- NSE Indices index factsheets
- NSE Indices historical index values
- Nifty 50, Nifty 100, Nifty 500, and other broad-market index documentation
- Total Return Index data where available

### 3. Constituents and universe membership

Needed to avoid survivorship bias as much as possible.

Potential public sources:

- NSE Indices current constituent files
- NSE Indices archived factsheets, if available
- Monthly or periodic index constituent disclosures
- Researcher-created liquid NSE universe from historical bhavcopy data

Important limitation: historical constituent files may not be fully available for all periods. If current constituents are used, the paper must explicitly label results as subject to survivorship bias.

### 4. Market capitalization

Needed for size sorting and value-weighted portfolios.

Potential public sources:

- NSE security-level data
- Company shareholding and shares outstanding data
- Annual reports
- Public financial websites used only for verification where data terms allow

### 5. Value variables

Needed for value-factor construction.

Possible measures:

- Book-to-market
- Price-to-book
- Earnings yield
- Dividend yield

Potential public sources:

- Company annual reports
- NSE company information pages
- Public index valuation data
- Screener-style publicly available financial statement data, if manually verified and cited cautiously

### 6. Risk-free rate

Needed for excess returns and performance measures.

Potential public sources:

- RBI Treasury bill data
- RBI government securities data
- FIMMDA or other public fixed-income references where appropriate

## Data storage policy

Raw and processed data should generally not be committed to GitHub. The repository should track:

- Source links
- Collection scripts
- Cleaning scripts
- Data dictionaries
- Small sample files only if legally safe and necessary

Large or frequently updated datasets should stay in local folders ignored by Git:

```text
data/raw/
data/interim/
data/processed/
outputs/
```

## Reproducibility principle

A reader should be able to reproduce the project by following the documented data-source instructions and running the scripts in order.

## Data-quality risks

Key risks include:

1. Survivorship bias from using only current index constituents.
2. Missing delisted firms.
3. Inconsistent ticker/symbol changes.
4. Corporate actions such as splits, bonuses, and dividends.
5. Illiquid small-cap stocks distorting factor returns.
6. Differences between price-return and total-return calculations.
