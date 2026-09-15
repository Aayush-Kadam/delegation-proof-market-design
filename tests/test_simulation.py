import numpy as np
from delegation_market.agents import TruthfulAgent
from delegation_market.simulation import SimulationConfig, simulate, counterfactual_rewards
from delegation_market.agents import HedgeAgent


def test_seeded_simulation_is_deterministic():
    grid=np.linspace(0,1,101)
    a=[TruthfulAgent(1,grid,1),TruthfulAgent(.6,grid,2)]
    b=[TruthfulAgent(1,grid,1),TruthfulAgent(.6,grid,2)]
    fa,ma=simulate(a,SimulationConfig(rounds=50,seed=7)); fb,mb=simulate(b,SimulationConfig(rounds=50,seed=7))
    assert fa.equals(fb); assert ma==mb


def test_accounting_identity():
    grid=np.linspace(0,1,101); f,m=simulate([TruthfulAgent(1,grid),TruthfulAgent(.6,grid)],SimulationConfig(rounds=10))
    grouped=f.groupby("round"); welfare=(f.value*f.allocated).groupby(f["round"]).sum()
    assert np.allclose(grouped.utility.sum()+grouped.payment.sum(),welfare)


def test_counterfactual_tie_uses_expected_uniform_allocation():
    grid=np.array([.4,.5,.6]); a=HedgeAgent(1,grid)
    rewards=counterfactual_rewards(a,0,np.array([.4,.5]),"first_price",0,1)
    assert np.allclose(rewards,[0,.25,.4])


def test_no_overbidding_grid_can_be_enforced_by_construction():
    a=HedgeAgent(.5,np.arange(0,.51,.01)); assert a.bid_grid.max()<=a.value
