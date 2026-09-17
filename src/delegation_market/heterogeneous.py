"""Crash-safe ordered heterogeneous-learner auction runner."""
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
from delegation_market.level3 import _atomic_json, file_hash
from delegation_market.level5 import FTPLAgent, RegretMatchingAgent
from delegation_market.mechanisms import run_auction
from delegation_market.simulation import counterfactual_rewards

AGENTS = {"hedge": HedgeAgent, "ftpl": FTPLAgent, "regret_matching": RegretMatchingAgent}


def make_agents(high_learner, low_learner, v, horizon, c_high, c_low, step, seed):
    grids = [np.round(np.arange(0, 1 + step / 2, step), 10),
             np.round(np.arange(0, v + step / 2, step), 10)]
    etas = [c_high * math.sqrt(math.log(len(grids[0])) / horizon),
            c_low * math.sqrt(math.log(len(grids[1])) / horizon)]
    agents = [AGENTS[high_learner](1, grids[0], etas[0], 2 * seed),
              AGENTS[low_learner](v, grids[1], etas[1], 2 * seed + 1)]
    return agents, grids


def job_id(spec):
    return "het-" + hashlib.sha256(json.dumps(spec, separators=(",", ":")).encode()).hexdigest()[:24]


def tasks(cfg):
    return [(p[0], p[1], m, e["v_low"], e["horizon"], e["c_high"], e["c_low"], s,
             cfg["bid_step"], cfg["tail_share"])
            for p in cfg["profiles"] for e in cfg["environments"] for s in cfg["seeds"]
            for m in cfg["mechanisms"]]


def run_job(spec):
    high_l, low_l, mech, v, horizon, ch, cl, seed, step, tail = spec
    agents, grids = make_agents(high_l, low_l, v, horizon, ch, cl, step, seed)
    rng = np.random.default_rng(seed + 10000)
    values = np.array([1.0, v])
    sums = {"revenue": 0.0, "welfare": 0.0, "high_win": 0.0}
    tail_start = int((1 - tail) * horizon)
    bid_h, bid_l = np.zeros(len(grids[0])), np.zeros(len(grids[1]))
    start = time.perf_counter()
    for t in range(horizon):
        bids = np.array([a.act() for a in agents])
        result = run_auction(bids, mech, rng=rng)
        rewards = result.allocations * values - result.payments
        for i, agent in enumerate(agents):
            agent.update(bids[i], rewards[i], counterfactual_rewards(agent, i, bids, mech, 0, 1))
        sums["revenue"] += float(result.payments.sum())
        sums["welfare"] += float(result.allocations @ values)
        sums["high_win"] += float(result.allocations[0])
        if t >= tail_start:
            bid_h[np.abs(grids[0] - bids[0]).argmin()] += 1
            bid_l[np.abs(grids[1] - bids[1]).argmin()] += 1
    return {"run_id": job_id(spec), "learner_high": high_l, "learner_low": low_l,
            "profile": f"{high_l}__{low_l}", "mechanism": mech, "v_low": v,
            "horizon": horizon, "c_high": ch, "c_low": cl, "seed": seed, "step": step,
            **{k: value / horizon for k, value in sums.items()},
            "regret_high": agents[0].diagnostics()["external_regret"] / horizon,
            "regret_low": agents[1].diagnostics()["external_regret"] / horizon,
            "tail_bid_high": bid_h.tolist(), "tail_bid_low": bid_l.tolist(),
            "runtime_seconds": time.perf_counter() - start}


def valid(path, rid):
    try:
        return json.loads(path.read_text()).get("run_id") == rid
    except Exception:
        return False


def execute(root, cfg_path, workers=4, max_jobs=None):
    cfg = json.loads(cfg_path.read_text())
    expected = tasks(cfg)
    parts = root / "results/heterogeneous/runs"
    parts.mkdir(parents=True, exist_ok=True)
    pending = [x for x in expected if not valid(parts / f"{job_id(x)}.json", job_id(x))]
    if max_jobs is not None:
        pending = pending[:max_jobs]
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_job, x): x for x in pending}
        for future in as_completed(futures):
            row = future.result()
            _atomic_json(parts / f"{row['run_id']}.json", row)
            completed = sum(valid(parts / f"{job_id(x)}.json", job_id(x)) for x in expected)
            _atomic_json(root / "results/heterogeneous/checkpoint.json", {
                "status": "running", "expected": len(expected), "completed": completed,
                "remaining": len(expected) - completed, "workers": workers,
                "config_hash": file_hash(cfg_path)})
    completed = sum(valid(parts / f"{job_id(x)}.json", job_id(x)) for x in expected)
    _atomic_json(root / "results/heterogeneous/checkpoint.json", {
        "status": "complete" if completed == len(expected) else "shard_complete",
        "expected": len(expected), "completed": completed, "remaining": len(expected) - completed,
        "workers": workers, "config_hash": file_hash(cfg_path),
        "runtime_seconds": time.perf_counter() - start})
    return completed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-jobs", type=int)
    args = parser.parse_args()
    print(execute(args.root, args.config, args.workers, args.max_jobs))
