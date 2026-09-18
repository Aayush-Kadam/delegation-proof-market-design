# Clean-room reproduction

**Verdict: PASS**

Date: 2026-09-18. Source commit: `e7f0bf24` (release candidate for v1.1.0).

A new local clone was created in a fresh temporary directory. A new virtual environment was built with Python 3.12, and every package was downloaded without a pip cache from `requirements-lock.txt`; the project was then installed editable from that clone. No unpublished working-tree artifacts were copied into it.

| Step | Result | Runtime |
|---|---|---:|
| Fresh clone | PASS | included in setup |
| Fresh locked dependency install | PASS | 195.6 s including clone, venv, and install |
| Full tests | 66 passed, 0 failed | 17.0 s |
| M11 10,000-subinterval certificate | PASS | 454.7 s |
| Level-3 frozen holdout summary/figure | PASS | 5.3 s |
| Level-5 summary/figures | PASS | completed within core analysis stage |
| Heterogeneous summary/figures | PASS | 15.0 s |
| Manuscript and publication figures | PASS | 14.5 s |
| Compact archive and checksums | PASS | 0.6 s |

The regenerated Level-3 verdict is PASS with 54/75 primary-gate cells; Level 5 is STRONG CROSS-LEARNER GENERALIZATION with 25/25 for each homogeneous learner; heterogeneous regeneration retains 29 revenue reversals, zero allocation reversals, and the frozen profile classifications. The rebuilt PDF contains 18 pages.

This is the strongest internal approximation to independent reproduction available within the project. It is **not independent external replication**: the clone, code, and verification were all produced by the same research package and execution environment.
