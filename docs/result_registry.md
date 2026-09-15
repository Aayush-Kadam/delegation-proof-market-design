# Result registry

| ID | Claim | Status | Evidence | Novelty checked? |
|---|---|---|---|---|
| S1 | Mechanism and accounting invariants pass automated tests | SOFTWARE VALIDATION | `tests/` | N/A |
| E1 | Adaptive-agent smoke runs execute across 30 seeded configurations | DIAGNOSTIC | `results/processed/smoke_summary.csv` | N/A |
| R1 | Kolumbus–Nisan report a principal-reporting contrast between FPA and SPA | ESTABLISHED | literature map | Yes, first pass |
| R-REP-001 | Equal-rate Hedge in SPA with values `(1,.5)` yields near-certain high-value wins and mean tail price `.27058` | REPLICATED | `results/replication/seed_results.csv` | Source result checked |
| R-REP-002 | Hedge in FPA produces price `.49550` and high-value win share `.98019`, but fails frozen tail-stability criterion | PARTIAL REPLICATION | `experiments/level_02/replication_report.md` | Source result checked |
| R-REP-003 | A 10x runner learning rate raises its mean SPA bid by `.10505`, but does not meet the frozen truthfulness threshold | PARTIAL / NOT THEOREM-COMPARABLE | `results/replication/seed_results.csv` | Source theorem checked |

No new computational or theoretical project result is registered. Level 2 is MIXED because fewer than two targets strictly passed the frozen criteria.

The smoke run used 3 seeds and 1,000 rounds. Examples of variation (such as Q/Q first-price efficiency from 0.585 to 0.919) demonstrate why these runs cannot support a stable economic claim.
