# Project Roadmap

## Phase 1: Research design

- [x] Define research question
- [x] Define benchmark universes
- [x] Define primary factors
- [x] Document methodology
- [x] Document variables
- [x] Document public data-source strategy

## Phase 2: Data collection

- [ ] Collect Nifty 50, Nifty 100, and Nifty 500 index information
- [ ] Collect stock-level historical price-volume data
- [ ] Collect or reconstruct eligible monthly stock universes
- [ ] Collect market capitalization data
- [ ] Collect value-signal data such as book-to-market or price-to-book
- [ ] Collect risk-free-rate data

## Phase 3: Data cleaning

- [ ] Standardize symbols and company names
- [ ] Handle ticker changes where possible
- [ ] Adjust or flag corporate actions
- [ ] Convert daily data to monthly data
- [ ] Calculate monthly stock returns
- [ ] Apply liquidity filters
- [ ] Build monthly analysis panel

## Phase 4: Factor construction

- [ ] Build size factor
- [ ] Build value factor
- [ ] Build momentum factor
- [ ] Build low-volatility factor
- [ ] Compare equal-weighted and value-weighted factor returns
- [ ] Export factor-return datasets

## Phase 5: Empirical analysis

- [ ] Compare mean returns across universes
- [ ] Calculate t-statistics
- [ ] Calculate Sharpe ratios
- [ ] Calculate drawdowns
- [ ] Calculate factor correlations across universes
- [ ] Run regression tests

## Phase 6: Robustness checks

- [ ] Test alternative liquidity filters
- [ ] Test alternative momentum lookback windows
- [ ] Test alternative volatility lookback windows
- [ ] Exclude crisis windows such as COVID-19
- [ ] Compare equal-weighted and value-weighted results

## Phase 7: Paper development

- [ ] Expand literature review
- [ ] Add data section
- [ ] Add empirical results
- [ ] Add tables and figures
- [ ] Add limitations and robustness discussion
- [ ] Prepare SSRN-ready draft

## Main open methodological issue

The biggest risk is survivorship bias. The project should prioritize historical constituent data or a broad NSE universe reconstructed from historical public data. If historical constituents are unavailable, the paper must explicitly state the limitation and avoid overstating conclusions.
