"""Build a monthly stock-level panel from a raw price-volume file.

Usage example:

    python scripts/build_monthly_panel.py --input data/raw/prices.csv --output data/processed/monthly_panel.csv

Expected minimum input columns:

- date
- symbol
- close

Optional input columns:

- volume
- traded_value
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.cleaning import standardize_columns
from src.panel_builder import add_traded_value, to_month_end_panel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build monthly stock panel.")
    parser.add_argument("--input", required=True, help="Path to raw CSV file.")
    parser.add_argument("--output", required=True, help="Path to output CSV file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(input_path)
    raw = standardize_columns(raw)

    if "traded_value" not in raw.columns and {"close", "volume"}.issubset(raw.columns):
        raw = add_traded_value(raw, price_col="close", volume_col="volume")

    monthly = to_month_end_panel(
        raw,
        symbol_col="symbol",
        date_col="date",
        price_col="close",
        volume_col="volume" if "volume" in raw.columns else None,
        traded_value_col="traded_value" if "traded_value" in raw.columns else None,
    )
    monthly.to_csv(output_path, index=False)
    print(f"Saved monthly panel to {output_path}")


if __name__ == "__main__":
    main()
