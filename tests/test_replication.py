import numpy as np
from delegation_market.replication import run_hedge_seed


def test_replication_runner_is_deterministic():
    a=run_hedge_seed("second_price",3,horizon=200); b=run_hedge_seed("second_price",3,horizon=200)
    for key in ["tail_mean_price","tail_high_win_share","tail_mean_bid_low","regret_per_round_high"]: assert np.isclose(a[key],b[key])


def test_replication_disallows_low_bidder_overbid_indirectly():
    a=run_hedge_seed("first_price",1,horizon=300); assert a["tail_mean_bid_low"]<=.5

