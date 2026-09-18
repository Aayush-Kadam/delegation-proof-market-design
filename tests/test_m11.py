import json
from pathlib import Path
import numpy as np
from delegation_market.m11_theory import matrices,run,derivative
from delegation_market.m8_theory import run as endpoint_run
from delegation_market.m11_interval import certify


def test_generic_alpha_endpoints_match_m8():
    for alpha,mechanism in [(0,"SPA"),(1,"FPA")]:
        assert np.allclose(run(1/3,1,.1,3,alpha),endpoint_run(1/3,1,.1,3,mechanism))


def test_generic_payment_bounds_and_affinity():
    for alpha in [0,.2,.7,1]:
        _,_,rev,_=matrices(.4,alpha)
        bids_h=[0,.2,.4,1];bids_l=[0,.2,.4]
        for i,bh in enumerate(bids_h):
            for j,bl in enumerate(bids_l): assert min(bh,bl)-1e-15<=rev[i][j]<=max(bh,bl)+1e-15


def test_derivative_agrees_with_secant():
    dr,da=derivative(1/3,1,.1,3,.5);eps=1e-4
    r0,a0=run(1/3,1,.1,3,.5-eps);r1,a1=run(1/3,1,.1,3,.5+eps)
    assert abs(dr-(r1-r0)/(2*eps))<1e-6;assert abs(da-(a1-a0)/(2*eps))<1e-6


def test_interval_witness_certificate():
    result=json.loads((Path(__file__).resolve().parents[1]/"results/m11/constant_alpha_certificate.json").read_text())
    assert result["certified"] and result["alpha_subintervals"]==10000
    assert float(result["revenue_derivative"][0])>0
    assert float(result["allocation_derivative"][1])<0
