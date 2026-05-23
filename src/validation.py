"""Validation utilities for empirical research datasets."""

from __future__ import annotations

import pandas as pd


class ValidationError(Exception):
    """Raised when a dataset fails validation."""


def require_columns(data: pd.DataFrame, required_columns: list[str], dataset_name: str = "dataset") -> None:
    """Raise ValidationError if required columns are missing."""
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValidationError(f"{dataset_name} is missing required columns: {missing}")


def validate_monthly_panel(data: pd.DataFrame) -> dict[str, object]:
    """Validate the minimum monthly panel required for factor construction."""
    required = ["date", "symbol", "return_1m"]
    require_columns(data, required, dataset_name="monthly panel")

    report: dict[str, object] = {}
    report["rows"] = int(len(data))
    report["columns"] = list(data.columns)
    report["unique_symbols"] = int(data["symbol"].nunique())
    report["missing_return_1m"] = int(data["return_1m"].isna().sum())
    report["start_date"] = str(pd.to_datetime(data["date"]).min().date())
    report["end_date"] = str(pd.to_datetime(data["date"]).max().date())

    optional = ["universe", "market_cap", "book_to_market", "momentum_signal", "volatility_12m", "traded_value"]
    report["available_optional_columns"] = [col for col in optional if col in data.columns]
    report["missing_optional_columns"] = [col for col in optional if col not in data.columns]

    return report


def validate_factor_returns(data: pd.DataFrame) -> dict[str, object]:
    """Validate factor-return dataset."""
    required = ["date", "universe", "factor_name", "factor_return"]
    require_columns(data, required, dataset_name="factor returns")

    report: dict[str, object] = {}
    report["rows"] = int(len(data))
    report["universes"] = sorted(data["universe"].dropna().astype(str).unique().tolist())
    report["factors"] = sorted(data["factor_name"].dropna().astype(str).unique().tolist())
    report["start_date"] = str(pd.to_datetime(data["date"]).min().date())
    report["end_date"] = str(pd.to_datetime(data["date"]).max().date())
    report["missing_factor_return"] = int(data["factor_return"].isna().sum())
    return report


def check_duplicate_symbol_dates(
    data: pd.DataFrame,
    symbol_col: str = "symbol",
    date_col: str = "date",
) -> pd.DataFrame:
    """Return duplicate symbol-date rows for inspection."""
    require_columns(data, [symbol_col, date_col], dataset_name="panel")
    duplicated = data.duplicated(subset=[symbol_col, date_col], keep=False)
    return data.loc[duplicated].sort_values([symbol_col, date_col])
