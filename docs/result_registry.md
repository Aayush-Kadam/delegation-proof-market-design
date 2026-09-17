# Result registry

| ID | Claim | Status | Evidence | Novelty checked? |
|---|---|---|---|---|
| S1 | Mechanism and accounting invariants pass automated tests | SOFTWARE VALIDATION | `tests/` | N/A |
| E1 | Adaptive-agent smoke runs execute across 30 seeded configurations | DIAGNOSTIC | `results/processed/smoke_summary.csv` | N/A |
| R1 | Kolumbus–Nisan report a principal-reporting contrast between FPA and SPA | ESTABLISHED | literature map | Yes, first pass |
| R-REP-001 | Equal-rate Hedge in SPA with values `(1,.5)` yields near-certain high-value wins and mean tail price `.27058` | REPLICATED | `results/replication/seed_results.csv` | Source result checked |
| R-REP-002 | Hedge in FPA produces price `.49550` and high-value win share `.98019`, but fails frozen tail-stability criterion | PARTIAL REPLICATION | `experiments/level_02/replication_report.md` | Source result checked |
| R-REP-003 | A 10x runner learning rate raises its mean SPA bid by `.10505`, but does not meet the frozen truthfulness threshold | PARTIAL / NOT THEOREM-COMPARABLE | `results/replication/seed_results.csv` | Source theorem checked |
| R-REP-002-V2 | FPA again matches price/allocation but narrowly fails prospective half-to-half economic-stability thresholds | PARTIAL REPLICATION | `experiments/level_02/replication_repair_v2_report.md` | V2 source mapping complete |
| R-REP-003-V2 | A theorem-compatible diverging-rate sequence improves exact last-iterate truthfulness at every horizon but does not reach frozen trend magnitudes | PARTIAL REPLICATION | `results/replication_v2/seed_results_v2.csv` | Theorem D.4 mapped |
| M2.5-FH-001 | Hedge exact expected regret satisfies the finite-time exponential-weights inequality in all ten frozen FPA/SPA horizon strata | REPLICATED / PASS | `results/finite_horizon_validation/summary.csv` | Source result checked prospectively |
| L3-C3-DEV | A frozen development cell exhibits an FPA-revenue versus SPA-allocation/welfare objective conflict | EXPLORATORY / CANDIDATE FROZEN | `results/level_03/development/analysis/paired_cell_summary.csv` | Substantial overlap |
| L3-C3-FALS | The frozen C3 candidate survives all eight preregistered falsification attacks | FALSIFICATION PASS | `results/level_03/falsification/verdict.json` | Substantial overlap |
| L3-C3-HOLDOUT | The frozen directional objective-conflict gate passes in 54/75 independent holdout cells | HOLDOUT PASS | `results/level_03/holdout/analysis/primary_candidate_verdict.json` | Substantial overlap |
| L3-FINAL | The candidate is robust across development, falsification, and holdout, but prior literature caps the scientific verdict | MIXED / PROMISING PHENOMENON | `docs/LEVEL_3_STATUS.md` | Yes; no novelty claim |
| M4-SMALL | Exact `.25`-grid mean-field Hedge reproduces the revenue-allocation sign conflict in 59/60 tiny cells and supplies one counterexample to universality | EXPLANATORY / NOT CONFIRMATORY | `results/m4/small_game/verdict.json` | Yes |
| M4-NOVELTY | The joint finite-horizon objective-conflict surface is possibly distinct, but its component mechanisms are known | PROMISING BUT NARROW | `docs/m4_novelty_matrix.md` | Claim-by-claim audit complete |
| TH-M5-001 | Symmetric two-action reduction produces the target two-round allocation sign | DISPROVEN | `docs/m5_proof.md` and M5 notes | Yes |
| TH-M5-002 | Universal finite-horizon FPA revenue dominance | COUNTEREXAMPLE | `results/m4/small_game/verdict.json` | Yes |
| TH-M5-003 | On explicit `C_2`, two-round FPA revenue exceeds SPA while SPA allocation exceeds FPA | THEOREM | `docs/m5_proof.md`, `results/m5/interval_certificate.json` | Yes, theorem-level audit |
| TH-M5-004 | Hedge cumulative log-weight ratio identity | RESTRICTED-PROPOSITION | `docs/m5_proof.md` | Established identity |
| TH-M6-001 | Exact three-log-ratio recurrence for the 3x2 Hedge model | PROPOSITION | `docs/m6_proof.md`, `src/delegation_market/m6_theory.py` | Yes |
| TH-M6-002 | Closed parameter rectangle supports the conflict at H=2 | RESTRICTED-THEOREM | `results/m6/interval_box.json` | Yes |
| TH-M6-003 | The same closed rectangle supports the conflict for every H=2,...,9 | THEOREM | `docs/m6_proof.md`, `results/m6/interval_box.json` | Yes, targeted audit |
| TH-M6-004 | Current interval proof extends through H=10 | CONJECTURE | H=10 enclosure crosses zero; witness remains positive | Pending |
| TH-M6-005 | Uniform early-horizon off-core mass control from Hedge alone | DISPROVEN | Uniform initialization and absent uniform payoff gaps | Structural |
| TH-M7-001 | Exact 4x2 payoff system and four-ratio Hedge recurrence | PROPOSITION | `docs/m7_proof.md` | Yes |
| TH-M7-002 | M6 conflict survives at a 4x2 witness | RESTRICTED-THEOREM | `results/m7/exploration.json` | Yes |
| TH-M7-003 | Closed 4x2 rectangle supports conflict for every H=2,...,6 | THEOREM | `results/m7/interval_box.json` | Targeted audit |
| TH-M7-004 | Fixed-history Hedge action-expansion/off-core-mass bound | PROPOSITION | `docs/m7_proof.md` | Elementary/known algebra |
| TH-M7-005 | Existing rectangle certified at H=7 in 4x2 model | CONJECTURE | Numerical support; interval enclosure inconclusive | Pending |
| TH-M8-001 | Exact rule-generated 4x3 payoff system and five-ratio recurrence | PROPOSITION | `docs/m8_proof.md` | Yes |
| TH-M8-002 | Closed 4x3 rectangle supports conflict for H=2,...,6 | THEOREM | `results/m8/interval_box_narrow.json` | Targeted audit |
| TH-M8-003 | Finite-horizon endogenous Hedge trajectory stability bound | PROPOSITION | `docs/m8_proof.md` | General ingredients known |
| TH-M8-004 | Margin-minus-stability-error sign transfer | CONDITIONAL-THEOREM | `docs/m8_proof.md` | Incremental |
| TH-M8-005 | Uniform-initialized 4x3 follows from generic transfer bound | DISPROVEN | Initial off-core mass makes bound vacuous | Structural |

V1 and V2 both leave historical Level 2 MIXED because fewer than two targets strictly passed their prospective criteria. Separately, M2.5 certifies the simulator for the finite-horizon domain stated in `docs/level_3_readiness.md`; it does not revise Level 2.

The smoke run used 3 seeds and 1,000 rounds. Examples of variation (such as Q/Q first-price efficiency from 0.585 to 0.919) demonstrate why these runs cannot support a stable economic claim.
