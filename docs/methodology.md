# Methodology

## Research question

Does benchmark or investment-universe choice change measured Indian equity factor premia?

The project compares factor results across multiple Indian equity universes rather than only asking whether a factor works in India.

## Planned universes

1. **Nifty 50**: concentrated large-cap benchmark.
2. **Nifty 100**: broader large-cap universe.
3. **Nifty 500**: broad listed-equity benchmark.
4. **Liquid NSE universe**: researcher-created universe using public price-volume and liquidity filters.

## Main factors

### 1. Size

Stocks are sorted by market capitalization. The basic factor return is the return of small-cap stocks minus large-cap stocks within the relevant universe.

### 2. Value

Stocks are sorted by valuation measures such as book-to-market or price-to-book. The value factor return is the return of high book-to-market stocks minus low book-to-market stocks.

### 3. Momentum

Stocks are sorted by prior return, usually using a 12-month lookback period excluding the most recent month. The momentum factor return is the return of past winners minus past losers.

### 4. Low volatility

Stocks are sorted by historical return volatility. The low-volatility factor return is the return of low-volatility stocks minus high-volatility stocks.

## Portfolio construction approach

The initial approach will use monthly rebalancing where possible.

For each universe and factor:

1. Define the eligible stock universe for each month.
2. Apply data-quality and liquidity filters.
3. Compute the relevant factor signal.
4. Sort stocks into portfolios.
5. Calculate equal-weighted and, where feasible, value-weighted returns.
6. Construct long-short factor returns.
7. Compare factor returns across universes.

## Core tests

The project will compare:

- Mean monthly factor return
- Annualized factor return
- Volatility
- Sharpe ratio
- Maximum drawdown
- Skewness
- Hit rate
- Turnover
- t-statistics
- Correlations across benchmark-specific factor series

## Key hypotheses

### H1: Factor premia differ across benchmark universes.

Measured factor premia are expected to vary between Nifty 50, Nifty 100, Nifty 500, and the broader liquid NSE universe.

### H2: The size factor is underestimated in narrow large-cap universes.

A concentrated large-cap universe such as Nifty 50 cannot fully capture the small-minus-big effect.

### H3: Value and momentum are more sensitive to universe definition than low volatility.

Value and momentum may depend more heavily on the inclusion of mid-cap and smaller companies.

### H4: Liquidity filters materially affect measured factor premia.

A factor premium that appears strong before liquidity filtering may weaken after excluding illiquid stocks.

## Robustness checks

Planned robustness checks include:

- Equal-weighted versus value-weighted factor portfolios
- Different rebalancing frequencies
- Alternative lookback windows for momentum and volatility
- Excluding crisis periods such as COVID-19
- Applying stricter liquidity filters
- Comparing Nifty 50, Nifty 100, Nifty 500, and researcher-created universes

## Main methodological risk

The largest risk is survivorship bias. If only current index constituents are used for historical testing, results may be biased. The project will document this limitation clearly and prioritize historical constituent data or a broad historical NSE universe where possible.
