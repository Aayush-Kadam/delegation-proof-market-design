import json
from pathlib import Path

import numpy as np

from delegation_market.m9 import run_id, run_job, tasks
from delegation_market.m9_analysis import select_candidate, summarize_development
from delegation_market.mechanisms import run_auction
from delegation_market.simulation import counterfactual_rewards
from delegation_market.agents import HedgeAgent


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/m9/design.json"


def test_hybrid_endpoints_match_classical_payments():
    bids = np.array([0.8, 0.3])
    assert run_auction(bids, "hybrid", alpha=1, rng=np.random.default_rng(1)).price == 0.8
    assert run_auction(bids, "hybrid", alpha=0, rng=np.random.default_rng(1)).price == 0.3


def test_hybrid_counterfactual_payoff():
    agent = HedgeAgent(1.0, np.array([0.0, 0.5, 1.0]), 0.1, 1)
    got = counterfactual_rewards(agent, 0, np.array([0.5, 0.25]), "hybrid", 0, 0.4)
    assert np.allclose(got, [0.0, 0.65, 0.45])


def test_m9_split_and_counts_are_frozen():
    cfg = json.loads(CONFIG.read_text())
    assert set(cfg["development_environment_ids"]).isdisjoint(cfg["holdout_environment_ids"])
    assert set(cfg["development_environment_ids"] + cfg["holdout_environment_ids"]) == set(range(25))
    assert len(tasks(ROOT, CONFIG, "development")) == 11 * 9 * 15 * 5
    assert len(tasks(ROOT, CONFIG, "holdout", [0, 0.5, 1])) == 3 * 9 * 10 * 30


def test_run_ids_are_deterministic_and_alpha_sensitive():
    spec = tasks(ROOT, CONFIG, "development")[0]
    assert run_id(spec) == run_id(dict(spec))
    changed = dict(spec, alpha=0.2)
    assert run_id(spec) != run_id(changed)


def test_tiny_hybrid_job_serializes_all_objectives():
    spec = dict(tasks(ROOT, CONFIG, "development")[0])
    spec["horizon"] = 8
    row = run_job(spec)
    assert row["run_id"] == run_id(spec)
    assert 0 <= row["revenue"] <= 1
    assert 0 <= row["high_win"] <= 1
    assert abs(row["welfare"] - row["revenue"] - row["bidder_surplus"]) < 1e-12


def test_candidate_rule_is_lexicographic_and_respects_floors():
    import pandas as pd
    frontier = pd.DataFrame([
        {"alpha": .3, "q_revenue_worst": .2, "q_allocation_worst": .08,
         "q_joint_worst": .2, "q_joint_cvar90": .1, "q_joint_p95": .15, "q_joint_mean": .05},
        {"alpha": .5, "q_revenue_worst": .3, "q_allocation_worst": .05,
         "q_joint_worst": .1, "q_joint_cvar90": .05, "q_joint_p95": .08, "q_joint_mean": .03},
        {"alpha": .7, "q_revenue_worst": .2, "q_allocation_worst": .08,
         "q_joint_worst": .2, "q_joint_cvar90": .1, "q_joint_p95": .15, "q_joint_mean": .05},
    ])
    assert select_candidate(frontier)["alpha"] == .3


def test_regret_summary_uses_endpoint_best_per_cell():
    import pandas as pd
    base = {"learner_high": "hedge", "learner_low": "hedge", "environment_id": 0,
            "v_low": .5, "horizon": 10, "c_high": 1, "c_low": 1,
            "welfare": .8, "bidder_surplus": .4}
    rows = pd.DataFrame([{**base, "alpha": 0., "revenue": .3, "high_win": .9},
                         {**base, "alpha": .5, "revenue": .4, "high_win": .8},
                         {**base, "alpha": 1., "revenue": .5, "high_win": .7}])
    cells, frontier = summarize_development(rows)
    middle = cells[cells.alpha == .5].iloc[0]
    assert abs(middle.q_revenue - .2) < 1e-12
    assert abs(middle.q_allocation - .1) < 1e-12
