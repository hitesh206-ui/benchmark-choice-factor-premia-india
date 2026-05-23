"""Portfolio sorting utilities for factor construction."""

from __future__ import annotations

import pandas as pd


def assign_quantile_buckets(
    data: pd.DataFrame,
    signal_col: str,
    date_col: str = "date",
    n_buckets: int = 5,
    label_col: str = "bucket",
) -> pd.DataFrame:
    """Assign cross-sectional quantile buckets by date.

    Parameters
    ----------
    data:
        Panel data containing date and signal columns.
    signal_col:
        Column used for sorting securities.
    date_col:
        Date column used for month-by-month cross-sectional sorting.
    n_buckets:
        Number of quantile buckets.
    label_col:
        Name of output bucket column.
    """
    df = data.copy()

    def _bucket(group: pd.DataFrame) -> pd.Series:
        valid = group[signal_col].notna()
        result = pd.Series(index=group.index, dtype="float")
        if valid.sum() < n_buckets:
            return result
        result.loc[valid] = pd.qcut(
            group.loc[valid, signal_col],
            q=n_buckets,
            labels=False,
            duplicates="drop",
        ) + 1
        return result

    df[label_col] = df.groupby(date_col, group_keys=False).apply(_bucket)
    return df


def calculate_bucket_returns(
    data: pd.DataFrame,
    return_col: str,
    bucket_col: str,
    date_col: str = "date",
    weight_col: str | None = None,
) -> pd.DataFrame:
    """Calculate periodic portfolio returns by date and bucket."""
    df = data.dropna(subset=[return_col, bucket_col]).copy()

    if weight_col is None:
        grouped = df.groupby([date_col, bucket_col])[return_col].mean()
    else:
        def _weighted_return(group: pd.DataFrame) -> float:
            weights = group[weight_col].fillna(0)
            if weights.sum() == 0:
                return group[return_col].mean()
            return (group[return_col] * weights).sum() / weights.sum()

        grouped = df.groupby([date_col, bucket_col]).apply(_weighted_return)

    return grouped.rename("portfolio_return").reset_index()


def calculate_long_short_return(
    bucket_returns: pd.DataFrame,
    date_col: str = "date",
    bucket_col: str = "bucket",
    return_col: str = "portfolio_return",
    long_bucket: int | float = 5,
    short_bucket: int | float = 1,
    output_col: str = "factor_return",
) -> pd.DataFrame:
    """Calculate long-short factor returns from bucket returns."""
    wide = bucket_returns.pivot(index=date_col, columns=bucket_col, values=return_col)
    if long_bucket not in wide.columns or short_bucket not in wide.columns:
        raise ValueError("Requested long or short bucket not found in bucket returns.")
    out = wide[long_bucket] - wide[short_bucket]
    return out.rename(output_col).reset_index()
