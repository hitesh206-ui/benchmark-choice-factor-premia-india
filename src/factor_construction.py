"""Factor construction helpers for Indian equity benchmark-choice research."""

from __future__ import annotations

import pandas as pd

from .portfolio_sorts import (
    assign_quantile_buckets,
    calculate_bucket_returns,
    calculate_long_short_return,
)


def construct_factor_from_signal(
    data: pd.DataFrame,
    signal_col: str,
    return_col: str = "return_1m",
    date_col: str = "date",
    universe_col: str = "universe",
    n_buckets: int = 5,
    weight_col: str | None = None,
    factor_name: str = "factor",
    long_bucket: int = 5,
    short_bucket: int = 1,
) -> pd.DataFrame:
    """Construct long-short factor returns within each universe.

    The function sorts securities into quantile portfolios separately for
    each date-universe cross-section and then calculates a long-short factor.
    """
    required = [date_col, universe_col, signal_col, return_col]
    missing = [col for col in required if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    results = []
    for universe, group in data.groupby(universe_col):
        sorted_group = assign_quantile_buckets(
            group,
            signal_col=signal_col,
            date_col=date_col,
            n_buckets=n_buckets,
            label_col="bucket",
        )
        bucket_returns = calculate_bucket_returns(
            sorted_group,
            return_col=return_col,
            bucket_col="bucket",
            date_col=date_col,
            weight_col=weight_col,
        )
        factor_returns = calculate_long_short_return(
            bucket_returns,
            date_col=date_col,
            bucket_col="bucket",
            return_col="portfolio_return",
            long_bucket=long_bucket,
            short_bucket=short_bucket,
            output_col="factor_return",
        )
        factor_returns[universe_col] = universe
        factor_returns["factor_name"] = factor_name
        factor_returns["signal_col"] = signal_col
        factor_returns["weighting_method"] = "value_weighted" if weight_col else "equal_weighted"
        results.append(factor_returns)

    if not results:
        return pd.DataFrame(
            columns=[date_col, "factor_return", universe_col, "factor_name", "signal_col", "weighting_method"]
        )
    return pd.concat(results, ignore_index=True)


def construct_standard_factors(
    data: pd.DataFrame,
    return_col: str = "return_1m",
    date_col: str = "date",
    universe_col: str = "universe",
    weight_col: str | None = None,
) -> pd.DataFrame:
    """Construct planned size, value, momentum, and low-volatility factors.

    Expected signal columns:
    - `market_cap` for size. The size factor is small minus big, so the
      low market-cap bucket is long and high market-cap bucket is short.
    - `book_to_market` for value.
    - `momentum_signal` for momentum.
    - `volatility_12m` for low volatility. The low-volatility bucket is long
      and the high-volatility bucket is short.
    """
    factor_specs = [
        {
            "factor_name": "size_smb",
            "signal_col": "market_cap",
            "long_bucket": 1,
            "short_bucket": 5,
        },
        {
            "factor_name": "value_hml",
            "signal_col": "book_to_market",
            "long_bucket": 5,
            "short_bucket": 1,
        },
        {
            "factor_name": "momentum_wml",
            "signal_col": "momentum_signal",
            "long_bucket": 5,
            "short_bucket": 1,
        },
        {
            "factor_name": "low_volatility",
            "signal_col": "volatility_12m",
            "long_bucket": 1,
            "short_bucket": 5,
        },
    ]

    frames = []
    for spec in factor_specs:
        if spec["signal_col"] not in data.columns:
            continue
        frames.append(
            construct_factor_from_signal(
                data,
                signal_col=spec["signal_col"],
                return_col=return_col,
                date_col=date_col,
                universe_col=universe_col,
                weight_col=weight_col,
                factor_name=spec["factor_name"],
                long_bucket=spec["long_bucket"],
                short_bucket=spec["short_bucket"],
            )
        )

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)
