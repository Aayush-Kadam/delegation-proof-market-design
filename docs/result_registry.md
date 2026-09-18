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
| R-L5-HEDGE | Hedge reproduces the joint FPA-revenue/SPA-allocation conflict in all 25 frozen cross-learner cells | CONFIRMED | `results/level_05/analysis/cell_summary.csv` | Control result; theory remains separately scoped |
| R-L5-FTPL | Full-information FTPL reproduces the joint conflict in all 25 primary cells and all 3 limited falsification attacks | CONFIRMED | `results/level_05/analysis/summary.json`; falsification analysis | Cross-learner computational evidence |
| R-L5-RM | External regret matching passes all 25 primary cells but misses the allocation magnitude threshold in 3/3 independent-seed falsification attacks | PARTIAL | primary and falsification cell summaries | Learner/seed sensitivity |
| R-L5-AGG | The frozen primary Level-5 gate yields strong cross-learner generalization, qualified by regret-matching falsification instability | CONFIRMED / QUALIFIED | `docs/LEVEL_5_STATUS.md` | Theory not extended beyond Hedge |
| R-HET-HF | Hedge high / FTPL low preserves positive aggregate conflict directions but passes 13/25 cells | PARTIAL | `results/heterogeneous/analysis/summary.json` | Ordered-role computation |
| R-HET-FH | FTPL high / Hedge low passes 19/25 cells | STRONG | `results/heterogeneous/analysis/summary.json` | Ordered-role computation |
| R-HET-HR | Hedge high / RM low passes 2/25 cells with positive medians | DIRECTION-ONLY | `results/heterogeneous/analysis/summary.json` | Ordered-role computation |
| R-HET-RH | RM high / Hedge low passes 15/25 cells | STRONG | `results/heterogeneous/analysis/summary.json` | Ordered-role computation |
| R-HET-FR | FTPL high / RM low passes 14/25 cells | PARTIAL | `results/heterogeneous/analysis/summary.json` | Ordered-role computation |
| R-HET-RF | RM high / FTPL low passes 11/25 cells | PARTIAL | `results/heterogeneous/analysis/summary.json` | Ordered-role computation |
| R-HET-ROLE | Swapping learner roles changes the joint gate in 68-72% of environments and the revenue sign in 36-40% | CONFIRMED | `results/heterogeneous/analysis/summary.json` | Possibly distinct auction application |
| R-HET-AGG | Five profiles are strong/partial, one direction-only, and none reverses its aggregate median; 29 cell-level revenue reversals remain | HETEROGENEOUS ROBUSTNESS | `docs/HETEROGENEOUS_LEARNER_STATUS.md` | Targeted audit complete |
| M9-DEV-FRONTIER | The known convex-combination family traces a smooth development revenue/allocation frontier across nine learner profiles | TRADEOFF FRONTIER | `results/m9/development/analysis/frontier.csv` | Family known; application audit complete |
| M9-CANDIDATE | No coarse alpha satisfies both frozen worst normalized revenue-regret and allocation-regret floors | D0 / NO ELIGIBLE CANDIDATE | `results/m9/development/analysis/summary.json` | Prospectively selected negative result |
| M9-HOLDOUT | Holdout evaluation requires an eligible frozen candidate | NOT OPENED | `docs/M9_MECHANISM_STATUS.md` | N/A |
| M9-REDTEAM | Red team requires a D2-or-higher holdout result | NOT RUN | `docs/M9_MECHANISM_STATUS.md` | N/A |
| M9-THEORY | Candidate-specific hybrid theory requires a successful candidate | NOT ATTEMPTED | `docs/M9_MECHANISM_STATUS.md` | N/A |
| M10-GAH-DEV | The normalized bid-gap rule activates as intended across valuation strata but no coarse candidate clears either frozen worst-case floor | G0 / DEVELOPMENT FAILURE | `results/m10/development/analysis/summary.json` | Exact-form novelty unresolved; prospective application audit complete |
| M10-GAH-REFINE | No candidate is eligible or within `.02` of both safety floors | NOT TRIGGERED | `results/m10/development/analysis/coarse_frontier.csv` | N/A |
| M10-GAH-HOLDOUT | M9 mechanism holdout requires an eligible frozen M10 candidate | UNOPENED | `docs/M10_GAP_ADAPTIVE_MECHANISM_STATUS.md` | N/A |
| M10-GAH-REDTEAM | Red team requires holdout success | NOT RUN | `docs/M10_GAP_ADAPTIVE_MECHANISM_STATUS.md` | N/A |
| M10-GAH-THEORY | Candidate-specific theory requires empirical candidate success | NOT ATTEMPTED | `docs/M10_GAP_ADAPTIVE_MECHANISM_STATUS.md` | N/A |

V1 and V2 both leave historical Level 2 MIXED because fewer than two targets strictly passed their prospective criteria. Separately, M2.5 certifies the simulator for the finite-horizon domain stated in `docs/level_3_readiness.md`; it does not revise Level 2.

The smoke run used 3 seeds and 1,000 rounds. Examples of variation (such as Q/Q first-price efficiency from 0.585 to 0.919) demonstrate why these runs cannot support a stable economic claim.
