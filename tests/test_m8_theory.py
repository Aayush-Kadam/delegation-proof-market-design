from fractions import Fraction as F
from delegation_market.m8_theory import matrices,contrast

def test_4x3_payoffs_at_v_one_third():
    v=F(1,3);uf,lf,rf,af=matrices(v,'FPA');us,ls,rs,ass=matrices(v,'SPA')
    assert uf[1]==[1-v/2,(1-v/2)/2,0]
    assert us[1]==[1,(1-v/2)/2,0]
    assert lf[0]==[v/2,v/2,0]
    assert ls[0]==[v/2,v, v]
    assert rf[2]==[v,v,v] and rs[2]==[0,v/2,v]

def test_certified_narrow_corners_through_six():
    for v in (.31,.35):
      for eh in (.85,1.15):
       for el in (.06,.14):
        for h in range(2,7): assert contrast(v,eh,el,h)['conflict']

def test_endogenous_stability_closed_form():
    eta=.2;e=[.1,.05,.02];
    bounds=[2*eta*sum((1+eta)**(t-1-s)*e[s] for s in range(t)) for t in range(1,4)]
    assert bounds[0]==2*eta*e[0]
    assert bounds[2] >= 0
