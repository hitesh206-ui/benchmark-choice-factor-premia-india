"""Plotting utilities for factor-premia analysis."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_cumulative_returns(
    data: pd.DataFrame,
    date_col: str = "date",
    return_col: str = "factor_return",
    group_col: str = "universe",
    title: str = "Cumulative Factor Returns",
    output_path: str | Path | None = None,
) -> None:
    """Plot cumulative returns by group."""
    df = data.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    fig, ax = plt.subplots(figsize=(10, 6))
    for group, group_df in df.groupby(group_col):
        group_df = group_df.sort_values(date_col)
        cumulative = (1.0 + group_df[return_col].fillna(0)).cumprod() - 1.0
        ax.plot(group_df[date_col], cumulative, label=str(group))
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative return")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_drawdowns(
    data: pd.DataFrame,
    date_col: str = "date",
    return_col: str = "factor_return",
    group_col: str = "universe",
    title: str = "Factor Drawdowns",
    output_path: str | Path | None = None,
) -> None:
    """Plot drawdowns by group."""
    df = data.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    fig, ax = plt.subplots(figsize=(10, 6))
    for group, group_df in df.groupby(group_col):
        group_df = group_df.sort_values(date_col)
        wealth = (1.0 + group_df[return_col].fillna(0)).cumprod()
        drawdown = wealth / wealth.cummax() - 1.0
        ax.plot(group_df[date_col], drawdown, label=str(group))
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_factor_correlation_heatmap(
    data: pd.DataFrame,
    date_col: str = "date",
    return_col: str = "factor_return",
    group_col: str = "universe",
    title: str = "Factor Correlation Across Universes",
    output_path: str | Path | None = None,
) -> None:
    """Plot correlation heatmap across groups."""
    df = data.copy()
    wide = df.pivot(index=date_col, columns=group_col, values=return_col)
    corr = wide.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    image = ax.imshow(corr, aspect="auto")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.index)
    ax.set_title(title)
    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
    plt.close(fig)
