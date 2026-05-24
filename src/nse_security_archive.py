"""Utilities for NSE Security-wise Archives equity CSV files.

The NSE company-wise files downloaded from Security-wise Archives often contain
columns such as Symbol, Series, Date, Close Price, Total Traded Quantity, and
Turnover. This module standardizes those files into the project schema.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


COLUMN_MAP = {
    "symbol": "symbol",
    "series": "series",
    "date": "date",
    "prev_close": "prev_close",
    "open_price": "open",
    "high_price": "high",
    "low_price": "low",
    "last_price": "last",
    "close_price": "close",
    "average_price": "vwap",
    "total_traded_quantity": "volume",
    "turnover_₹": "traded_value",
    "turnover": "traded_value",
    "no._of_trades": "num_trades",
    "deliverable_qty": "deliverable_qty",
    "%_dly_qt_to_traded_qty": "deliverable_pct",
}


def _clean_numeric(series: pd.Series) -> pd.Series:
    """Convert NSE comma-formatted numeric strings to floats."""
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.strip(),
        errors="coerce",
    )


def standardize_nse_security_file(path: str | Path) -> pd.DataFrame:
    """Read and standardize one NSE Security-wise Archives CSV file."""
    df = pd.read_csv(path)
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
    )
    df = df.rename(columns={col: COLUMN_MAP.get(col, col) for col in df.columns})

    for col in list(df.columns):
        if "turnover" in col and col != "traded_value":
            df = df.rename(columns={col: "traded_value"})
        if "trades" in col and col != "num_trades":
            df = df.rename(columns={col: "num_trades"})

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="%d-%b-%Y", errors="coerce")

    numeric_cols = [
        "prev_close",
        "open",
        "high",
        "low",
        "last",
        "close",
        "vwap",
        "volume",
        "traded_value",
        "num_trades",
        "deliverable_qty",
        "deliverable_pct",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = _clean_numeric(df[col])

    keep_cols = [
        "symbol",
        "series",
        "date",
        "prev_close",
        "open",
        "high",
        "low",
        "last",
        "close",
        "vwap",
        "volume",
        "traded_value",
        "num_trades",
        "deliverable_qty",
        "deliverable_pct",
    ]
    existing = [col for col in keep_cols if col in df.columns]
    return df[existing].sort_values(["symbol", "date"]).reset_index(drop=True)


def combine_nse_security_files(paths: list[str | Path]) -> pd.DataFrame:
    """Combine several NSE Security-wise Archives files into one standardized file."""
    frames = [standardize_nse_security_file(path) for path in paths]
    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True)
    return combined.sort_values(["symbol", "date"]).reset_index(drop=True)
