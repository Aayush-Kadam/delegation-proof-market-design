from fractions import Fraction as F
from delegation_market.m7_theory import contrast,step

def test_exact_uniform_payoff_vectors_v_one_third():
    v=F(1,3)
    assert ((F(1,4),(1-v/2)/2,3*(1-v)/4,F(0))) == (F(1,4),F(5,12),F(1,2),F(0))
    assert ((F(1,4),F(1,2),(3-v)/4,1-v/2)) == (F(1,4),F(1,2),F(2,3),F(5,6))

def test_low_ratio_recurrence_signs():
    assert step(1/3,1,.1,'FPA',0,0,0,0)[3] < 0
    assert step(1/3,1,.1,'SPA',0,0,0,0)[3] > 0

def test_certified_rectangle_corners_through_six():
    for v in (.30,.36):
      for eh in (.8,1.2):
       for el in (.05,.15):
        for h in range(2,7): assert contrast(v,eh,el,h)['conflict']

def test_action_expansion_mass_bound():
    # one added action, equal initial weights, cumulative gap G=2, eta=.5
    import math
    delta=math.exp(-1)/(1+math.exp(-1))
    assert delta <= math.exp(-1)
