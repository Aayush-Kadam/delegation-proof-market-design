import numpy as np

from delegation_market.m4_small_game import mean_field_hedge, payoff_matrices


def test_tiny_payoff_matrices_accounting():
    _, _, uh, ul, revenue, high_win = payoff_matrices("first_price", .5, .25)
    welfare = .5 + .5 * high_win
    assert np.allclose(uh + ul + revenue, welfare)
    _, _, uh, ul, revenue, high_win = payoff_matrices("second_price", .5, .25)
    welfare = .5 + .5 * high_win
    assert np.allclose(uh + ul + revenue, welfare)


def test_tiny_mean_field_is_deterministic():
    a = mean_field_hedge("first_price", .5, 25)
    b = mean_field_hedge("first_price", .5, 25)
    assert a == b
