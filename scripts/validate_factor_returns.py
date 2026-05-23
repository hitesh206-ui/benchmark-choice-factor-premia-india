"""Validate factor-return file and export a validation report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.validation import validate_factor_returns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate factor returns.")
    parser.add_argument("--input", required=True, help="Path to factor returns CSV.")
    parser.add_argument("--output", default="outputs/tables/factor_returns_validation.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input, parse_dates=["date"])
    report = validate_factor_returns(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved validation report to {output_path}")


if __name__ == "__main__":
    main()
