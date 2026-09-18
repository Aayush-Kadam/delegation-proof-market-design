"""Crash-safe M10 gap-adaptive hybrid campaign."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

from delegation_market.heterogeneous import AGENTS
from delegation_market.level3 import _atomic_json, file_hash
from delegation_market.mechanisms import gap_adaptive_alpha, run_auction
from delegation_market.simulation import counterfactual_rewards


def run_id(spec):
    return "m10-" + hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:24]


def load_design(root, config):
    cfg = json.loads(config.read_text())
    envs = json.loads((root / cfg["source_environment_config"]).read_text())["environments"]
    return cfg, envs


def tasks(root, config, pairs=None, stage="development"):
    cfg, envs = load_design(root, config)
    if stage != "development":
        raise ValueError("candidate holdout requires a separately frozen config")
    chosen = pairs or [(a, tau) for a in cfg["a_values"] for tau in cfg["tau_values"]]
    return [{"stage": stage, "learner_high": high, "learner_low": low,
             "environment_id": int(eid), "v_low": envs[eid]["v_low"],
             "horizon": envs[eid]["horizon"], "c_high": envs[eid]["c_high"],
             "c_low": envs[eid]["c_low"], "seed": int(seed), "a": float(a),
             "tau": float(tau), "bid_step": cfg["bid_step"], "tail_share": cfg["tail_share"]}
            for high, low in cfg["profiles"] for eid in cfg["development_environment_ids"]
            for seed in cfg["development_seeds"] for a, tau in chosen]


def _agents(spec):
    v, horizon, step = spec["v_low"], spec["horizon"], spec["bid_step"]
    grids = [np.round(np.arange(0, 1 + step / 2, step), 10),
             np.round(np.arange(0, v + step / 2, step), 10)]
    etas = [spec["c_high"] * math.sqrt(math.log(len(grids[0])) / horizon),
            spec["c_low"] * math.sqrt(math.log(len(grids[1])) / horizon)]
    seed = spec["seed"]
    return [AGENTS[spec["learner_high"]](1, grids[0], etas[0], 2 * seed),
            AGENTS[spec["learner_low"]](v, grids[1], etas[1], 2 * seed + 1)]


def run_job(spec):
    agents = _agents(spec)
    rng = np.random.default_rng(spec["seed"] + 10000)
    values = np.array([1.0, spec["v_low"]])
    sums = {"revenue": 0.0, "welfare": 0.0, "high_win": 0.0,
            "bidder_surplus": 0.0, "normalized_gap": 0.0, "realized_alpha": 0.0}
    start = time.perf_counter()
    for _ in range(spec["horizon"]):
        bids = np.array([agent.act() for agent in agents])
        top, second = float(np.max(bids)), float(np.min(bids))
        gap = 0.0 if top == 0 else (top - second) / top
        weight = gap_adaptive_alpha(top, second, spec["a"], spec["tau"])
        result = run_auction(bids, "gap_adaptive", alpha=spec["a"], tau=spec["tau"], rng=rng)
        rewards = result.allocations * values - result.payments
        for i, agent in enumerate(agents):
            rv = counterfactual_rewards(agent, i, bids, "gap_adaptive", 0, spec["a"], spec["tau"])
            agent.update(bids[i], rewards[i], rv)
        sums["revenue"] += float(result.payments.sum())
        sums["welfare"] += float(result.allocations @ values)
        sums["high_win"] += float(result.allocations[0])
        sums["bidder_surplus"] += float(rewards.sum())
        sums["normalized_gap"] += gap
        sums["realized_alpha"] += weight
    return {"run_id": run_id(spec), **spec,
            **{key: val / spec["horizon"] for key, val in sums.items()},
            "regret_high": agents[0].diagnostics()["external_regret"] / spec["horizon"],
            "regret_low": agents[1].diagnostics()["external_regret"] / spec["horizon"],
            "runtime_seconds": time.perf_counter() - start}


def valid(path, spec, config_hash):
    try: row = json.loads(path.read_text())
    except Exception: return False
    return row.get("run_id") == run_id(spec) and row.get("config_hash") == config_hash


def execute(root, config, workers=4, max_jobs=None):
    expected = tasks(root, config); config_hash = file_hash(config)
    parts = root / "results/m10/development/runs"; parts.mkdir(parents=True, exist_ok=True)
    pending = [s for s in expected if not valid(parts / f"{run_id(s)}.json", s, config_hash)]
    if max_jobs is not None: pending = pending[:max_jobs]
    completed = len(expected) - sum(not valid(parts / f"{run_id(s)}.json", s, config_hash) for s in expected)
    checkpoint = root / "results/m10/development/checkpoint.json"; start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_job, spec): spec for spec in pending}
        for future in as_completed(futures):
            row = future.result(); row["config_hash"] = config_hash
            _atomic_json(parts / f"{row['run_id']}.json", row); completed += 1
            _atomic_json(checkpoint, {"status":"running","expected":len(expected),"completed":completed,
                         "remaining":len(expected)-completed,"workers":workers,"failures":0,"retries":0,
                         "pool_restarts":0,"config_hash":config_hash})
    _atomic_json(checkpoint, {"status":"complete" if completed==len(expected) else "shard_complete",
                 "expected":len(expected),"completed":completed,"remaining":len(expected)-completed,
                 "workers":workers,"failures":0,"retries":0,"pool_restarts":0,"config_hash":config_hash,
                 "runtime_seconds":time.perf_counter()-start})
    return completed


if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--config",type=Path,required=True)
    p.add_argument("--workers",type=int,default=4);p.add_argument("--max-jobs",type=int);a=p.parse_args()
    print(execute(a.root,a.config,a.workers,a.max_jobs))
