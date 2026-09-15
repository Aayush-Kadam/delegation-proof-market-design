import numpy as np
from delegation_market.diagnostics import classify_convergence,policy_l1_distance,total_variation,wasserstein_1_ordered,stationary_null_l1


def test_identical_windows_are_stable():
    grid=np.array([0,.5,1]); a=np.tile([0,.5,1],4000)
    assert classify_convergence(a,grid)["label"]=="stable_tail"


def test_distribution_shift_is_unstable():
    grid=np.array([0,.5,1]); a=np.r_[np.zeros(5000),np.ones(5000)]
    assert policy_l1_distance(a[:5000],a[5000:],grid)==2
    assert classify_convergence(a,grid)["label"]=="unstable_tail"


def test_policy_distances_have_known_values():
    p=np.array([1.,0,0]); q=np.array([0,0,1.]); grid=np.array([0.,.5,1.])
    assert total_variation(p,q)==1; assert wasserstein_1_ordered(p,q,grid)==1


def test_stationary_null_is_seeded_and_nonnegative():
    p=np.ones(10)/10; a=stationary_null_l1(p,100,repetitions=20,seed=4); b=stationary_null_l1(p,100,repetitions=20,seed=4)
    assert np.array_equal(a,b); assert np.all(a>=0)
