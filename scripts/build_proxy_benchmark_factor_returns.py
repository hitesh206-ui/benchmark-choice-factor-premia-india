"""Build factor returns across public-data proxy benchmark universes.

This script creates monthly Top-50, Top-100, and Top-500 proxy benchmark
universes from the NSE monthly panel using lagged 12-month average traded value.
It then computes equal-weighted long-short factor returns for:

- Momentum WML 12-1
- Low-volatility

Important disclosure:
These are public-data benchmark proxies, not official historical Nifty 50,
Nifty 100, or Nifty 500 constituent histories. They are designed to avoid
survivorship bias using only information available in the monthly NSE panel.

Example:

    python scripts/build_proxy_benchmark_factor_returns.py \
      --input data/processed/monthly_panel_eq_2021_2026.csv \
      --output outputs/factor_returns/proxy_benchmark_factor_returns_2021_2026.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "symbol",
    "return_1m",
    "momentum_signal_12_1",
    "volatility_12m",
    "avg_monthly_traded_value_12m",
]

PROXY_UNIVERSES = {
    "top50_proxy": 50,
    "top100_proxy": 100,
    "top500_proxy": 500,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build factor returns across proxy benchmark universes."
    )
    parser.add_argument("--input", required=True, help="Input monthly panel CSV.")
    parser.add_argument("--output", required=True, help="Output factor return CSV.")
    parser.add_argument(
        "--min-universe-size",
        type=int,
        default=30,
        help="Minimum number of stocks required in a universe-month.",
    )
    parser.add_argument(
        "--quantile",
        type=float,
        default=0.3,
        help="Long/short quantile size. Default 0.3 means top/bottom 30 percent.",
    )
    return parser.parse_args()


def check_required_columns(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def prepare_panel(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    check_required_columns(df)

    # Forward return is the realized next-month return earned after forming
    # portfolios using signals known at the current month-end.
    df = df.sort_values(["symbol", "date"]).copy()
    df["forward_return_1m"] = df.groupby("symbol")["return_1m"].shift(-1)

    df = df.dropna(
        subset=[
            "momentum_signal_12_1",
            "volatility_12m",
            "avg_monthly_traded_value_12m",
            "forward_return_1m",
        ]
    ).copy()

    # Keep only stocks with positive lagged trading value.
    df = df[df["avg_monthly_traded_value_12m"] > 0].copy()
    return df


def add_proxy_universe_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Assign top-N proxy universes each month by lagged liquidity."""
    ranked = df.sort_values(
        ["date", "avg_monthly_traded_value_12m", "symbol"],
        ascending=[True, False, True],
    ).copy()
    ranked["liquidity_rank"] = ranked.groupby("date")["avg_monthly_traded_value_12m"].rank(
        method="first", ascending=False
    )
    return ranked


def long_short_return(
    df: pd.DataFrame,
    signal_col: str,
    factor_name: str,
    universe_name: str,
    high_signal_is_long: bool,
    quantile: float,
    min_universe_size: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for date, group in df.groupby("date"):
        group = group.dropna(subset=[signal_col, "forward_return_1m"]).copy()
        n = len(group)
        if n < min_universe_size:
            continue

        leg_size = int(n * quantile)
        if leg_size < 1:
            continue

        sorted_group = group.sort_values(signal_col, ascending=True)

        if high_signal_is_long:
            short_leg = sorted_group.head(leg_size)
            long_leg = sorted_group.tail(leg_size)
        else:
            long_leg = sorted_group.head(leg_size)
            short_leg = sorted_group.tail(leg_size)

        factor_return = long_leg["forward_return_1m"].mean() - short_leg["forward_return_1m"].mean()

        rows.append(
            {
                "date": date,
                "factor_return": factor_return,
                "universe": universe_name,
                "factor_name": factor_name,
                "weighting_method": "equal_weighted",
                "long_leg_count": len(long_leg),
                "short_leg_count": len(short_leg),
                "universe_count": n,
                "universe_construction": "public_data_proxy_by_lagged_12m_traded_value",
            }
        )

    return rows


def build_all_factor_returns(
    df: pd.DataFrame,
    quantile: float,
    min_universe_size: int,
) -> pd.DataFrame:
    labelled = add_proxy_universe_labels(df)
    all_rows: list[dict[str, object]] = []

    universe_specs: list[tuple[str, pd.DataFrame]] = [("liquid_nse_universe", labelled)]

    for universe_name, top_n in PROXY_UNIVERSES.items():
        universe_df = labelled[labelled["liquidity_rank"] <= top_n].copy()
        universe_specs.append((universe_name, universe_df))

    for universe_name, universe_df in universe_specs:
        all_rows.extend(
            long_short_return(
                universe_df,
                signal_col="momentum_signal_12_1",
                factor_name="momentum_wml_12_1",
                universe_name=universe_name,
                high_signal_is_long=True,
                quantile=quantile,
                min_universe_size=min_universe_size,
            )
        )
        all_rows.extend(
            long_short_return(
                universe_df,
                signal_col="volatility_12m",
                factor_name="low_volatility",
                universe_name=universe_name,
                high_signal_is_long=False,
                quantile=quantile,
                min_universe_size=min_universe_size,
            )
        )

    result = pd.DataFrame(all_rows)
    if result.empty:
        raise ValueError("No factor returns were created. Check filters and input data.")

    return result.sort_values(["universe", "factor_name", "date"]).reset_index(drop=True)


def main() -> None:
    args = parse_args()
    panel = prepare_panel(args.input)
    factor_returns = build_all_factor_returns(
        panel,
        quantile=args.quantile,
        min_universe_size=args.min_universe_size,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    factor_returns.to_csv(output_path, index=False)

    print(f"Input rows after required filters: {len(panel):,}")
    print(f"Factor rows: {len(factor_returns):,}")
    print(f"Universes: {factor_returns['universe'].nunique():,}")
    print(f"Factors: {factor_returns['factor_name'].nunique():,}")
    for universe, group in factor_returns.groupby("universe"):
        print(f"{universe}: {group['date'].nunique():,} factor months")
    print(f"Saved proxy benchmark factor returns: {output_path}")


if __name__ == "__main__":
    main()
