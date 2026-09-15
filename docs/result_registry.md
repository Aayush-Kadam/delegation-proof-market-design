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

V1 and V2 both leave historical Level 2 MIXED because fewer than two targets strictly passed their prospective criteria. Separately, M2.5 certifies the simulator for the finite-horizon domain stated in `docs/level_3_readiness.md`; it does not revise Level 2.

The smoke run used 3 seeds and 1,000 rounds. Examples of variation (such as Q/Q first-price efficiency from 0.585 to 0.919) demonstrate why these runs cannot support a stable economic claim.
