# Does Benchmark Choice Change Measured Factor Premia in India?

This repository supports a reproducible research project examining whether measured equity factor premia in India change when the investment universe or benchmark changes.

## Working research title

**Does Benchmark Choice Change Measured Factor Premia in India? Evidence from Public NSE Data**

## Core research question

Do common Indian equity factor premia such as size, value, momentum, and low volatility produce different results when constructed using different benchmark universes such as Nifty 50, Nifty 100, Nifty 500, and a broader liquid NSE universe?

## Motivation

Many empirical studies report factor premia for India, but results often depend on the chosen universe. A factor that appears weak in a large-cap universe may appear stronger in a broader universe. This project tests whether benchmark choice affects factor magnitude, statistical significance, drawdown, turnover, and practical investability.

## Planned benchmark universes

1. Nifty 50
2. Nifty 100
3. Nifty 500
4. Liquid NSE universe constructed from public price-volume data

## Planned factors

1. Size
2. Value
3. Momentum
4. Low volatility

Optional later extensions may include quality, profitability, dividend yield, and liquidity.

## Repository structure

```text
benchmark-choice-factor-premia-india/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── docs/
│   ├── data_sources.md
│   ├── methodology.md
│   └── variable_definitions.md
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_factor_construction.ipynb
│   ├── 04_results_analysis.ipynb
│   └── 05_robustness_checks.ipynb
├── outputs/
│   ├── factor_returns/
│   ├── figures/
│   └── tables/
├── paper/
│   ├── draft.md
│   └── references.bib
└── src/
    ├── data_loader.py
    ├── cleaning.py
    ├── factor_construction.py
    ├── performance_metrics.py
    ├── portfolio_sorts.py
    └── regression_tests.py
```

## Public-data principle

This project is designed to use only freely accessible public data sources. It avoids Bloomberg, Refinitiv, Capital IQ, Prowess, FactSet, PitchBook, Mergermarket, and other paid databases.

## Expected outputs

- Clean factor-return datasets
- Tables comparing factor premia across universes
- Figures showing cumulative factor performance and drawdowns
- A research-paper draft suitable for SSRN development
- A reproducible GitHub workflow for future factor research in Indian equities

## Current status

Research design and repository scaffold are being built.

## Disclaimer

This repository is for academic and educational research only. Nothing here is investment advice or a recommendation to buy, sell, or hold any security.
