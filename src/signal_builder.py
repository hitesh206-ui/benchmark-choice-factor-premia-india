"""Build factor signals from monthly stock-level panels."""

from __future__ import annotations

import pandas as pd


def add_momentum_signal(
    data: pd.DataFrame,
    symbol_col: str = "symbol",
    date_col: str = "date",
    return_col: str = "return_1m",
    lookback_months: int = 12,
    skip_months: int = 1,
    output_col: str = "momentum_signal",
) -> pd.DataFrame:
    """Add momentum signal using cumulative past returns.

    Default definition: prior 12-month return excluding the most recent month.
    """
    df = data.copy().sort_values([symbol_col, date_col])
    shifted = df.groupby(symbol_col)[return_col].shift(skip_months)
    gross = 1.0 + shifted
    df[output_col] = (
        gross.groupby(df[symbol_col])
        .rolling(lookback_months, min_periods=lookback_months)
        .apply(lambda x: x.prod() - 1.0, raw=False)
        .reset_index(level=0, drop=True)
    )
    return df


def add_volatility_signal(
    data: pd.DataFrame,
    symbol_col: str = "symbol",
    date_col: str = "date",
    return_col: str = "return_1m",
    lookback_months: int = 12,
    output_col: str = "volatility_12m",
) -> pd.DataFrame:
    """Add trailing volatility signal from monthly returns."""
    df = data.copy().sort_values([symbol_col, date_col])
    df[output_col] = (
        df.groupby(symbol_col)[return_col]
        .rolling(lookback_months, min_periods=lookback_months)
        .std()
        .reset_index(level=0, drop=True)
    )
    return df


def add_size_signal(
    data: pd.DataFrame,
    market_cap_col: str = "market_cap",
    output_col: str = "size_signal",
) -> pd.DataFrame:
    """Add size signal from market capitalization.

    The raw market capitalization is retained as the sort signal. Smaller firms
    are treated as the long side in the size factor inside factor construction.
    """
    df = data.copy()
    if market_cap_col not in df.columns:
        raise ValueError(f"Column not found: {market_cap_col}")
    df[output_col] = df[market_cap_col]
    return df


def add_value_signal(
    data: pd.DataFrame,
    book_value_col: str = "book_value_equity",
    market_cap_col: str = "market_cap",
    output_col: str = "book_to_market",
) -> pd.DataFrame:
    """Add book-to-market value signal."""
    df = data.copy()
    missing = [col for col in [book_value_col, market_cap_col] if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df[output_col] = df[book_value_col] / df[market_cap_col]
    return df


def add_core_signals(
    data: pd.DataFrame,
    include_value: bool = False,
) -> pd.DataFrame:
    """Add momentum and volatility signals, and value if inputs are available."""
    df = add_momentum_signal(data)
    df = add_volatility_signal(df)
    if include_value and {"book_value_equity", "market_cap"}.issubset(df.columns):
        df = add_value_signal(df)
    return df
