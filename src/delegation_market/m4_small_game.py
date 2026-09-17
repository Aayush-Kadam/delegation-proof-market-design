"""Exact tiny-grid mean-field Hedge analysis for M4 (no Monte Carlo)."""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd


def payoff_matrices(mechanism: str, v_low: float, step: float):
    high = np.arange(0, 1 + step / 2, step)
    low = np.arange(0, v_low + step / 2, step)
    uh = np.zeros((len(high), len(low)))
    ul = np.zeros_like(uh)
    revenue = np.zeros_like(uh)
    high_win = np.zeros_like(uh)
    for i, bh in enumerate(high):
        for j, bl in enumerate(low):
            ph = 1.0 if bh > bl else (0.5 if bh == bl else 0.0)
            pl = 1 - ph
            if mechanism == "first_price":
                uh[i, j] = ph * (1 - bh); ul[i, j] = pl * (v_low - bl)
                revenue[i, j] = ph * bh + pl * bl
            elif mechanism == "second_price":
                uh[i, j] = ph * (1 - bl); ul[i, j] = pl * (v_low - bh)
                revenue[i, j] = min(bh, bl)
            else:
                raise ValueError(mechanism)
            high_win[i, j] = ph
    return high, low, uh, ul, revenue, high_win


def exact_payoff_table(mechanism: str, v_low: float, step: float) -> dict:
    high, low, uh, ul, revenue, high_win = payoff_matrices(mechanism, v_low, step)
    rational = lambda a: [[str(Fraction(float(x)).limit_denominator()) for x in row] for row in a]
    return {
        "mechanism": mechanism, "v_high": 1, "v_low": v_low,
        "high_actions": high.tolist(), "low_actions": low.tolist(),
        "high_payoff": rational(uh), "low_payoff": rational(ul),
        "revenue": rational(revenue), "high_win_probability": rational(high_win),
    }


def mean_field_hedge(mechanism: str, v_low: float, horizon: int, c_high=1.0, c_low=1.0, step=.25):
    high, low, uh, ul, revenue, high_win = payoff_matrices(mechanism, v_low, step)
    eta_h = c_high * math.sqrt(math.log(len(high)) / horizon)
    eta_l = c_low * math.sqrt(math.log(len(low)) / horizon)
    log_h = np.zeros(len(high)); log_l = np.zeros(len(low))
    totals = {"revenue": 0.0, "high_win": 0.0, "welfare": 0.0,
              "surplus_high": 0.0, "surplus_low": 0.0}
    for _ in range(horizon):
        ph = np.exp(log_h - log_h.max()); ph /= ph.sum()
        pl = np.exp(log_l - log_l.max()); pl /= pl.sum()
        joint = np.outer(ph, pl)
        totals["revenue"] += float((joint * revenue).sum())
        totals["high_win"] += float((joint * high_win).sum())
        totals["welfare"] += float((joint * (v_low + (1-v_low)*high_win)).sum())
        totals["surplus_high"] += float((joint * uh).sum())
        totals["surplus_low"] += float((joint * ul).sum())
        log_h += eta_h * (uh @ pl)
        log_l += eta_l * (ph @ ul)
    return {"mechanism": mechanism, "v_low": v_low, "horizon": horizon,
            "c_high": c_high, "c_low": c_low, "step": step,
            **{key: value / horizon for key, value in totals.items()},
            "terminal_expected_bid_high": float(ph @ high),
            "terminal_expected_bid_low": float(pl @ low)}


def analyze(output: Path):
    output.mkdir(parents=True, exist_ok=True)
    matrices = [exact_payoff_table(m, .5, .25) for m in ("first_price", "second_price")]
    (output / "payoff_matrices.json").write_text(json.dumps(matrices, indent=2) + "\n", encoding="utf-8")
    rows = [mean_field_hedge(m, v, h, ch, cl)
            for v in (.25, .5, .75)
            for h in (25, 100, 400, 1600)
            for ch, cl in ((1., 1.), (.5, 1.), (1., .5), (1., 2.), (2., 1.))
            for m in ("first_price", "second_price")]
    raw = pd.DataFrame(rows); raw.to_csv(output / "mean_field_results.csv", index=False)
    keys = ["v_low", "horizon", "c_high", "c_low", "step"]
    fpa = raw[raw.mechanism == "first_price"].set_index(keys)
    spa = raw[raw.mechanism == "second_price"].set_index(keys)
    summary = fpa[[]].copy()
    for metric in ("revenue", "high_win", "welfare", "surplus_high", "surplus_low"):
        summary[f"delta_{metric}"] = fpa[metric] - spa[metric]
    summary["delta_ndl_revenue"] = -summary.delta_revenue / summary.index.get_level_values("v_low")
    summary["delta_allocation_loss"] = -(fpa.high_win - spa.high_win)
    summary["delta_welfare_loss"] = -(fpa.welfare - spa.welfare)
    summary = summary.reset_index()
    summary["sign_conflict"] = (summary.delta_ndl_revenue < 0) & (summary.delta_allocation_loss > 0)
    summary.to_csv(output / "mean_field_contrasts.csv", index=False)
    verdict = {
        "cells": len(summary),
        "revenue_favors_fpa": int((summary.delta_ndl_revenue < 0).sum()),
        "allocation_favors_spa": int((summary.delta_allocation_loss > 0).sum()),
        "sign_conflict": int(summary.sign_conflict.sum()),
        "by_value": summary.groupby("v_low").sign_conflict.agg(["sum", "count"]).reset_index().to_dict("records"),
        "interpretation": "Exact deterministic mean-field Hedge on a .25 grid; explanatory, not confirmatory evidence.",
    }
    (output / "verdict.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
    return verdict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(analyze(args.output), indent=2))


if __name__ == "__main__":
    main()
