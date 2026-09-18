"""Completeness, Pareto, regret, and role-sensitivity analysis for M9."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from delegation_market.level3 import _atomic_json, file_hash
from delegation_market.m9 import run_id, tasks


OBJECTIVES = ["revenue", "high_win", "welfare", "bidder_surplus"]


def validate(root: Path, config: Path, stage: str, alphas=None):
    expected = tasks(root, config, stage, alphas)
    expected_ids = {run_id(spec): spec for spec in expected}
    parts = root / "results/m9" / stage / "runs"
    config_hash = file_hash(config)
    rows, corrupt, mismatch, duplicates, unexpected = [], [], [], [], []
    seen = set()
    for path in parts.glob("*.json") if parts.exists() else []:
        try:
            row = json.loads(path.read_text())
        except Exception:
            corrupt.append(path.name)
            continue
        rid = row.get("run_id")
        if rid in seen:
            duplicates.append(rid)
            continue
        seen.add(rid)
        if rid not in expected_ids:
            unexpected.append(rid)
            continue
        spec = expected_ids[rid]
        identity = all(row.get(key) == value for key, value in spec.items())
        if not identity or row.get("config_hash") != config_hash:
            mismatch.append(rid)
            continue
        rows.append(row)
    valid_ids = {row["run_id"] for row in rows}
    missing = sorted(set(expected_ids) - valid_ids)
    report = {"expected": len(expected), "unique_valid": len(rows), "missing": len(missing),
              "duplicates": len(duplicates), "corrupt": len(corrupt),
              "identity_mismatches": len(mismatch), "unexpected": len(unexpected),
              "config_hash": config_hash, "complete": len(rows) == len(expected) and not any(
                  [missing, duplicates, corrupt, mismatch, unexpected])}
    return pd.DataFrame(rows), report


def _cvar(values, tail=.1):
    values = np.sort(np.asarray(values, float))
    n = max(1, int(np.ceil(tail * len(values))))
    return float(values[-n:].mean())


def summarize_development(rows: pd.DataFrame, revenue_floor=.1):
    group = ["alpha", "learner_high", "learner_low", "environment_id", "v_low",
             "horizon", "c_high", "c_low"]
    cells = rows.groupby(group, as_index=False)[OBJECTIVES].mean()
    endpoints = cells[cells.alpha.isin([0.0, 1.0])].groupby(
        group[1:], as_index=False)[["revenue", "high_win", "welfare"]].max()
    endpoints = endpoints.rename(columns={"revenue": "best_revenue", "high_win": "best_allocation",
                                          "welfare": "best_welfare"})
    cells = cells.merge(endpoints, on=group[1:], validate="many_to_one")
    cells["q_revenue"] = (cells.best_revenue - cells.revenue) / cells.v_low.clip(lower=revenue_floor)
    cells["q_allocation"] = cells.best_allocation - cells.high_win
    cells["q_welfare"] = cells.best_welfare - cells.welfare
    cells["q_joint"] = cells[["q_revenue", "q_allocation"]].max(axis=1)
    metrics = []
    for alpha, data in cells.groupby("alpha"):
        row = {"alpha": float(alpha)}
        for name in ["q_revenue", "q_allocation", "q_welfare", "q_joint"]:
            x = data[name].to_numpy()
            row.update({f"{name}_mean": float(np.mean(x)), f"{name}_median": float(np.median(x)),
                        f"{name}_p90": float(np.quantile(x, .9)),
                        f"{name}_p95": float(np.quantile(x, .95)),
                        f"{name}_worst": float(np.max(x)), f"{name}_cvar90": _cvar(x)})
        row.update({f"{name}_mean": float(data[name].mean()) for name in OBJECTIVES})
        metrics.append(row)
    return cells, pd.DataFrame(metrics).sort_values("alpha")


def select_candidate(frontier: pd.DataFrame, revenue_limit=.25, allocation_limit=.10):
    eligible = frontier[(frontier.q_revenue_worst <= revenue_limit) &
                        (frontier.q_allocation_worst <= allocation_limit)].copy()
    if eligible.empty:
        return None
    # Decimal alpha grids must preserve the prospective final tie-break rather
    # than inherit asymmetric binary floating-point representations.
    eligible["distance_half"] = (eligible.alpha - .5).abs().round(12)
    keys = ["q_joint_worst", "q_joint_cvar90", "q_joint_p95", "q_joint_mean",
            "distance_half", "alpha"]
    return eligible.sort_values(keys).iloc[0].to_dict()


def role_sensitivity(cells: pd.DataFrame):
    pairs = [("hedge", "ftpl"), ("hedge", "regret_matching"),
             ("ftpl", "regret_matching")]
    records = []
    keys = ["alpha", "environment_id"]
    for x, y in pairs:
        xy = cells[(cells.learner_high == x) & (cells.learner_low == y)]
        yx = cells[(cells.learner_high == y) & (cells.learner_low == x)]
        merged = xy.merge(yx, on=keys, suffixes=("_xy", "_yx"))
        for alpha, data in merged.groupby("alpha"):
            sr = np.abs(data.revenue_xy - data.revenue_yx)
            sa = np.abs(data.high_win_xy - data.high_win_yx)
            records.append({"pair": f"{x}/{y}", "alpha": alpha,
                            "S_R_median": float(np.median(sr)), "S_R_p95": float(np.quantile(sr, .95)),
                            "S_A_median": float(np.median(sa)), "S_A_p95": float(np.quantile(sa, .95))})
    return pd.DataFrame(records)


def analyze(root: Path, config: Path, stage: str, alphas=None):
    rows, integrity = validate(root, config, stage, alphas)
    if not integrity["complete"]:
        raise RuntimeError(f"incomplete {stage}: {integrity}")
    cfg = json.loads(config.read_text())
    cells, frontier = summarize_development(rows, cfg["revenue_normalizer_floor"])
    candidate = select_candidate(frontier, cfg["eligibility"]["worst_normalized_revenue_regret"],
                                 cfg["eligibility"]["worst_allocation_regret"])
    roles = role_sensitivity(cells)
    out = root / "results/m9" / stage / "analysis"
    figures = out / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    cells.to_csv(out / "cell_metrics.csv", index=False)
    frontier.to_csv(out / "frontier.csv", index=False)
    roles.to_csv(out / "role_sensitivity.csv", index=False)
    summary = {"stage": stage, "integrity": integrity, "candidate": candidate}
    _atomic_json(out / "summary.json", summary)
    _figures(frontier, cells, roles, figures, candidate)
    return summary


def _figures(frontier, cells, roles, out, candidate):
    plt.figure(figsize=(7, 5))
    plt.plot(frontier.high_win_mean, frontier.revenue_mean, "o-")
    for row in frontier.itertuples(): plt.annotate(f"{row.alpha:g}", (row.high_win_mean, row.revenue_mean))
    plt.xlabel("Mean allocation efficiency"); plt.ylabel("Mean seller revenue"); plt.tight_layout()
    plt.savefig(out / "M9-F1_pareto.png", dpi=180); plt.close()
    plt.figure(figsize=(7, 5)); plt.plot(frontier.alpha, frontier.q_joint_worst, "o-")
    plt.xlabel("alpha"); plt.ylabel("Worst-case normalized joint regret"); plt.tight_layout()
    plt.savefig(out / "M9-F2_worst_regret.png", dpi=180); plt.close()
    plt.figure(figsize=(7, 5)); plt.plot(frontier.alpha, frontier.q_joint_cvar90, "o-")
    plt.xlabel("alpha"); plt.ylabel("CVaR90 joint regret"); plt.tight_layout()
    plt.savefig(out / "M9-F3_tail_regret.png", dpi=180); plt.close()
    if candidate is not None:
        chosen = cells[cells.alpha.isin([0, candidate["alpha"], 1])]
        chosen.boxplot(column="q_joint", by="alpha", figsize=(7, 5)); plt.suptitle("")
        plt.ylabel("Cell joint regret"); plt.tight_layout()
        plt.savefig(out / "M9-F4_candidate_endpoints.png", dpi=180); plt.close()
        stress = chosen[chosen.v_low >= .7]
        stress.boxplot(column="q_joint", by="alpha", figsize=(7, 5)); plt.suptitle("")
        plt.ylabel("High-valuation joint regret"); plt.tight_layout()
        plt.savefig(out / "M9-F5_high_v_stress.png", dpi=180); plt.close()
    if not roles.empty:
        roles.pivot(index="pair", columns="alpha", values="S_R_median").plot(figsize=(8, 5))
        plt.ylabel("Median revenue role sensitivity"); plt.tight_layout()
        plt.savefig(out / "M9-F6_role_sensitivity.png", dpi=180); plt.close()
