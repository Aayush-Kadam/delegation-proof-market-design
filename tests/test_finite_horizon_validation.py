import numpy as np

from delegation_market.finite_horizon_validation import reward_vector


def test_fpa_reward_vector_matches_direct_formula():
    grid=np.linspace(0,1,101); rival=.6
    expected=np.where(grid>rival,1-grid,np.where(grid==rival,(1-grid)/2,0))
    np.testing.assert_allclose(reward_vector(grid,"first_price",rival),expected)


def test_spa_reward_vector_matches_direct_formula_and_bounds():
    grid=np.linspace(0,1,101); rival=.6
    expected=np.where(grid>rival,.4,np.where(grid==rival,.2,0))
    actual=reward_vector(grid,"second_price",rival)
    np.testing.assert_allclose(actual,expected)
    assert actual.min() >= 0 and actual.max() <= 1
