"""Build factor returns from a monthly stock-level panel.

Usage example:

    python scripts/build_factor_returns.py \
      --input data/processed/monthly_panel_eq.csv \
      --output outputs/factor_returns/factor_returns.csv

The current public-data workflow can build price-volume factors first:

- momentum_wml
- low_volatility

Size and value factors require market_cap and book_value_equity inputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.factor_construction import construct_standard_factors
from src.signal_builder import add_core_signals


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build factor return series.")
    parser.add_argument("--input", required=True, help="Path to processed monthly panel CSV.")
    parser.add_argument("--output", required=True, help="Path to output factor returns CSV.")
    parser.add_argument(
        "--universe-name",
        default="broad_nse_eq_universe",
        help="Universe label to use if the input panel has no universe column.",
    )
    parser.add_argument(
        "--value-weighted",
        action="store_true",
        help="Use market-cap weights where available.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(input_path, parse_dates=["date"])

    if "universe" not in panel.columns:
        panel["universe"] = args.universe_name

    include_value = {"book_value_equity", "market_cap"}.issubset(panel.columns)

    # Reuse the panel-builder's strict ex-ante signals when available.
    # Otherwise compute default signals from the monthly panel.
    if "momentum_signal_12_1" in panel.columns and "momentum_signal" not in panel.columns:
        panel["momentum_signal"] = panel["momentum_signal_12_1"]

    needs_core_signals = "momentum_signal" not in panel.columns or "volatility_12m" not in panel.columns
    if needs_core_signals:
        panel = add_core_signals(panel, include_value=include_value)
    elif include_value and "book_to_market" not in panel.columns:
        panel = add_core_signals(panel, include_value=True)

    weight_col = "market_cap" if args.value_weighted and "market_cap" in panel.columns else None
    factors = construct_standard_factors(panel, weight_col=weight_col)

    if factors.empty:
        print("No factor returns were produced. Check that the panel has non-missing signals and returns.")
    else:
        print(f"Factor rows: {len(factors):,}")
        print(f"Factors: {', '.join(sorted(factors['factor_name'].dropna().unique()))}")
        print(f"Months: {factors['date'].nunique():,}")

    factors.to_csv(output_path, index=False)
    print(f"Saved factor returns to {output_path}")


if __name__ == "__main__":
    main()
