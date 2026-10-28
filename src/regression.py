"""
Panel-regression.

Two-way fixed-effects PanelOLS with cluster-robust SEs at the entity level.
CPI-U deflator for converting nominal to dollars.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS


@dataclass
class RegressionResult:
    name: str
    n_obs: int
    n_entities: int
    r2_within: float
    coef_table: pd.DataFrame

    def as_markdown(self) -> str:
        return (
            f"### {self.name}\n\n"
            f"- Observations: {self.n_obs:,}\n"
            f"- Entities: {self.n_entities:,}\n"
            f"- Within R²: {self.r2_within:.3f}\n\n"
            + self.coef_table.round(4).to_markdown()
        )


def _to_panel(df: pd.DataFrame, entity: str = "unitid", time: str = "year") -> pd.DataFrame:
    df = df.copy()
    df[time] = pd.to_numeric(df[time], errors="coerce").astype("Int64")
    df = df.dropna(subset=[entity, time])
    return df.set_index([entity, time])


def fixed_effects_panel(
    df: pd.DataFrame,
    dependent: str,
    regressors: Iterable[str],
    entity_effects: bool = True,
    time_effects: bool = True,
    cluster_entity: bool = True,
    name: str = "panel",
) -> RegressionResult:
    panel_df = _to_panel(df)
    regressors = list(regressors)
    both = pd.concat([panel_df[dependent], panel_df[regressors]], axis=1).dropna()
    y = both[dependent]
    X = both[regressors]
    model = PanelOLS(y, X,
                     entity_effects=entity_effects,
                     time_effects=time_effects,
                     drop_absorbed=True)
    res = model.fit(cov_type="clustered", cluster_entity=cluster_entity)
    ci = res.conf_int()
    table = pd.DataFrame({
        "coef": res.params, "stderr": res.std_errors,
        "tstat": res.tstats, "pvalue": res.pvalues,
        "ci_low": ci["lower"], "ci_high": ci["upper"],
    })
    return RegressionResult(
        name=name, n_obs=int(res.nobs),
        n_entities=int(res.entity_info.total),
        r2_within=float(res.rsquared_within),
        coef_table=table,
    )


# CPI-U annual averages, US City Average (1982-84 = 100). Source: BLS.
_CPI = {
    2003: 184.0, 2004: 188.9, 2005: 195.3, 2006: 201.6, 2007: 207.3,
    2008: 215.3, 2009: 214.5, 2010: 218.1, 2011: 224.9, 2012: 229.6,
    2013: 233.0, 2014: 236.7, 2015: 237.0, 2016: 240.0, 2017: 245.1,
    2018: 251.1, 2019: 255.7, 2020: 258.8, 2021: 271.0, 2022: 292.7,
    2023: 304.7, 2024: 313.7,
}


def deflate_to_real_dollars(df: pd.DataFrame, dollar_cols: Iterable[str],
                            year_col: str = "year", base_year: int = 2023) -> pd.DataFrame:
    base = _CPI[base_year]
    scale = pd.Series({y: base / v for y, v in _CPI.items()})
    scale_series = df[year_col].map(scale)
    out = df.copy()
    for c in dollar_cols:
        out[c + "_real"] = out[c] * scale_series
    return out
