"""Build monthly stock-level panels for factor construction.

This module contains reusable helpers for converting raw price-volume data into
monthly observations. The functions are intentionally source-agnostic so they
can be used with NSE bhavcopy files, NSE price-volume exports, or manually
compiled public datasets.
"""

from __future__ import annotations

import pandas as pd


def to_month_end_panel(
    data: pd.DataFrame,
    symbol_col: str = "symbol",
    date_col: str = "date",
    price_col: str = "close",
    volume_col: str | None = "volume",
    traded_value_col: str | None = "traded_value",
) -> pd.DataFrame:
    """Convert daily stock-level data to month-end observations.

    The function keeps the last available observation in each symbol-month and
    calculates one-month returns from month-end prices.
    """
    required = [symbol_col, date_col, price_col]
    missing = [col for col in required if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = data.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[symbol_col, date_col, price_col])
    df = df.sort_values([symbol_col, date_col])
    df["month"] = df[date_col].dt.to_period("M").dt.to_timestamp("M")

    agg_map = {price_col: "last"}
    if volume_col and volume_col in df.columns:
        agg_map[volume_col] = "sum"
    if traded_value_col and traded_value_col in df.columns:
        agg_map[traded_value_col] = "sum"

    monthly = (
        df.groupby([symbol_col, "month"], as_index=False)
        .agg(agg_map)
        .rename(columns={"month": date_col})
        .sort_values([symbol_col, date_col])
    )
    monthly["return_1m"] = monthly.groupby(symbol_col)[price_col].pct_change()
    return monthly


def add_traded_value(
    data: pd.DataFrame,
    price_col: str = "close",
    volume_col: str = "volume",
    output_col: str = "traded_value",
) -> pd.DataFrame:
    """Add traded value if price and volume are available."""
    df = data.copy()
    if price_col not in df.columns or volume_col not in df.columns:
        raise ValueError("Price and volume columns are required to calculate traded value.")
    df[output_col] = df[price_col] * df[volume_col]
    return df


def add_liquidity_flags(
    data: pd.DataFrame,
    traded_value_col: str = "traded_value",
    min_monthly_traded_value: float = 0.0,
    output_col: str = "liquidity_filter_pass",
) -> pd.DataFrame:
    """Flag stocks that pass a minimum monthly traded-value filter."""
    df = data.copy()
    if traded_value_col not in df.columns:
        df[output_col] = True
    else:
        df[output_col] = df[traded_value_col].fillna(0) >= min_monthly_traded_value
    return df


def merge_universe_membership(
    panel: pd.DataFrame,
    universe_data: pd.DataFrame,
    symbol_col: str = "symbol",
    date_col: str = "date",
    universe_col: str = "universe",
) -> pd.DataFrame:
    """Merge monthly universe membership onto a monthly stock panel."""
    required_panel = [symbol_col, date_col]
    required_universe = [symbol_col, date_col, universe_col]
    missing_panel = [col for col in required_panel if col not in panel.columns]
    missing_universe = [col for col in required_universe if col not in universe_data.columns]
    if missing_panel or missing_universe:
        raise ValueError(
            f"Missing panel columns: {missing_panel}; missing universe columns: {missing_universe}"
        )

    left = panel.copy()
    right = universe_data.copy()
    left[date_col] = pd.to_datetime(left[date_col]).dt.to_period("M").dt.to_timestamp("M")
    right[date_col] = pd.to_datetime(right[date_col]).dt.to_period("M").dt.to_timestamp("M")
    return left.merge(right[[symbol_col, date_col, universe_col]], on=[symbol_col, date_col], how="left")


def build_liquid_universe(
    panel: pd.DataFrame,
    traded_value_col: str = "traded_value",
    date_col: str = "date",
    percentile_cutoff: float = 0.2,
    universe_name: str = "liquid_nse_universe",
) -> pd.DataFrame:
    """Create a liquid universe based on traded-value percentile by month.

    Stocks below the selected traded-value percentile are excluded.
    """
    df = panel.copy()
    if traded_value_col not in df.columns:
        raise ValueError(f"Column not found: {traded_value_col}")
    threshold = df.groupby(date_col)[traded_value_col].transform(
        lambda x: x.quantile(percentile_cutoff)
    )
    df["universe"] = None
    df.loc[df[traded_value_col] >= threshold, "universe"] = universe_name
    return df[df["universe"].notna()].copy()
