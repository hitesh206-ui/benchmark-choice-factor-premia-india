"""Validate a monthly stock-level panel and export a validation report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.validation import check_duplicate_symbol_dates, validate_monthly_panel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate monthly panel.")
    parser.add_argument("--input", required=True, help="Path to monthly panel CSV.")
    parser.add_argument("--output", default="outputs/tables/monthly_panel_validation.json")
    parser.add_argument("--duplicates-output", default="outputs/tables/duplicate_symbol_dates.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input, parse_dates=["date"])
    report = validate_monthly_panel(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    duplicates = check_duplicate_symbol_dates(data)
    if not duplicates.empty:
        dup_path = Path(args.duplicates_output)
        dup_path.parent.mkdir(parents=True, exist_ok=True)
        duplicates.to_csv(dup_path, index=False)

    print(f"Saved validation report to {output_path}")


if __name__ == "__main__":
    main()
