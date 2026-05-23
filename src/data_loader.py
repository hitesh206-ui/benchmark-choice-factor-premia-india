"""Data loading helpers for local research files.

Raw data files are intentionally ignored by Git. These functions assume the
user has downloaded public data into the local data folders documented in
`docs/data_sources.md`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"


def read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read a CSV file from a path."""
    return pd.read_csv(Path(path), **kwargs)


def read_excel(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read an Excel file from a path."""
    return pd.read_excel(Path(path), **kwargs)


def save_processed_csv(data: pd.DataFrame, filename: str, index: bool = False) -> Path:
    """Save a processed CSV into data/processed and return the file path."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / filename
    data.to_csv(output_path, index=index)
    return output_path


def list_raw_files(pattern: str = "*") -> list[Path]:
    """List files in the raw data folder matching a pattern."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    return sorted(RAW_DIR.glob(pattern))
