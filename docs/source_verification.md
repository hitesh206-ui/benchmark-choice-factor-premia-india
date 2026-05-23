# Verified Public Source Plan

This file records the public-data source strategy for making the project empirically executable.

## 1. Stock price and volume data

Primary source:

- NSE Historical Reports page
- Security-wise Price Volume Archives for equities
- Archives of Daily / Monthly Reports for equity market reports

Use case:

- Daily close price
- Volume
- Traded value where available
- Security-level price-volume history

Research use:

- Build monthly returns
- Build liquidity filters
- Build broad liquid NSE universe

## 2. Index and benchmark data

Primary source:

- NSE Historical Index Data
- NSE Indices Historical Data reports
- NSE Indices Daily / Monthly Reports
- Total Return Index values where available
- P/E, P/B, and dividend yield values where available

Use case:

- Nifty 50, Nifty 100, Nifty 500 index levels
- Price index and total return index comparisons
- Index valuation references

## 3. Constituents and benchmark membership

Primary source:

- NSE Indices factsheets
- NSE Indices daily or monthly reports
- Current constituent files where available
- Archived factsheets if available

Use case:

- Current or historical benchmark membership
- Benchmark comparison groups

Important warning:

Historical constituents may not be fully available in a clean downloadable format. If historical membership cannot be reconstructed, the first empirical version should use a broad liquid NSE universe as the primary universe and treat current benchmark constituents as a pilot comparison only.

## 4. Risk-free rate

Primary source:

- RBI Bulletin tables
- Government of India Treasury Bill auction tables
- 91-day Treasury Bill data where available

Use case:

- Monthly risk-free rate proxy
- Excess return calculation
- Sharpe ratio calculation

## 5. Market capitalization

Potential public sources:

- NSE security information
- NSE market capitalization reports where available
- Company shares outstanding from filings
- Price multiplied by shares outstanding

Use case:

- Size factor
- Value-weighted portfolio returns
- Liquidity and investability checks

## 6. Value variable

Potential public sources:

- Annual reports
- Public financial statements
- NSE/company filings
- Price-to-book or book-value data from public sources, if verifiable

Use case:

- Book-to-market factor
- Price-to-book value signal

Important warning:

Value-factor construction is more difficult than momentum or low-volatility because it requires accounting data and careful timing to avoid look-ahead bias. The first empirical version can begin with size, momentum, and low-volatility, then add value once accounting data is reliable.

## Recommended empirical sequence

1. Build price-return panel.
2. Build broad liquid NSE universe.
3. Construct momentum and low-volatility factors first.
4. Add market capitalization and size factor.
5. Add value factor only after reliable accounting data is available.
6. Compare with Nifty 50, Nifty 100, and Nifty 500 where constituent data allows.

## Minimum viable empirical version

The minimum viable empirical version should include:

- Monthly returns
- Liquidity filter
- Liquid NSE universe
- Momentum factor
- Low-volatility factor
- Summary statistics
- Cumulative return figures
- Drawdown figures

This version is empirically useful even before value-factor and historical-constituent issues are fully solved.
