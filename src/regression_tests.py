"""Regression utilities for testing factor premia across benchmark universes."""

from __future__ import annotations

import pandas as pd
import statsmodels.api as sm


def run_ols(
    data: pd.DataFrame,
    dependent_col: str,
    independent_cols: list[str],
    add_constant: bool = True,
    cov_type: str = "HAC",
    maxlags: int = 3,
):
    """Run OLS regression with optional HAC/Newey-West standard errors.

    Parameters
    ----------
    data:
        Input dataframe.
    dependent_col:
        Name of dependent variable.
    independent_cols:
        List of independent variables.
    add_constant:
        Whether to add an intercept.
    cov_type:
        Covariance estimator. Default uses HAC for time-series factor returns.
    maxlags:
        Number of lags for HAC standard errors.
    """
    required = [dependent_col] + independent_cols
    df = data.dropna(subset=required).copy()
    if df.empty:
        raise ValueError("No observations available after dropping missing values.")

    y = df[dependent_col]
    x = df[independent_cols]
    if add_constant:
        x = sm.add_constant(x)

    model = sm.OLS(y, x).fit(cov_type=cov_type, cov_kwds={"maxlags": maxlags})
    return model


def summarize_model(model) -> pd.DataFrame:
    """Return a compact coefficient summary from a fitted statsmodels object."""
    return pd.DataFrame(
        {
            "coef": model.params,
            "std_error": model.bse,
            "t_stat": model.tvalues,
            "p_value": model.pvalues,
        }
    )
