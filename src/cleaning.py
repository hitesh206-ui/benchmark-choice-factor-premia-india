"""Data-cleaning helpers for benchmark-choice factor premia project."""

from __future__ import annotations

import pandas as pd


def standardize_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase snake-case style."""
    df = data.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
    )
    return df


def parse_date_column(data: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Parse a date column to pandas datetime."""
    df = data.copy()
    if date_col not in df.columns:
        raise ValueError(f"Date column not found: {date_col}")
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    return df


def calculate_simple_returns(
    data: pd.DataFrame,
    price_col: str = "close",
    symbol_col: str = "symbol",
    date_col: str = "date",
    output_col: str = "return_1m",
) -> pd.DataFrame:
    """Calculate simple returns by symbol from a price column."""
    df = data.copy().sort_values([symbol_col, date_col])
    df[output_col] = df.groupby(symbol_col)[price_col].pct_change()
    return df


def winsorize_by_date(
    data: pd.DataFrame,
    cols: list[str],
    date_col: str = "date",
    lower: float = 0.01,
    upper: float = 0.99,
) -> pd.DataFrame:
    """Winsorize selected columns cross-sectionally by date."""
    df = data.copy()
    for col in cols:
        if col not in df.columns:
            continue
        lower_q = df.groupby(date_col)[col].transform(lambda x: x.quantile(lower))
        upper_q = df.groupby(date_col)[col].transform(lambda x: x.quantile(upper))
        df[col] = df[col].clip(lower=lower_q, upper=upper_q)
    return df


def apply_basic_liquidity_filter(
    data: pd.DataFrame,
    traded_value_col: str = "traded_value",
    min_traded_value: float = 0.0,
    output_col: str = "liquidity_filter_pass",
) -> pd.DataFrame:
    """Add a basic liquidity-filter indicator based on traded value."""
    df = data.copy()
    if traded_value_col not in df.columns:
        df[output_col] = True
        return df
    df[output_col] = df[traded_value_col].fillna(0) >= min_traded_value
    return df
