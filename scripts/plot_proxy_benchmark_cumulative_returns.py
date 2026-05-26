"""Plot cumulative factor returns by proxy benchmark universe.

This script handles multiple universes for the same factor by creating one line
per universe-factor pair.

Example:

    python scripts/plot_proxy_benchmark_cumulative_returns.py \
      --input outputs/factor_returns/proxy_benchmark_factor_returns_2021_2026.csv \
      --output outputs/figures/proxy_benchmark_cumulative_2021_2026.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot cumulative factor returns by proxy benchmark universe."
    )
    parser.add_argument("--input", required=True, help="Input factor return CSV.")
    parser.add_argument("--output", required=True, help="Output PNG path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, parse_dates=["date"])
    if df.empty:
        raise ValueError("Input factor return file is empty.")

    required = {"date", "factor_return", "universe", "factor_name"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.sort_values(["factor_name", "universe", "date"]).copy()
    df["line_name"] = df["factor_name"] + " | " + df["universe"]
    df["cumulative_return"] = df.groupby("line_name")["factor_return"].transform(
        lambda x: (1.0 + x).cumprod() - 1.0
    )

    wide = df.pivot_table(
        index="date",
        columns="line_name",
        values="cumulative_return",
        aggfunc="last",
    ).sort_index()

    ax = wide.plot(figsize=(12, 7))
    ax.set_title("Cumulative Factor Returns by Proxy Benchmark Universe")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Factor | Universe", fontsize=8)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved proxy benchmark cumulative return chart: {output_path}")


if __name__ == "__main__":
    main()
