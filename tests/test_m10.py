import json
from pathlib import Path

import numpy as np
import pytest

from delegation_market.agents import HedgeAgent
from delegation_market.m10 import run_id, run_job, tasks
from delegation_market.mechanisms import gap_adaptive_alpha, run_auction
from delegation_market.simulation import counterfactual_rewards
from delegation_market.m10_analysis import cvar

ROOT=Path(__file__).resolve().parents[1];CONFIG=ROOT/"configs/m10/design.json"


def test_gap_alpha_zero_and_saturation_and_monotonicity():
    assert gap_adaptive_alpha(0,0,.2,.4)==.2
    values=[gap_adaptive_alpha(1,1-g,.2,.4) for g in [0,.1,.2,.4,.8]]
    assert values==sorted(values);assert values[-1]==1;assert values[-2]==1


@pytest.mark.parametrize("bids", [[0,0],[.8,.3],[.5,.5],[1,0]])
def test_gap_payment_bounds_and_determinism(bids):
    x=run_auction(bids,"gap_adaptive",alpha=.35,tau=.4,rng=np.random.default_rng(3))
    y=run_auction(bids,"gap_adaptive",alpha=.35,tau=.4,rng=np.random.default_rng(3))
    assert min(bids)<=x.price<=max(bids);assert x.price==y.price;assert x.winner==y.winner


def test_gap_counterfactual_matches_direct_utility_without_ties():
    agent=HedgeAgent(1,np.array([0.,.5,1.]),.1,1);bids=np.array([.5,.25])
    rv=counterfactual_rewards(agent,0,bids,"gap_adaptive",0,.2,.5)
    direct=[]
    for bid in agent.bid_grid:
        r=run_auction([bid,.25],"gap_adaptive",alpha=.2,tau=.5,rng=np.random.default_rng(1))
        direct.append((1-r.price) if r.winner==0 else 0)
    assert np.allclose(rv,direct)


def test_frozen_grid_count_and_identity():
    assert len(tasks(ROOT,CONFIG))==4860
    spec=tasks(ROOT,CONFIG)[0];assert run_id(spec)==run_id(dict(spec));assert run_id(spec)!=run_id(dict(spec,tau=.8))


def test_tiny_job_records_diagnostics_and_accounting():
    spec=dict(tasks(ROOT,CONFIG)[0],horizon=10);row=run_job(spec)
    assert 0<=row["normalized_gap"]<=1;assert spec["a"]<=row["realized_alpha"]<=1
    assert abs(row["welfare"]-row["revenue"]-row["bidder_surplus"])<1e-12


def test_cvar_selects_upper_tail():
    assert cvar([0,1,2,3,4],.4)==3.5
