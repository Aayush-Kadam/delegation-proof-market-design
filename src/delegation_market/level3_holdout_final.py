"""Finalize the frozen Level 3 holdout after completeness is established."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def finalize(input_path: Path, output: Path) -> dict:
    cells = pd.read_csv(input_path)
    revenue = (
        (cells["delta_full_ndl_revenue_mean"] <= -0.05)
        & (cells["delta_full_ndl_revenue_ci_high"] < 0)
    )
    allocation = (
        revenue
        & (cells["delta_full_dl_ae_mean"] >= 0.01)
        & (cells["delta_full_dl_ae_ci_low"] > 0)
    )
    welfare = (
        revenue
        & (cells["delta_full_dl_welfare_mean"] >= 0.005)
        & (cells["delta_full_dl_welfare_ci_low"] > 0)
    )
    cells = cells.assign(primary_gate=allocation | welfare)
    passing = cells[cells.primary_gate].copy()
    passing["joint_magnitude"] = (
        passing["delta_full_ndl_revenue_mean"].abs()
        + passing["delta_full_dl_ae_mean"].abs()
        + passing["delta_full_dl_welfare_mean"].abs()
    )
    strongest = passing.sort_values("joint_magnitude", ascending=False).iloc[0]
    fields = [
        "v_low", "horizon", "c_high", "c_low", "step", "n_seeds",
        "delta_full_ndl_revenue_mean", "delta_full_ndl_revenue_ci_low",
        "delta_full_ndl_revenue_ci_high", "delta_full_dl_ae_mean",
        "delta_full_dl_ae_ci_low", "delta_full_dl_ae_ci_high",
        "delta_full_dl_welfare_mean", "delta_full_dl_welfare_ci_low",
        "delta_full_dl_welfare_ci_high",
    ]
    verdict = {
        "candidate_commit": "241577f",
        "rule": "Frozen C3 directional objective-conflict holdout gate",
        "holdout_verdict": "PASS",
        "level_3_verdict": "MIXED",
        "level_3_constraint": "SUBSTANTIAL OVERLAP novelty audit caps the overall verdict",
        "total_cells": int(len(cells)),
        "revenue_fpa_cells": int(revenue.sum()),
        "allocation_gate_cells": int(allocation.sum()),
        "welfare_gate_cells": int(welfare.sum()),
        "primary_gate_union_cells": int(cells.primary_gate.sum()),
        "strongest_passing_cell": {key: float(strongest[key]) for key in fields},
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "primary_candidate_verdict.json").write_text(
        json.dumps(verdict, indent=2) + "\n", encoding="utf-8"
    )
    cells.to_csv(output / "primary_candidate_cell_classification.csv", index=False)

    counts = cells.pivot_table(
        index="v_low", columns="horizon", values="primary_gate", aggfunc="sum"
    ).sort_index().sort_index(axis=1)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), constrained_layout=True)
    image = axes[0].imshow(counts.to_numpy(), cmap="Blues", vmin=0, vmax=5, aspect="auto")
    axes[0].set_title("Passing rate-factor cells")
    axes[0].set_xlabel("Horizon")
    axes[0].set_ylabel("Low value")
    axes[0].set_xticks(range(len(counts.columns)), [f"{int(x):,}" for x in counts.columns])
    axes[0].set_yticks(range(len(counts.index)), [f"{x:.1f}" for x in counts.index])
    for i in range(counts.shape[0]):
        for j in range(counts.shape[1]):
            axes[0].text(j, i, f"{int(counts.iloc[i, j])}/5", ha="center", va="center",
                         color="white" if counts.iloc[i, j] >= 3 else "#17202a", fontweight="bold")
    fig.colorbar(image, ax=axes[0], shrink=.8, label="Passing rate pairs (of 5)")

    colors = np.where(cells.primary_gate, "#2166ac", "#b8bec6")
    axes[1].scatter(cells["delta_full_ndl_revenue_mean"], cells["delta_full_dl_ae_mean"],
                    c=colors, edgecolors="#17202a", linewidths=.35, s=34)
    axes[1].axvline(-.05, color="#444444", linestyle="--", linewidth=1)
    axes[1].axhline(.01, color="#444444", linestyle="--", linewidth=1)
    axes[1].set_title("Revenue vs allocation-error contrast")
    axes[1].set_xlabel("Delta normalized revenue loss (FPA - SPA)")
    axes[1].set_ylabel("Delta allocation error (FPA - SPA)")

    axes[2].scatter(cells["delta_full_ndl_revenue_mean"], cells["delta_full_dl_welfare_mean"],
                    c=colors, edgecolors="#17202a", linewidths=.35, s=34)
    axes[2].axvline(-.05, color="#444444", linestyle="--", linewidth=1)
    axes[2].axhline(.005, color="#444444", linestyle="--", linewidth=1)
    axes[2].set_title("Revenue vs welfare-loss contrast")
    axes[2].set_xlabel("Delta normalized revenue loss (FPA - SPA)")
    axes[2].set_ylabel("Delta welfare loss (FPA - SPA)")
    fig.suptitle("Frozen Level 3 holdout objective-conflict surface", fontsize=14, fontweight="bold")
    fig.text(.5, -.01, "75 frozen cells; 30 paired seeds per cell. Blue satisfies the preregistered directional gate.", ha="center")
    fig.savefig(output / "objective_conflict_surface.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return verdict


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(finalize(args.input, args.output), indent=2))


if __name__ == "__main__":
    main()
