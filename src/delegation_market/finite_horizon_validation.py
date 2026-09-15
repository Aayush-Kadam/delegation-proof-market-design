"""Prospectively frozen M2.5 finite-horizon Hedge validation."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .agents import HedgeAgent
from .simulation import counterfactual_rewards


HORIZONS = (10_000, 25_000, 50_000, 100_000, 200_000)
MECHANISMS = ("first_price", "second_price")
RIVAL_CYCLE = np.array((.10, .35, .60, .85, .45, .70, .20, .95))
BLOCK = 37


def rival_bid(t: int) -> float:
    return float(RIVAL_CYCLE[(t // BLOCK) % len(RIVAL_CYCLE)])


def reward_vector(grid: np.ndarray, mechanism: str, opponent_bid: float) -> np.ndarray:
    dummy = HedgeAgent(1.0, grid, eta=.01, seed=0)
    return counterfactual_rewards(dummy, 0, [0.0, opponent_bid], mechanism, 0.0, 1.0)


def run_stratum(mechanism: str, horizon: int, seeds: int = 30) -> tuple[dict, list[dict]]:
    grid = np.linspace(0.0, 1.0, 101)
    eta = math.sqrt(8.0 * math.log(len(grid)) / horizon)
    log_weights = np.zeros(len(grid))
    cumulative = np.zeros(len(grid))
    exact_reward = 0.0
    sampled_reward = np.zeros(seeds)
    uniforms = np.vstack([np.random.default_rng(s).random(horizon) for s in range(seeds)])
    reward_min, reward_max = math.inf, -math.inf
    for t in range(horizon):
        z = log_weights - log_weights.max()
        policy = np.exp(z); policy /= policy.sum()
        rv = reward_vector(grid, mechanism, rival_bid(t))
        reward_min = min(reward_min, float(rv.min()))
        reward_max = max(reward_max, float(rv.max()))
        exact_reward += float(policy @ rv)
        sampled_actions = np.searchsorted(np.cumsum(policy), uniforms[:, t], side="right")
        sampled_reward += rv[np.minimum(sampled_actions, len(grid)-1)]
        cumulative += rv
        log_weights = eta * cumulative
    best = float(cumulative.max())
    exact_regret = best - exact_reward
    bound = math.log(len(grid)) / eta + eta * horizon / 8.0
    base = {"mechanism": mechanism, "horizon": horizon, "K": len(grid), "eta": eta,
            "best_fixed_reward": best, "exact_expected_reward": exact_reward,
            "exact_expected_regret": exact_regret, "theoretical_bound": bound,
            "normalized_exact_regret": exact_regret / bound,
            "reward_min": reward_min, "reward_max": reward_max}
    rows = [{**base, "seed": s, "realized_reward": float(sampled_reward[s]),
             "realized_regret": best-float(sampled_reward[s])} for s in range(seeds)]
    return base, rows


def execute(root: Path, protocol_hash: str, seeds: int = 30) -> tuple[pd.DataFrame, dict]:
    started = time.perf_counter(); summaries=[]; rows=[]
    for mechanism in MECHANISMS:
        for horizon in HORIZONS:
            summary, sample_rows = run_stratum(mechanism, horizon, seeds)
            summaries.append(summary); rows.extend(sample_rows)
    runtime = time.perf_counter()-started
    out = root/"results"/"finite_horizon_validation"; out.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows); frame["protocol_hash"] = protocol_hash
    frame.to_csv(out/"seed_results.csv", index=False)
    summary_frame = pd.DataFrame(summaries); summary_frame.to_csv(out/"summary.csv", index=False)
    passed = bool((summary_frame.normalized_exact_regret <= 1.0 + 1e-12).all() and
                  (summary_frame.reward_min >= -1e-12).all() and
                  (summary_frame.reward_max <= 1.0 + 1e-12).all())
    manifest = {"experiment_id":"M2.5-FINITE-HORIZON-VALIDATION", "protocol_hash":protocol_hash,
                "timestamp":datetime.now(timezone.utc).isoformat(), "seeds":seeds,
                "mechanisms":list(MECHANISMS), "horizons":list(HORIZONS),
                "total_rounds":seeds*len(MECHANISMS)*sum(HORIZONS),
                "exact_policy_rounds":len(MECHANISMS)*sum(HORIZONS),
                "runtime_seconds":runtime, "pass":passed, "python":platform.python_version()}
    (out/"manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return summary_frame, manifest


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--root",type=Path); parser.add_argument("--protocol-hash",required=True); parser.add_argument("--seeds",type=int,default=30)
    args=parser.parse_args(); root=args.root or Path(__file__).resolve().parents[2]
    summary, manifest=execute(root,args.protocol_hash,args.seeds)
    print(summary.to_string(index=False)); print(json.dumps(manifest,indent=2))


if __name__ == "__main__": main()
