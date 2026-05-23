"""Performance metric utilities for factor-return analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd


def annualized_return(returns: pd.Series, periods_per_year: int = 12) -> float:
    """Compute annualized compounded return from periodic returns."""
    clean = returns.dropna()
    if clean.empty:
        return np.nan
    cumulative = (1.0 + clean).prod()
    years = len(clean) / periods_per_year
    if years <= 0:
        return np.nan
    return cumulative ** (1.0 / years) - 1.0


def annualized_volatility(returns: pd.Series, periods_per_year: int = 12) -> float:
    """Compute annualized volatility from periodic returns."""
    clean = returns.dropna()
    if len(clean) < 2:
        return np.nan
    return clean.std(ddof=1) * np.sqrt(periods_per_year)


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 12,
) -> float:
    """Compute annualized Sharpe ratio."""
    excess = returns.dropna() - risk_free_rate / periods_per_year
    vol = annualized_volatility(excess, periods_per_year=periods_per_year)
    if pd.isna(vol) or vol == 0:
        return np.nan
    ann_excess = annualized_return(excess, periods_per_year=periods_per_year)
    return ann_excess / vol


def max_drawdown(returns: pd.Series) -> float:
    """Compute maximum drawdown from periodic returns."""
    clean = returns.dropna()
    if clean.empty:
        return np.nan
    wealth = (1.0 + clean).cumprod()
    running_max = wealth.cummax()
    drawdown = wealth / running_max - 1.0
    return drawdown.min()


def hit_rate(returns: pd.Series) -> float:
    """Compute the proportion of periods with positive returns."""
    clean = returns.dropna()
    if clean.empty:
        return np.nan
    return (clean > 0).mean()


def t_stat_mean(returns: pd.Series) -> float:
    """Compute t-statistic for whether the mean periodic return differs from zero."""
    clean = returns.dropna()
    if len(clean) < 2:
        return np.nan
    std_error = clean.std(ddof=1) / np.sqrt(len(clean))
    if std_error == 0:
        return np.nan
    return clean.mean() / std_error


def summarize_returns(returns: pd.Series, periods_per_year: int = 12) -> dict[str, float]:
    """Return a dictionary of common performance metrics."""
    clean = returns.dropna()
    return {
        "mean_return": clean.mean() if not clean.empty else np.nan,
        "annualized_return": annualized_return(clean, periods_per_year),
        "annualized_volatility": annualized_volatility(clean, periods_per_year),
        "sharpe_ratio": sharpe_ratio(clean, periods_per_year=periods_per_year),
        "max_drawdown": max_drawdown(clean),
        "skewness": clean.skew() if len(clean) > 2 else np.nan,
        "kurtosis": clean.kurtosis() if len(clean) > 3 else np.nan,
        "hit_rate": hit_rate(clean),
        "t_stat": t_stat_mean(clean),
        "observations": float(len(clean)),
    }
