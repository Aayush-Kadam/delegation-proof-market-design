import numpy as np
from delegation_market.diagnostics import classify_convergence,policy_l1_distance


def test_identical_windows_are_stable():
    grid=np.array([0,.5,1]); a=np.tile([0,.5,1],4000)
    assert classify_convergence(a,grid)["label"]=="stable_tail"


def test_distribution_shift_is_unstable():
    grid=np.array([0,.5,1]); a=np.r_[np.zeros(5000),np.ones(5000)]
    assert policy_l1_distance(a[:5000],a[5000:],grid)==2
    assert classify_convergence(a,grid)["label"]=="unstable_tail"
