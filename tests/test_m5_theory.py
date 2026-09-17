from delegation_market.m5_theory import two_round_contrast
from fractions import Fraction

def test_certificate_point_has_conflict():
    x=two_round_contrast(1/3,1,.1)
    assert x["delta_revenue"] > 0
    assert x["delta_allocation_spa_minus_fpa"] > 0

def test_revenue_coarse_bound_on_restricted_domain():
    for v in (.1,.3,.399):
        for eh in (.1,1,10):
            for el in (0,.1,10):
                x=two_round_contrast(v,eh,el)
                assert x["delta_revenue"] >= (2-5*v)/12 - 1e-12

def test_uniform_payoff_vectors_by_direct_enumeration():
    v=Fraction(1,3)
    # Independently enumerated counterfactual expected utilities against uniform play.
    assert (Fraction(1,4), 3*(1-v)/4, Fraction(0)) == (Fraction(1,4), Fraction(1,2), Fraction(0))
    assert (Fraction(1,4), (3-v)/4, 1-v/2) == (Fraction(1,4), Fraction(2,3), Fraction(5,6))
    assert (v/6, Fraction(0)) == (Fraction(1,18), Fraction(0))
    assert (v/6, v/3) == (Fraction(1,18), Fraction(1,9))
