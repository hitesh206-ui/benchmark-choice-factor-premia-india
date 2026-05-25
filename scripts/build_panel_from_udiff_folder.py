"""Build daily and monthly panels from a folder of NSE UDiFF bhavcopy ZIP files.

Example:

    python scripts/build_panel_from_udiff_folder.py \
      --input-dir data/raw/udiff_bhavcopy \
      --daily-output data/interim/standardized_daily_eq.csv \
      --monthly-output data/processed/monthly_panel_eq.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.nse_udiff_bhavcopy import combine_udiff_bhavcopies


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build daily and monthly panels from NSE UDiFF files.")
    parser.add_argument("--input-dir", default="data/raw/udiff_bhavcopy")
    parser.add_argument("--daily-output", default="data/interim/standardized_daily_eq.csv")
    parser.add_argument("--monthly-output", default="data/processed/monthly_panel_eq.csv")
    return parser.parse_args()


def build_monthly_panel(daily: pd.DataFrame) -> pd.DataFrame:
    """Aggregate standardized daily EQ data to symbol-month level."""
    data = daily.copy()
    data["month"] = data["date"].dt.to_period("M").dt.to_timestamp("M")
    monthly = (
        data.sort_values(["symbol", "date"])
        .groupby(["symbol", "month"], as_index=False)
        .agg(
            first_trade_date=("date", "min"),
            last_trade_date=("date", "max"),
            trading_days=("date", "nunique"),
            isin=("isin", "last"),
            security_name=("security_name", "last"),
            close=("close", "last"),
            open_first=("open", "first"),
            high_month=("high", "max"),
            low_month=("low", "min"),
            volume=("volume", "sum"),
            traded_value=("traded_value", "sum"),
            num_trades=("num_trades", "sum"),
        )
    )
    monthly = monthly.rename(columns={"month": "date"})
    monthly["return_1m"] = monthly.groupby("symbol")["close"].pct_change()
    return monthly.sort_values(["symbol", "date"]).reset_index(drop=True)


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    paths = sorted(input_dir.glob("*.zip"))
    if not paths:
        raise FileNotFoundError(f"No ZIP files found in {input_dir}")

    daily = combine_udiff_bhavcopies(paths, eq_only=True)
    daily = daily.drop_duplicates(["date", "symbol", "series"]).sort_values(["symbol", "date"])
    monthly = build_monthly_panel(daily)

    daily_output = Path(args.daily_output)
    monthly_output = Path(args.monthly_output)
    daily_output.parent.mkdir(parents=True, exist_ok=True)
    monthly_output.parent.mkdir(parents=True, exist_ok=True)

    daily.to_csv(daily_output, index=False)
    monthly.to_csv(monthly_output, index=False)

    print(f"Input ZIP files: {len(paths)}")
    print(f"Daily EQ rows: {len(daily):,}")
    print(f"Trading dates: {daily['date'].nunique():,}")
    print(f"Unique symbols: {daily['symbol'].nunique():,}")
    print(f"Monthly rows: {len(monthly):,}")
    print(f"Saved daily panel: {daily_output}")
    print(f"Saved monthly panel: {monthly_output}")


if __name__ == "__main__":
    main()
