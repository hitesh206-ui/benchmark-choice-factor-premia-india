"""Utilities for NSE CM UDiFF bhavcopy files.

This module standardizes the newer NSE CM bhavcopy ZIP/CSV format, with fields
such as TradDt, TckrSymb, SctySrs, OpnPric, ClsPric, TtlTradgVol, and TtlTrfVal.
"""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd


COLUMN_MAP = {
    "TradDt": "date",
    "BizDt": "business_date",
    "Sgmt": "segment",
    "Src": "source",
    "FinInstrmTp": "instrument_type",
    "FinInstrmId": "instrument_id",
    "ISIN": "isin",
    "TckrSymb": "symbol",
    "SctySrs": "series",
    "FinInstrmNm": "security_name",
    "OpnPric": "open",
    "HghPric": "high",
    "LwPric": "low",
    "ClsPric": "close",
    "LastPric": "last",
    "PrvsClsgPric": "prev_close",
    "TtlTradgVol": "volume",
    "TtlTrfVal": "traded_value",
    "TtlNbOfTxsExctd": "num_trades",
    "NewBrdLotQty": "board_lot_qty",
}

KEEP_COLUMNS = [
    "date",
    "business_date",
    "segment",
    "source",
    "instrument_type",
    "instrument_id",
    "isin",
    "symbol",
    "series",
    "security_name",
    "open",
    "high",
    "low",
    "close",
    "last",
    "prev_close",
    "volume",
    "traded_value",
    "num_trades",
    "board_lot_qty",
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
    "board_lot_qty",
]


def read_udiff_bhavcopy(path: str | Path) -> pd.DataFrame:
    """Read a UDiFF bhavcopy CSV or ZIP file."""
    path = Path(path)
    if path.suffix.lower() == ".zip":
        with ZipFile(path) as archive:
            csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
            if not csv_names:
                raise FileNotFoundError(f"No CSV file found inside {path}")
            with archive.open(csv_names[0]) as file:
                return pd.read_csv(file)
    return pd.read_csv(path)


def standardize_udiff_bhavcopy(path: str | Path, eq_only: bool = True) -> pd.DataFrame:
    """Standardize a NSE CM UDiFF bhavcopy file into the project schema."""
    raw = read_udiff_bhavcopy(path)
    df = raw.rename(columns=COLUMN_MAP)
    existing = [col for col in KEEP_COLUMNS if col in df.columns]
    df = df[existing].copy()

    for col in ["date", "business_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if eq_only and "series" in df.columns:
        df = df[df["series"].eq("EQ")].copy()

    return df.sort_values(["symbol", "date"]).reset_index(drop=True)


def combine_udiff_bhavcopies(paths: list[str | Path], eq_only: bool = True) -> pd.DataFrame:
    """Combine multiple UDiFF bhavcopy files."""
    frames = [standardize_udiff_bhavcopy(path, eq_only=eq_only) for path in paths]
    if not frames:
        return pd.DataFrame(columns=KEEP_COLUMNS)
    return pd.concat(frames, ignore_index=True).sort_values(["symbol", "date"]).reset_index(drop=True)
