"""Build first empirical momentum and low-volatility factors from monthly NSE panel.

This script is designed for the first broad-NSE empirical test before market-cap
and book-value data are available.

It uses:
- trailing 12-1 momentum signal
- trailing 12-month volatility signal
- next-month return as the realized factor return
- a broad liquid universe based on prior average traded value

Example:

    python scripts/build_momentum_lowvol_factors.py \
      --input data/processed/monthly_panel_eq_2025_2026.csv \
      --output outputs/factor_returns/momentum_lowvol_factors.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.portfolio_sorts import (
    assign_quantile_buckets,
    calculate_bucket_returns,
    calculate_long_short_return,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build momentum and low-volatility factors.")
    parser.add_argument("--input", required=True, help="Monthly panel CSV.")
    parser.add_argument("--output", required=True, help="Output factor returns CSV.")
    parser.add_argument("--liquidity-percentile", type=float, default=0.20)
    parser.add_argument("--buckets", type=int, default=5)
    return parser.parse_args()


def add_forward_returns(panel: pd.DataFrame) -> pd.DataFrame:
    """Add next-month realized returns for each symbol."""
    df = panel.sort_values(["symbol", "date"]).copy()
    df["forward_return_1m"] = df.groupby("symbol")["return_1m"].shift(-1)
    return df


def add_liquid_universe_flag(
    panel: pd.DataFrame,
    liquidity_percentile: float,
) -> pd.DataFrame:
    """Flag broad liquid universe using prior 12-month average traded value."""
    df = panel.copy()
    liquidity_col = "avg_monthly_traded_value_12m"
    if liquidity_col not in df.columns:
        raise ValueError(f"Missing required liquidity column: {liquidity_col}")

    threshold = df.groupby("date")[liquidity_col].transform(lambda x: x.quantile(liquidity_percentile))
    df["universe"] = "liquid_nse_universe"
    df["liquidity_filter_pass"] = df[liquidity_col] >= threshold
    return df[df["liquidity_filter_pass"]].copy()


def build_factor(
    panel: pd.DataFrame,
    signal_col: str,
    factor_name: str,
    long_bucket: int,
    short_bucket: int,
    n_buckets: int,
) -> pd.DataFrame:
    """Build one long-short factor from a signal and forward returns."""
    required = ["date", "symbol", signal_col, "forward_return_1m"]
    missing = [col for col in required if col not in panel.columns]
    if missing:
        raise ValueError(f"Missing columns for {factor_name}: {missing}")

    data = panel.dropna(subset=[signal_col, "forward_return_1m"]).copy()
    if data.empty:
        return pd.DataFrame(columns=["date", "factor_return", "universe", "factor_name", "weighting_method"])

    sorted_data = assign_quantile_buckets(
        data,
        signal_col=signal_col,
        date_col="date",
        n_buckets=n_buckets,
        label_col="bucket",
    )
    bucket_returns = calculate_bucket_returns(
        sorted_data,
        return_col="forward_return_1m",
        bucket_col="bucket",
        date_col="date",
        weight_col=None,
    )
    factor_returns = calculate_long_short_return(
        bucket_returns,
        date_col="date",
        bucket_col="bucket",
        return_col="portfolio_return",
        long_bucket=long_bucket,
        short_bucket=short_bucket,
        output_col="factor_return",
    )
    factor_returns["universe"] = "liquid_nse_universe"
    factor_returns["factor_name"] = factor_name
    factor_returns["weighting_method"] = "equal_weighted"
    return factor_returns


def main() -> None:
    args = parse_args()
    panel = pd.read_csv(args.input, parse_dates=["date"])
    panel = add_forward_returns(panel)
    panel = add_liquid_universe_flag(panel, liquidity_percentile=args.liquidity_percentile)

    frames = [
        build_factor(
            panel,
            signal_col="momentum_signal_12_1",
            factor_name="momentum_wml_12_1",
            long_bucket=args.buckets,
            short_bucket=1,
            n_buckets=args.buckets,
        ),
        build_factor(
            panel,
            signal_col="volatility_12m",
            factor_name="low_volatility",
            long_bucket=1,
            short_bucket=args.buckets,
            n_buckets=args.buckets,
        ),
    ]
    factors = pd.concat(frames, ignore_index=True)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    factors.to_csv(output_path, index=False)

    print(f"Input monthly rows: {len(panel):,}")
    print(f"Factor rows: {len(factors):,}")
    print(f"Factor months: {factors['date'].nunique() if not factors.empty else 0:,}")
    print(f"Saved factor returns: {output_path}")


if __name__ == "__main__":
    main()
