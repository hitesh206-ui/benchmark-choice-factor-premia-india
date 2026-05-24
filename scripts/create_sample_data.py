"""Create a small synthetic monthly panel for testing the research pipeline.

This file does not create real empirical evidence. It only makes the repository
runnable before official NSE/public data files are collected locally.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2018-01-31", "2025-12-31", freq="M")
    symbols = [f"STOCK{i:03d}" for i in range(1, 151)]
    universes = ["liquid_nse_universe", "nifty_50", "nifty_100", "nifty_500"]

    rows = []
    for symbol_index, symbol in enumerate(symbols):
        base_market_cap = rng.lognormal(mean=10.0, sigma=1.0)
        price = rng.uniform(50, 1000)
        for date in dates:
            monthly_return = rng.normal(loc=0.01, scale=0.08)
            price = max(1.0, price * (1.0 + monthly_return))
            traded_value = rng.lognormal(mean=14.0, sigma=1.0)
            market_cap = base_market_cap * price * rng.uniform(0.9, 1.1)

            if symbol_index < 50:
                universe = "nifty_50"
            elif symbol_index < 100:
                universe = "nifty_100"
            elif symbol_index < 140:
                universe = "nifty_500"
            else:
                universe = "liquid_nse_universe"

            rows.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "universe": universe,
                    "close": price,
                    "return_1m": monthly_return,
                    "volume": rng.integers(10000, 1000000),
                    "traded_value": traded_value,
                    "market_cap": market_cap,
                    "book_value_equity": market_cap * rng.uniform(0.2, 1.2),
                }
            )

    panel = pd.DataFrame(rows)
    output_path = Path("data/processed/monthly_panel.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(output_path, index=False)
    print(f"Saved synthetic sample panel to {output_path}")
    print("Warning: this is fake sample data for testing only, not empirical evidence.")


if __name__ == "__main__":
    main()
