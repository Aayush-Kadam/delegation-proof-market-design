"""Frozen Level-5 analysis, run only after the 4,500-record completeness gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


LEARNERS = ["hedge", "ftpl", "regret_matching"]


def ci95(values):
    x = np.asarray(values, dtype=float)
    mean = float(x.mean())
    half = 1.96 * float(x.std(ddof=1)) / np.sqrt(len(x))
    return mean, mean - half, mean + half


def median_ci(values, seed):
    x = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    boot = np.median(rng.choice(x, size=(20000, len(x)), replace=True), axis=1)
    return [float(np.median(x)), *map(float, np.quantile(boot, [0.025, 0.975]))]


def main(root: Path):
    out = root / "results/level_05/analysis"
    figs = out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(p.read_text()) for p in (root / "results/level_05/runs").glob("*.json")]
    df = pd.DataFrame(rows)
    assert len(df) == 4500 and df.run_id.nunique() == 4500
    idx = ["learner", "v_low", "horizon", "c_high", "c_low", "seed"]
    fpa = df[df.mechanism == "first_price"].set_index(idx)
    spa = df[df.mechanism == "second_price"].set_index(idx)
    assert fpa.index.is_unique and spa.index.is_unique and set(fpa.index) == set(spa.index)
    paired = pd.DataFrame(index=fpa.index).reset_index()
    paired["D_R"] = (fpa.revenue - spa.revenue).to_numpy()
    paired["D_A"] = (spa.high_win - fpa.high_win).to_numpy()
    paired["D_W"] = (spa.welfare - fpa.welfare).to_numpy()
    paired.to_csv(out / "paired_seed_gaps.csv", index=False)

    cell_keys = ["learner", "v_low", "horizon", "c_high", "c_low"]
    cell_rows = []
    for key, g in paired.groupby(cell_keys, sort=True):
        mr, lr, ur = ci95(g.D_R)
        ma, la, ua = ci95(g.D_A)
        mw, lw, uw = ci95(g.D_W)
        learner, v, h, ch, cl = key
        cell_rows.append(dict(learner=learner, v_low=v, horizon=h, c_high=ch, c_low=cl,
                              D_R=mr, D_R_ci_low=lr, D_R_ci_high=ur,
                              D_A=ma, D_A_ci_low=la, D_A_ci_high=ua,
                              D_W=mw, D_W_ci_low=lw, D_W_ci_high=uw,
                              conflict_pass=bool(mr / v >= .05 and ma >= .01 and lr > 0 and la > 0)))
    cells = pd.DataFrame(cell_rows)
    cells.to_csv(out / "cell_summary.csv", index=False)

    summaries = {}
    for j, learner in enumerate(LEARNERS):
        c = cells[cells.learner == learner]
        passes = int(c.conflict_pass.sum())
        med_r = median_ci(c.D_R, 5501 + j * 10)
        med_a = median_ci(c.D_A, 5502 + j * 10)
        med_w = median_ci(c.D_W, 5503 + j * 10)
        if passes >= 15 and med_r[0] > 0 and med_a[0] > 0:
            classification = "STRONG GENERALIZATION"
        elif (passes >= 10 or (med_r[0] > 0 and med_a[0] > 0)) and med_r[0] > 0 and med_a[0] > 0:
            classification = "PARTIAL GENERALIZATION"
        else:
            classification = "FAIL"
        regret = {}
        for mech in ["first_price", "second_price"]:
            d = df[(df.learner == learner) & (df.mechanism == mech)]
            regret[mech] = {
                "high_mean": float(d.regret_high.mean()), "high_median": float(d.regret_high.median()),
                "low_mean": float(d.regret_low.mean()), "low_median": float(d.regret_low.median())}
        by_v = {str(v): int(g.conflict_pass.sum()) for v, g in c.groupby("v_low")}
        by_h = {str(int(h)): {"passed": int(g.conflict_pass.sum()), "total": int(len(g))}
                for h, g in c.groupby("horizon")}
        summaries[learner] = {"classification": classification, "cells_passed": passes,
                              "median_D_R_ci95": med_r, "median_D_A_ci95": med_a,
                              "median_D_W_ci95": med_w, "support_by_valuation_out_of_5": by_v,
                              "support_by_horizon": by_h, "regret_per_round": regret}

    agreement = {}
    disagreements = []
    env_keys = ["v_low", "horizon", "c_high", "c_low"]
    for i, a in enumerate(LEARNERS):
        for b in LEARNERS[i + 1:]:
            ca = cells[cells.learner == a].set_index(env_keys)
            cb = cells[cells.learner == b].set_index(env_keys)
            agreement[f"{a}__{b}"] = {
                "revenue_sign_agreement": float((np.sign(ca.D_R) == np.sign(cb.D_R)).mean()),
                "allocation_sign_agreement": float((np.sign(ca.D_A) == np.sign(cb.D_A)).mean())}
            for env in ca.index:
                if np.sign(ca.loc[env, "D_R"]) != np.sign(cb.loc[env, "D_R"]) or np.sign(ca.loc[env, "D_A"]) != np.sign(cb.loc[env, "D_A"]):
                    disagreements.append({"learners": f"{a} vs {b}", "v_low": env[0], "horizon": env[1],
                                          "c_high": env[2], "c_low": env[3],
                                          "D_R_a": float(ca.loc[env, "D_R"]), "D_R_b": float(cb.loc[env, "D_R"]),
                                          "D_A_a": float(ca.loc[env, "D_A"]), "D_A_b": float(cb.loc[env, "D_A"])})
    pd.DataFrame(disagreements).to_csv(out / "learner_disagreements.csv", index=False)

    new = [summaries["ftpl"]["classification"], summaries["regret_matching"]["classification"]]
    if all(x != "FAIL" for x in new) and "STRONG GENERALIZATION" in new:
        verdict = "STRONG CROSS-LEARNER GENERALIZATION"
    elif all(summaries[x]["median_D_R_ci95"][0] > 0 and summaries[x]["median_D_A_ci95"][0] > 0 for x in ["ftpl", "regret_matching"]):
        verdict = "CROSS-LEARNER GENERALIZATION"
    elif sum(x != "FAIL" for x in new) == 1:
        verdict = "MIXED — LEARNER DEPENDENT"
    else:
        verdict = "HEDGE-SPECIFIC"
    summary = {"verdict": verdict, "learners": summaries, "sign_agreement": agreement,
               "completeness": {"expected": 4500, "unique": 4500, "missing": 0, "duplicates": 0, "corrupt": 0}}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    colors = ["#3569a8", "#e17c36", "#4b9b63"]
    plt.figure(figsize=(7, 4)); plt.bar(LEARNERS, [summaries[x]["cells_passed"] for x in LEARNERS], color=colors)
    plt.axhline(15, color="black", ls="--", lw=1); plt.ylabel("Conflict-gate cells (out of 25)"); plt.tight_layout(); plt.savefig(figs / "01_conflict_support.png", dpi=180); plt.close()
    plt.figure(figsize=(7, 4)); plt.boxplot([cells[cells.learner == x].D_R for x in LEARNERS], tick_labels=LEARNERS); plt.axhline(0, color="black", lw=1); plt.ylabel("D_R across environments"); plt.tight_layout(); plt.savefig(figs / "02_revenue_gaps.png", dpi=180); plt.close()
    plt.figure(figsize=(7, 4)); plt.boxplot([cells[cells.learner == x].D_A for x in LEARNERS], tick_labels=LEARNERS); plt.axhline(0, color="black", lw=1); plt.ylabel("D_A across environments"); plt.tight_layout(); plt.savefig(figs / "03_allocation_gaps.png", dpi=180); plt.close()
    heat = cells.pivot_table(index="learner", columns="v_low", values="conflict_pass", aggfunc="mean").loc[LEARNERS]
    plt.figure(figsize=(7, 3)); plt.imshow(heat, vmin=0, vmax=1, cmap="YlGn"); plt.xticks(range(len(heat.columns)), heat.columns); plt.yticks(range(3), LEARNERS); plt.colorbar(label="Share of 5 strata passing"); plt.xlabel("Low value"); plt.tight_layout(); plt.savefig(figs / "04_learner_valuation_heatmap.png", dpi=180); plt.close()

    rep = df[(df.v_low == .5) & (df.horizon == 25000) & (df.c_high == 1) & (df.c_low == .5)]
    fig, axes = plt.subplots(3, 2, figsize=(10, 8), sharex=True)
    for i, learner in enumerate(LEARNERS):
        for j, mech in enumerate(["first_price", "second_price"]):
            g = rep[(rep.learner == learner) & (rep.mechanism == mech)]
            hist = np.mean(np.vstack(g.tail_bid_high), axis=0); hist /= hist.sum()
            axes[i, j].plot(np.arange(len(hist)) / 100, hist, lw=1)
            axes[i, j].set_title(f"{learner}: {mech}"); axes[i, j].set_ylabel("Tail mass")
    axes[-1, 0].set_xlabel("High-bidder bid"); axes[-1, 1].set_xlabel("High-bidder bid")
    fig.suptitle("Representative terminal-tail bid distributions (not time trajectories)")
    fig.tight_layout(); fig.savefig(figs / "05_representative_tail_bid_distributions.png", dpi=180); plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, required=True)
    main(parser.parse_args().root)
