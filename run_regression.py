"""
Workshop demo  -  IPEDS RQ2:
  6-year graduation rate at 4-year institutions ~
      real per-FTE instruction spending
    + real per-FTE administrative spending
    + log(FTE)
    + sector dummies
  with two-way fixed effects and cluster-robust SEs at the institution level.

Reads parquets from ./data/ produced by the pre-workshop pull.

Usage (on OSPool via HTCondor, but also runs locally):
    python3 run_regression.py --out results/
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from src.regression import fixed_effects_panel, deflate_to_real_dollars


def load_parquets(prefix: str) -> pd.DataFrame:
    files = sorted(Path("data").glob(f"{prefix}__*.parquet"))
    if not files:
        raise FileNotFoundError(f"No parquets matched data/{prefix}__*.parquet")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def _safe_log(s):
    return np.log(pd.Series(s).replace([0, np.inf, -np.inf], np.nan))


def build_panel() -> pd.DataFrame:
    directory = load_parquets("directory")
    finance   = load_parquets("finance")
    grads_raw = load_parquets("grad-rates")

    # Overall bachelor's cohort: subcohort==2, race==99 (total), sex==99 (total).
    grads = grads_raw.query("subcohort == 2 & race == 99 & sex == 99")[
        ["unitid", "year", "completion_rate_150pct"]
    ]

    fin_cols = ["unitid", "year", "exp_instruc_total", "exp_inst_supp_total",
                "exp_acad_supp_total", "est_fte"]

    panel = (
        directory.query("sector in [1, 2, 3]")[["unitid", "year", "sector"]]
        .merge(grads, on=["unitid", "year"])
        .merge(finance[fin_cols], on=["unitid", "year"], how="left")
    )
    panel = deflate_to_real_dollars(
        panel,
        dollar_cols=["exp_instruc_total", "exp_inst_supp_total", "exp_acad_supp_total"],
        base_year=2023,
    )
    panel["admin_exp_real"] = (
        panel["exp_inst_supp_total_real"].fillna(0)
        + panel["exp_acad_supp_total_real"].fillna(0)
    )
    panel["fte_safe"] = panel["est_fte"].replace(0, np.nan)
    panel["instr_per_fte"] = panel["exp_instruc_total_real"] / panel["fte_safe"]
    panel["admin_per_fte"] = panel["admin_exp_real"] / panel["fte_safe"]
    panel["log_instr_per_fte"] = _safe_log(panel["instr_per_fte"])
    panel["log_admin_per_fte"] = _safe_log(panel["admin_per_fte"])
    panel["log_fte"] = _safe_log(panel["est_fte"])

    sec = pd.get_dummies(panel["sector"], prefix="sector", drop_first=True).astype(float)
    return pd.concat([panel, sec], axis=1).dropna(
        subset=["completion_rate_150pct", "log_instr_per_fte", "log_admin_per_fte", "log_fte"]
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("results"))
    args = ap.parse_args()
    args.out.mkdir(exist_ok=True)

    panel = build_panel()
    regs = ["log_instr_per_fte", "log_admin_per_fte", "log_fte"]
    regs += [c for c in panel.columns if c.startswith("sector_")]

    print(f"Panel: {len(panel):,} obs, {panel['unitid'].nunique():,} institutions, "
          f"years {panel['year'].min()}-{panel['year'].max()}", flush=True)

    res = fixed_effects_panel(
        panel, "completion_rate_150pct", regs,
        entity_effects=True, time_effects=True,
        name="RQ2  -  grad rate ~ spending mix",
    )
    res.coef_table.to_csv(args.out / "rq2_main.csv")
    pd.DataFrame([{"n_obs": res.n_obs, "n_entities": res.n_entities,
                   "r2_within": res.r2_within, "dep": "completion_rate_150pct"}]) \
        .to_csv(args.out / "rq2_meta.csv", index=False)
    print(res.as_markdown(), flush=True)


if __name__ == "__main__":
    main()
