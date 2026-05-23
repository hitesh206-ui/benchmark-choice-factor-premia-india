# Execution Checklist

## Immediate priority

The next research decision is the universe-construction strategy. The project should avoid survivorship bias as much as possible.

## Data-source verification

- [ ] Confirm public source for historical NSE price-volume data.
- [ ] Confirm public source for Nifty 50, Nifty 100, and Nifty 500 index values.
- [ ] Confirm whether historical index constituent files are available.
- [ ] Confirm whether current constituent files can be downloaded and documented.
- [ ] Confirm source for market capitalization.
- [ ] Confirm source for book-to-market or price-to-book.
- [ ] Confirm source for risk-free rate.

## Universe-construction decision

Choose one of the following:

### Option A: Historical constituents

Best option if monthly or periodic historical constituents are available.

Pros:
- Closest to true benchmark membership.
- Lower survivorship bias.

Cons:
- Historical constituent files may be hard to obtain.

### Option B: Broad liquid NSE universe

Construct the universe from historical price-volume files and liquidity filters.

Pros:
- More reproducible from public files.
- Reduces dependence on unavailable historical constituent files.

Cons:
- Not the exact same as benchmark membership.

### Option C: Current constituents with explicit limitation

Use current benchmark constituents and clearly disclose survivorship bias.

Pros:
- Easiest to implement.

Cons:
- Weakest academically.
- Should be used only for a pilot version.

## First empirical version recommendation

Start with Option B: a broad liquid NSE universe. Then compare results with current Nifty 50, Nifty 100, and Nifty 500 constituents as a pilot benchmark exercise. Upgrade to historical constituents later if the data is found.

## Minimum viable empirical pipeline

- [ ] Download or collect price-volume data.
- [ ] Create monthly stock returns.
- [ ] Add liquidity filters.
- [ ] Add market capitalization.
- [ ] Create size signal.
- [ ] Create momentum signal.
- [ ] Create low-volatility signal.
- [ ] Add value signal once book-value data is available.
- [ ] Construct factor returns by universe.
- [ ] Generate summary statistics.
- [ ] Create first result tables and figures.

## First results to target

1. Summary statistics by universe.
2. Factor-return table by universe.
3. Cumulative factor-return chart.
4. Drawdown chart.
5. Factor correlation matrix across universes.
6. Table showing how factor significance changes by universe.
