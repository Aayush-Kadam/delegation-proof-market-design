import numpy as np

from delegation_market.heterogeneous_analysis import median_ci, normal_ci


def test_normal_ci_and_deterministic_median_bootstrap():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    mean, low, high = normal_ci(x)
    assert mean == 2.5 and low < mean < high
    assert median_ci(x, 11) == median_ci(x, 11)
    median, low, high = median_ci(x, 11)
    assert median == 2.5 and low <= median <= high
