# Variable Definitions

This document defines the planned variables for the factor-premia and benchmark-choice analysis.

## Universe variables

| Variable | Definition |
|---|---|
| `date` | Month-end date for the observation |
| `symbol` | NSE stock symbol |
| `company_name` | Company name |
| `universe` | Benchmark or investment universe: Nifty 50, Nifty 100, Nifty 500, or liquid NSE universe |
| `sector` | Sector or industry classification where available |
| `is_eligible` | Indicator for whether the stock passes filters for a given month |

## Return variables

| Variable | Definition |
|---|---|
| `price` | Adjusted or unadjusted closing price depending on available data |
| `return_1m` | One-month stock return |
| `return_12_1` | Past 12-month return excluding the most recent month, used for momentum |
| `excess_return` | Stock or portfolio return minus risk-free rate |
| `market_return` | Benchmark return for the relevant index or broad market |

## Size variables

| Variable | Definition |
|---|---|
| `market_cap` | Market capitalization |
| `log_market_cap` | Natural log of market capitalization |
| `size_rank` | Cross-sectional size rank within a universe and month |
| `size_bucket` | Portfolio group such as small, middle, or big |

## Value variables

| Variable | Definition |
|---|---|
| `book_value_equity` | Book value of shareholder equity |
| `book_to_market` | Book value of equity divided by market capitalization |
| `price_to_book` | Market capitalization divided by book value of equity |
| `value_rank` | Cross-sectional rank based on value signal |
| `value_bucket` | Portfolio group such as value, neutral, or growth |

## Momentum variables

| Variable | Definition |
|---|---|
| `momentum_signal` | Past return signal, usually 12-month return excluding most recent month |
| `momentum_rank` | Cross-sectional rank of momentum signal |
| `momentum_bucket` | Portfolio group such as loser, neutral, or winner |

## Volatility variables

| Variable | Definition |
|---|---|
| `volatility_12m` | Historical return volatility over the prior 12 months |
| `volatility_6m` | Historical return volatility over the prior 6 months |
| `low_vol_rank` | Rank based on historical volatility |
| `low_vol_bucket` | Portfolio group such as low volatility, neutral, or high volatility |

## Liquidity variables

| Variable | Definition |
|---|---|
| `traded_value` | Price multiplied by traded volume |
| `volume` | Number of shares traded |
| `turnover_ratio` | Traded volume divided by shares outstanding, where available |
| `zero_return_days` | Number or proportion of days with zero return in a period |
| `liquidity_filter_pass` | Indicator for whether a stock passes liquidity filters |

## Factor return variables

| Variable | Definition |
|---|---|
| `smb` | Small-minus-big size factor return |
| `hml` | High-minus-low book-to-market value factor return |
| `wml` | Winners-minus-losers momentum factor return |
| `lmh_vol` | Low-minus-high volatility factor return |
| `factor_return` | Generic factor return field |
| `factor_name` | Name of the factor |
| `weighting_method` | Equal-weighted or value-weighted |

## Performance variables

| Variable | Definition |
|---|---|
| `mean_return` | Average periodic return |
| `annualized_return` | Annualized return |
| `annualized_volatility` | Annualized standard deviation |
| `sharpe_ratio` | Annualized excess return divided by annualized volatility |
| `max_drawdown` | Maximum peak-to-trough decline |
| `skewness` | Skewness of return distribution |
| `kurtosis` | Kurtosis of return distribution |
| `hit_rate` | Proportion of positive-return periods |
| `t_stat` | t-statistic of mean factor return |
