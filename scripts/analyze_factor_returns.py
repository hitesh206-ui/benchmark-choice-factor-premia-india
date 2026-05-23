"""Analyze factor returns and export summary statistics.

Usage example:

    python scripts/analyze_factor_returns.py --input outputs/factor_returns/factor_returns.csv --output outputs/tables/factor_summary.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.performance_metrics import summarize_returns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze factor returns.")
    parser.add_argument("--input", required=True, help="Path to factor returns CSV.")
    parser.add_argument("--output", required=True, help="Path to output summary CSV.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    factors = pd.read_csv(input_path, parse_dates=["date"])
    required = {"universe", "factor_name", "factor_return"}
    missing = required.difference(factors.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    rows = []
    for (universe, factor_name), group in factors.groupby(["universe", "factor_name"]):
        metrics = summarize_returns(group["factor_return"])
        metrics["universe"] = universe
        metrics["factor_name"] = factor_name
        rows.append(metrics)

    summary = pd.DataFrame(rows)
    order = ["universe", "factor_name"] + [c for c in summary.columns if c not in {"universe", "factor_name"}]
    summary = summary[order]
    summary.to_csv(output_path, index=False)
    print(f"Saved factor summary to {output_path}")


if __name__ == "__main__":
    main()
