import numpy as np
from delegation_market.level3 import run_seed


def test_level3_accounting_identities_small_run():
    r=run_seed("first_price",.4,100,.1,.1,17,step=.1,tail_share=.1)
    assert np.isclose(r["full_dl_revenue"],.4-r["full_revenue"])
    assert np.isclose(r["full_dl_ae"],1-r["full_high_win"])
    assert np.isclose(r["full_dl_welfare"],1-r["full_welfare"])
    assert np.isclose(r["full_surplus_total"],r["full_surplus_high"]+r["full_surplus_low"])
    assert 0 <= r["full_high_win"] <= 1


def test_discrete_reference_profile_is_equilibrium_on_registered_values():
    step=.01
    for vl in [.1,.2,.3,.4,.5,.6,.7,.8,.9]:
        bh,bl=vl,vl-step
        high_u=1-bh; high_tie=.5*(1-bl)
        assert high_u >= high_tie
        assert bl <= vl and bh <= 1
