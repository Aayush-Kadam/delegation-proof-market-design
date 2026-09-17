# Level 5 cross-learner validation protocol — frozen before powered execution

## Design

- Learners: homogeneous Hedge/Hedge, FTPL/FTPL, external-regret-matching/external-regret-matching.
- Mechanisms: FPA and SPA only.
- Bid grids: exact Level-3 no-overbid `.01` grids.
- Feedback: full expected counterfactual rewards.
- Seeds: `3000,...,3029`, paired across mechanism and learner.
- Environments: 25 parameter-only cells in `configs/level_05/environments.json`.
- Horizons are inherited: 5,000, 25,000, or 100,000. Expected mechanism runs: 4,500; logical auction rounds: 144,000,000.

## Prospective selection

For each of the five holdout valuations, select the same five strata: `(5000,1,1)`, `(5000,.5,1)`, `(25000,1,.5)`, `(25000,1,2)`, `(100000,2,1)`. Selection uses parameters only and never Level-3 outcomes.

## Metrics and gates

Per learner/environment, paired seeds define `D_R=R_FPA-R_SPA`, `D_A=A_SPA-A_FPA`, and `D_W=W_SPA-W_FPA`. The inherited revenue magnitude threshold is normalized: `D_R/v >= .05`; allocation threshold is `D_A >= .01`. A cell passes when both thresholds hold and paired 95% normal CIs for raw `D_R` and `D_A` have lower endpoints above zero.

Learner classification: strong generalization at 15–25 passing cells with positive medians; partial at 10–14 or positive medians with weaker cell support; fail below 10 or if either median reverses. Overall: PASS—STRONG when both new learners are at least partial and one strong; PASS when both retain positive medians and meaningful support; MIXED when only one generalizes; FAIL when neither does.

No non-Hedge scientific outcome may be inspected until all frozen runs are complete and uniqueness/completeness checks pass.

## Durability

Every mechanism run has a deterministic SHA-256-derived ID and is atomically persisted immediately. Resume validates and skips completed IDs. The checkpoint records expected/completed counts and config hash. Powered execution requires interruption/resume smoke validation and 2-/4-worker benchmarks first.
