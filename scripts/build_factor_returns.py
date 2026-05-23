"""Build factor returns from a monthly stock-level panel.

Usage example:

    python scripts/build_factor_returns.py --input data/processed/monthly_panel.csv --output outputs/factor_returns/factor_returns.csv

The input panel should include:

- date
- symbol
- universe
- return_1m
- market_cap

Optional but recommended:

- book_value_equity
- traded_value
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
    include_value = {"book_value_equity", "market_cap"}.issubset(panel.columns)
    panel = add_core_signals(panel, include_value=include_value)

    weight_col = "market_cap" if args.value_weighted and "market_cap" in panel.columns else None
    factors = construct_standard_factors(panel, weight_col=weight_col)
    factors.to_csv(output_path, index=False)
    print(f"Saved factor returns to {output_path}")


if __name__ == "__main__":
    main()
