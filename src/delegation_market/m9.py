"""Crash-safe runner for the M9 hybrid-payment mechanism campaign."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

from delegation_market.agents import HedgeAgent
from delegation_market.heterogeneous import AGENTS
from delegation_market.level3 import _atomic_json, file_hash
from delegation_market.mechanisms import run_auction
from delegation_market.simulation import counterfactual_rewards


def run_id(spec):
    payload = json.dumps(spec, separators=(",", ":"), sort_keys=True).encode()
    return "m9-" + hashlib.sha256(payload).hexdigest()[:24]


def load_design(root: Path, config_path: Path):
    cfg = json.loads(config_path.read_text())
    source = json.loads((root / cfg["source_environment_config"]).read_text())
    return cfg, source["environments"]


def tasks(root: Path, config_path: Path, stage: str, alphas=None):
    cfg, environments = load_design(root, config_path)
    if stage == "development":
        env_ids, seeds = cfg["development_environment_ids"], cfg["development_seeds"]
        chosen = cfg["coarse_alphas"] if alphas is None else alphas
    elif stage == "holdout":
        env_ids, seeds = cfg["holdout_environment_ids"], cfg["holdout_seeds"]
        if alphas is None:
            raise ValueError("holdout requires explicitly frozen alphas")
        chosen = alphas
    elif stage == "refinement":
        env_ids, seeds = cfg["development_environment_ids"], cfg["development_seeds"]
        if alphas is None:
            raise ValueError("refinement requires explicitly frozen alphas")
        chosen = alphas
    else:
        raise ValueError(f"unknown stage: {stage}")
    out = []
    for high, low in cfg["profiles"]:
        for env_id in env_ids:
            env = environments[env_id]
            for seed in seeds:
                for alpha in chosen:
                    out.append({"stage": stage, "learner_high": high, "learner_low": low,
                                "environment_id": int(env_id), "v_low": env["v_low"],
                                "horizon": env["horizon"], "c_high": env["c_high"],
                                "c_low": env["c_low"], "seed": int(seed),
                                "alpha": float(alpha), "bid_step": cfg["bid_step"],
                                "tail_share": cfg["tail_share"]})
    return out


def _make_agents(spec):
    v, horizon, step = spec["v_low"], spec["horizon"], spec["bid_step"]
    grids = [np.round(np.arange(0, 1 + step / 2, step), 10),
             np.round(np.arange(0, v + step / 2, step), 10)]
    etas = [spec["c_high"] * math.sqrt(math.log(len(grids[0])) / horizon),
            spec["c_low"] * math.sqrt(math.log(len(grids[1])) / horizon)]
    seed = spec["seed"]
    agents = [AGENTS[spec["learner_high"]](1, grids[0], etas[0], 2 * seed),
              AGENTS[spec["learner_low"]](v, grids[1], etas[1], 2 * seed + 1)]
    return agents, grids


def run_job(spec):
    agents, grids = _make_agents(spec)
    rng = np.random.default_rng(spec["seed"] + 10000)
    values = np.array([1.0, spec["v_low"]])
    sums = {"revenue": 0.0, "welfare": 0.0, "high_win": 0.0, "bidder_surplus": 0.0}
    tail_start = int((1 - spec["tail_share"]) * spec["horizon"])
    bid_h, bid_l = np.zeros(len(grids[0])), np.zeros(len(grids[1]))
    start = time.perf_counter()
    for t in range(spec["horizon"]):
        bids = np.array([agent.act() for agent in agents])
        result = run_auction(bids, "hybrid", alpha=spec["alpha"], rng=rng)
        rewards = result.allocations * values - result.payments
        for i, agent in enumerate(agents):
            rv = counterfactual_rewards(agent, i, bids, "hybrid", 0, spec["alpha"])
            agent.update(bids[i], rewards[i], rv)
        sums["revenue"] += float(result.payments.sum())
        sums["welfare"] += float(result.allocations @ values)
        sums["high_win"] += float(result.allocations[0])
        sums["bidder_surplus"] += float(rewards.sum())
        if t >= tail_start:
            bid_h[np.abs(grids[0] - bids[0]).argmin()] += 1
            bid_l[np.abs(grids[1] - bids[1]).argmin()] += 1
    return {"run_id": run_id(spec), **spec,
            **{key: value / spec["horizon"] for key, value in sums.items()},
            "regret_high": agents[0].diagnostics()["external_regret"] / spec["horizon"],
            "regret_low": agents[1].diagnostics()["external_regret"] / spec["horizon"],
            "tail_bid_high": bid_h.tolist(), "tail_bid_low": bid_l.tolist(),
            "runtime_seconds": time.perf_counter() - start}


def valid(path: Path, spec, config_hash: str):
    try:
        row = json.loads(path.read_text())
    except Exception:
        return False
    return row.get("run_id") == run_id(spec) and row.get("config_hash") == config_hash


def execute(root: Path, config_path: Path, stage: str, alphas=None, workers=4, max_jobs=None):
    config_hash = file_hash(config_path)
    expected = tasks(root, config_path, stage, alphas)
    parts = root / "results" / "m9" / stage / "runs"
    parts.mkdir(parents=True, exist_ok=True)
    pending = [spec for spec in expected
               if not valid(parts / f"{run_id(spec)}.json", spec, config_hash)]
    if max_jobs is not None:
        pending = pending[:max_jobs]
    completed = len(expected) - len([spec for spec in expected
                                    if not valid(parts / f"{run_id(spec)}.json", spec, config_hash)])
    start = time.perf_counter()
    checkpoint = root / "results" / "m9" / stage / "checkpoint.json"
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_job, spec): spec for spec in pending}
        for future in as_completed(futures):
            row = future.result()
            row["config_hash"] = config_hash
            _atomic_json(parts / f"{row['run_id']}.json", row)
            completed += 1
            _atomic_json(checkpoint, {"status": "running", "stage": stage,
                         "expected": len(expected), "completed": completed,
                         "remaining": len(expected) - completed, "workers": workers,
                         "failures": 0, "retries": 0, "pool_restarts": 0,
                         "config_hash": config_hash})
    status = "complete" if completed == len(expected) else "shard_complete"
    _atomic_json(checkpoint, {"status": status, "stage": stage, "expected": len(expected),
                 "completed": completed, "remaining": len(expected) - completed,
                 "workers": workers, "failures": 0, "retries": 0,
                 "pool_restarts": 0, "config_hash": config_hash,
                 "runtime_seconds": time.perf_counter() - start})
    return completed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stage", choices=["development", "refinement", "holdout"], required=True)
    parser.add_argument("--alphas", type=float, nargs="*")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-jobs", type=int)
    args = parser.parse_args()
    print(execute(args.root, args.config, args.stage, args.alphas, args.workers, args.max_jobs))
