"""Plot cumulative factor returns from a factor-return CSV.

Example:

    python scripts/plot_factor_cumulative_returns.py \
      --input outputs/factor_returns/momentum_lowvol_factors_2024_2026.csv \
      --output outputs/figures/momentum_lowvol_cumulative_2024_2026.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot cumulative factor returns.")
    parser.add_argument("--input", required=True, help="Input factor returns CSV.")
    parser.add_argument("--output", required=True, help="Output PNG path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, parse_dates=["date"])
    if df.empty:
        raise ValueError("Input factor returns file is empty.")

    df = df.sort_values(["factor_name", "date"]).copy()
    df["cumulative_return"] = df.groupby("factor_name")["factor_return"].transform(
        lambda x: (1.0 + x).cumprod() - 1.0
    )

    wide = df.pivot(index="date", columns="factor_name", values="cumulative_return")

    ax = wide.plot(figsize=(9, 5))
    ax.set_title("Cumulative Factor Returns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Factor")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved cumulative return chart: {output_path}")


if __name__ == "__main__":
    main()
