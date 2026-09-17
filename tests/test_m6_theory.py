from delegation_market.m5_theory import two_round_contrast
from delegation_market.m6_theory import contrast, state, step

def test_general_recurrence_matches_m5_at_h2():
    old=two_round_contrast(1/3,1,.1);new=contrast(1/3,1,.1,2)
    assert abs(old['delta_revenue']-new['delta_revenue'])<1e-14
    assert abs(old['delta_allocation_spa_minus_fpa']-new['delta_allocation'])<1e-14

def test_low_log_ratio_moves_oppositely():
    assert step(1/3,1,.1,'FPA',0,0,0)[2] < 0
    assert step(1/3,1,.1,'SPA',0,0,0)[2] > 0

def test_certified_box_corners_through_nine():
    for v in (.30,.36):
      for eh in (.8,1.2):
       for el in (.05,.15):
        for h in range(2,10): assert contrast(v,eh,el,h)['conflict']
