import pandas as pd

from delegation_market.level3_holdout_final import finalize


def test_frozen_directional_gate_and_novelty_cap(tmp_path):
    cells = pd.DataFrame([
        {"v_low": .3, "horizon": 5000, "c_high": 1., "c_low": 1., "step": .01, "n_seeds": 30,
         "delta_full_ndl_revenue_mean": -.06, "delta_full_ndl_revenue_ci_low": -.07,
         "delta_full_ndl_revenue_ci_high": -.05, "delta_full_dl_ae_mean": .011,
         "delta_full_dl_ae_ci_low": .0101, "delta_full_dl_ae_ci_high": .012,
         "delta_full_dl_welfare_mean": .004, "delta_full_dl_welfare_ci_low": .003,
         "delta_full_dl_welfare_ci_high": .005},
        {"v_low": .5, "horizon": 5000, "c_high": 1., "c_low": 1., "step": .01, "n_seeds": 30,
         "delta_full_ndl_revenue_mean": -.04, "delta_full_ndl_revenue_ci_low": -.05,
         "delta_full_ndl_revenue_ci_high": -.03, "delta_full_dl_ae_mean": .02,
         "delta_full_dl_ae_ci_low": .019, "delta_full_dl_ae_ci_high": .021,
         "delta_full_dl_welfare_mean": .01, "delta_full_dl_welfare_ci_low": .009,
         "delta_full_dl_welfare_ci_high": .011},
    ])
    source = tmp_path / "cells.csv"; cells.to_csv(source, index=False)
    verdict = finalize(source, tmp_path / "out")
    assert verdict["holdout_verdict"] == "PASS"
    assert verdict["level_3_verdict"] == "MIXED"
    assert verdict["primary_gate_union_cells"] == 1
