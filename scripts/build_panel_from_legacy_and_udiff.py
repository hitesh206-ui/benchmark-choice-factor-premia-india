"""Build a combined monthly panel from legacy NSE bhavcopy and UDiFF files.

Example:

    python scripts/build_panel_from_legacy_and_udiff.py \
      --legacy-dir data/raw/legacy_bhavcopy \
      --udiff-dir data/raw/udiff_bhavcopy \
      --daily-output data/interim/standardized_daily_eq_2021_2026.csv \
      --monthly-output data/processed/monthly_panel_eq_2021_2026.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.nse_legacy_bhavcopy import combine_legacy_bhavcopies
from src.nse_udiff_bhavcopy import combine_udiff_bhavcopies


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build combined NSE legacy + UDiFF monthly panel.")
    parser.add_argument("--legacy-dir", default="data/raw/legacy_bhavcopy")
    parser.add_argument("--udiff-dir", default="data/raw/udiff_bhavcopy")
    parser.add_argument("--daily-output", default="data/interim/standardized_daily_eq_2021_2026.csv")
    parser.add_argument("--monthly-output", default="data/processed/monthly_panel_eq_2021_2026.csv")
    return parser.parse_args()


def build_monthly_panel(daily: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily EQ data to symbol-month level and add factor signals."""
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
    monthly = monthly.sort_values(["symbol", "date"]).reset_index(drop=True)

    monthly["return_1m"] = monthly.groupby("symbol")["close"].pct_change()

    shifted_return = monthly.groupby("symbol")["return_1m"].shift(1)
    monthly["momentum_signal_12_1"] = (
        (1.0 + shifted_return)
        .groupby(monthly["symbol"])
        .rolling(window=12, min_periods=12)
        .apply(lambda x: x.prod() - 1.0, raw=False)
        .reset_index(level=0, drop=True)
    )

    monthly["volatility_12m"] = (
        shifted_return.groupby(monthly["symbol"])
        .rolling(window=12, min_periods=12)
        .std()
        .reset_index(level=0, drop=True)
    )

    monthly["avg_monthly_traded_value_12m"] = (
        monthly.groupby("symbol")["traded_value"]
        .shift(1)
        .groupby(monthly["symbol"])
        .rolling(window=12, min_periods=12)
        .mean()
        .reset_index(level=0, drop=True)
    )

    return monthly.sort_values(["symbol", "date"]).reset_index(drop=True)


def main() -> None:
    args = parse_args()
    legacy_paths = sorted(Path(args.legacy_dir).glob("*.zip"))
    udiff_paths = sorted(Path(args.udiff_dir).glob("*.zip"))

    if not legacy_paths:
        raise FileNotFoundError(f"No legacy ZIP files found in {args.legacy_dir}")
    if not udiff_paths:
        raise FileNotFoundError(f"No UDiFF ZIP files found in {args.udiff_dir}")

    legacy_daily = combine_legacy_bhavcopies(legacy_paths, eq_only=True)
    udiff_daily = combine_udiff_bhavcopies(udiff_paths, eq_only=True)

    common_cols = sorted(set(legacy_daily.columns).intersection(set(udiff_daily.columns)))
    daily = pd.concat([legacy_daily[common_cols], udiff_daily[common_cols]], ignore_index=True)
    daily = daily.drop_duplicates(["date", "symbol", "series"]).sort_values(["symbol", "date"])

    monthly = build_monthly_panel(daily)

    daily_output = Path(args.daily_output)
    monthly_output = Path(args.monthly_output)
    daily_output.parent.mkdir(parents=True, exist_ok=True)
    monthly_output.parent.mkdir(parents=True, exist_ok=True)

    daily.to_csv(daily_output, index=False)
    monthly.to_csv(monthly_output, index=False)

    print(f"Legacy ZIP files: {len(legacy_paths):,}")
    print(f"UDiFF ZIP files: {len(udiff_paths):,}")
    print(f"Combined daily EQ rows: {len(daily):,}")
    print(f"Trading dates: {daily['date'].nunique():,}")
    print(f"Unique symbols: {daily['symbol'].nunique():,}")
    print(f"Monthly rows: {len(monthly):,}")
    print(f"Months: {monthly['date'].nunique():,}")
    print(f"Rows with 12-1 momentum signal: {monthly['momentum_signal_12_1'].notna().sum():,}")
    print(f"Rows with 12m volatility signal: {monthly['volatility_12m'].notna().sum():,}")
    print(f"Saved daily panel: {daily_output}")
    print(f"Saved monthly panel: {monthly_output}")


if __name__ == "__main__":
    main()
