import numpy as np
from delegation_market.replication import run_hedge_seed


def test_replication_runner_is_deterministic():
    a=run_hedge_seed("second_price",3,horizon=200); b=run_hedge_seed("second_price",3,horizon=200)
    for key in ["tail_mean_price","tail_high_win_share","tail_mean_bid_low","regret_per_round_high"]: assert np.isclose(a[key],b[key])


def test_replication_disallows_low_bidder_overbid_indirectly():
    a=run_hedge_seed("first_price",1,horizon=300); assert a["tail_mean_bid_low"]<=.5


def test_diverging_schedule_satisfies_rate_assumptions_directionally():
    small=run_hedge_seed("second_price",1,horizon=500,rate_schedule="diverging")
    large=run_hedge_seed("second_price",1,horizon=4000,rate_schedule="diverging")
    assert large["rate_ratio"]>small["rate_ratio"]
    assert large["eta_low"]*large["horizon"]>small["eta_low"]*small["horizon"]
    assert large["eta_low"]<small["eta_low"]


def test_exact_policy_metrics_are_bounded():
    a=run_hedge_seed("first_price",2,horizon=6000)
    assert 0<=a["exact_policy_tv_5000_high"]<=1
    assert 0<=a["terminal_truth_tv_low"]<=1
