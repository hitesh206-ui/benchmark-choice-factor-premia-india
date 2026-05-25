"""Utilities for legacy NSE CM bhavcopy files used before UDiFF.

Expected legacy fields commonly include:
SYMBOL, SERIES, OPEN, HIGH, LOW, CLOSE, LAST, PREVCLOSE, TOTTRDQTY,
TOTTRDVAL, TIMESTAMP, TOTALTRADES, ISIN.
"""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd


COLUMN_MAP = {
    "SYMBOL": "symbol",
    "SERIES": "series",
    "OPEN": "open",
    "HIGH": "high",
    "LOW": "low",
    "CLOSE": "close",
    "LAST": "last",
    "PREVCLOSE": "prev_close",
    "TOTTRDQTY": "volume",
    "TOTTRDVAL": "traded_value",
    "TIMESTAMP": "date",
    "TOTALTRADES": "num_trades",
    "ISIN": "isin",
}

KEEP_COLUMNS = [
    "date",
    "isin",
    "symbol",
    "series",
    "open",
    "high",
    "low",
    "close",
    "last",
    "prev_close",
    "volume",
    "traded_value",
    "num_trades",
]

NUMERIC_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "last",
    "prev_close",
    "volume",
    "traded_value",
    "num_trades",
]


def read_legacy_bhavcopy(path: str | Path) -> pd.DataFrame:
    """Read a legacy NSE bhavcopy CSV or ZIP file."""
    path = Path(path)
    if path.suffix.lower() == ".zip":
        with ZipFile(path) as archive:
            csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
            if not csv_names:
                raise FileNotFoundError(f"No CSV file found inside {path}")
            with archive.open(csv_names[0]) as file:
                return pd.read_csv(file)
    return pd.read_csv(path)


def standardize_legacy_bhavcopy(path: str | Path, eq_only: bool = True) -> pd.DataFrame:
    """Standardize one legacy NSE CM bhavcopy file into the project schema."""
    raw = read_legacy_bhavcopy(path)
    raw.columns = raw.columns.astype(str).str.strip().str.upper()
    df = raw.rename(columns=COLUMN_MAP)

    existing = [col for col in KEEP_COLUMNS if col in df.columns]
    df = df[existing].copy()

    for col in ["symbol", "series", "isin"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if eq_only and "series" in df.columns:
        df = df[df["series"].eq("EQ")].copy()

    return df.sort_values(["symbol", "date"]).reset_index(drop=True)


def combine_legacy_bhavcopies(paths: list[str | Path], eq_only: bool = True) -> pd.DataFrame:
    """Combine multiple legacy NSE bhavcopy files."""
    frames = [standardize_legacy_bhavcopy(path, eq_only=eq_only) for path in paths]
    if not frames:
        return pd.DataFrame(columns=KEEP_COLUMNS)
    combined = pd.concat(frames, ignore_index=True)
    return combined.drop_duplicates(["date", "symbol", "series"]).sort_values(["symbol", "date"]).reset_index(drop=True)
