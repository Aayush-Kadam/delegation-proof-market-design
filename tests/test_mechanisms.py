import numpy as np
import pytest
from delegation_market.mechanisms import run_auction


def test_first_price_allocation_and_payment():
    r=run_auction([.3,.6],"first_price",rng=np.random.default_rng(1)); assert r.winner==1; assert r.price==.6; assert r.payments.sum()==.6


def test_second_price_and_reserve():
    r=run_auction([.3,.8],"second_price",reserve=.5,rng=np.random.default_rng(1)); assert r.winner==1; assert r.price==.5


def test_no_sale_below_reserve():
    r=run_auction([.1,.2],"first_price",reserve=.3); assert r.winner is None; assert r.payments.sum()==0


def test_hybrid_nests_endpoints():
    assert run_auction([.2,.8],"hybrid",alpha=1,rng=np.random.default_rng(1)).price==.8
    assert run_auction([.2,.8],"hybrid",alpha=0,rng=np.random.default_rng(1)).price==.2


def test_invalid_bid_rejected():
    with pytest.raises(ValueError): run_auction([-.1,.2])

