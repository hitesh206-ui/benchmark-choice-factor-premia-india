"""Utilities for NSE Full Bhavcopy and Security Deliverable data files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


COLUMN_MAP = {
    "symbol": "symbol",
    "series": "series",
    "date1": "date",
    "prev_close": "prev_close",
    "open_price": "open",
    "high_price": "high",
    "low_price": "low",
    "last_price": "last",
    "close_price": "close",
    "avg_price": "vwap",
    "ttl_trd_qnty": "volume",
    "turnover_lacs": "turnover_lacs",
    "no_of_trades": "num_trades",
    "deliv_qty": "deliverable_qty",
    "deliv_per": "deliverable_pct",
}

KEEP_COLUMNS = [
    "date",
    "symbol",
    "series",
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


def standardize_full_bhavdata(path: str | Path, eq_only: bool = True) -> pd.DataFrame:
    """Read and standardize a full bhavdata CSV file."""
    df = pd.read_csv(path)
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    df = df.rename(columns={col: COLUMN_MAP.get(col, col) for col in df.columns})

    for col in ["symbol", "series"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"].astype(str).str.strip(), format="%d-%b-%Y", errors="coerce")

    numeric_cols = [
        "prev_close",
        "open",
        "high",
        "low",
        "last",
        "close",
        "vwap",
        "volume",
        "turnover_lacs",
        "num_trades",
        "deliverable_qty",
        "deliverable_pct",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "turnover_lacs" in df.columns:
        df["traded_value"] = df["turnover_lacs"] * 100000.0

    if eq_only and "series" in df.columns:
        df = df[df["series"].eq("EQ")].copy()

    existing = [col for col in KEEP_COLUMNS if col in df.columns]
    return df[existing].sort_values(["symbol", "date"]).reset_index(drop=True)


def combine_full_bhavdata(paths: list[str | Path], eq_only: bool = True) -> pd.DataFrame:
    """Combine multiple full bhavdata CSV files."""
    frames = [standardize_full_bhavdata(path, eq_only=eq_only) for path in paths]
    if not frames:
        return pd.DataFrame(columns=KEEP_COLUMNS)
    combined = pd.concat(frames, ignore_index=True)
    return combined.drop_duplicates(["date", "symbol", "series"]).sort_values(["symbol", "date"]).reset_index(drop=True)
