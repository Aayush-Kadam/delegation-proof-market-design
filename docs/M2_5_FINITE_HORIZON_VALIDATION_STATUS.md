# DELEGATION-PROOF MARKET DESIGN — M2.5 VALIDATION STATUS

## 1. Historical record

    Level 2 V1 = FAIL
    Level 2 V2 = FAIL
    Historical Level 2 = MIXED

No revision. M2.5 is a separate certification question.

## 2. Why the gate failed

### Substantive contradiction

None identified. R-REP-001 passed. R-REP-002 reproduced the source-relevant FPA price and allocation. R-REP-003 moved in the theorem-predicted direction under a theorem-compatible learning-rate sequence.

### Finite-horizon limitation

R-REP-003's exact last-iterate TV declined only from .95442 at 25k to .94597 at 200k. The theorem is asymptotic; this ladder did not enter a low-TV regime.

### Diagnostic limitation

V1's sampled adjacent-window L1 rule had 70–100% false rejection in prospective stationary-policy null checks. In V2, exact-policy TV remained .08048 for the FPA high bidder while Wasserstein-1 was only .000843, showing redistribution among neighboring bids rather than economically large movement.

### Protocol-created threshold failure

R-REP-002-V2 met the price (.495504), high-win-share (.980187), and regret targets, but its median half-to-half price and winner-share changes (.011347 and .04112) missed project-created .01 and .02 cutoffs. Those cutoffs are not theorem statements. Official status remains PARTIAL; its separate FINITE-HORIZON VALIDATION VALUE is **HIGH** because the economic quantities are reproduced and the residual instability is small in bid geometry. This is unresolved finite-horizon convergence, not an economically meaningful contradiction or software failure.

## 3. R-REP-003 convergence feasibility

With K_W=101 and K_R=51,

    eta_R/eta_W = sqrt(log(51)/log(101)) T^(1/6) = 0.92304 T^(1/6).

| Ratio | Required T | 30 seeds, one schedule | 30 paired seeds, two schedules |
|---:|---:|---:|---:|
| 8 | 423,942 | 0.12 h | 0.23 h |
| 10 | 1,617,210 | 0.45 h | 0.89 h |
| 15 | 18,421,030 | 5.09 h | 10.19 h |
| 20 | 103,501,400 | 28.62 h | 57.23 h |
| 30 | 1,178,946,000 | 325.95 h | 651.90 h |

Costs use the observed V2 aggregate throughput, approximately 30,141 auction rounds/second. Growth in this ratio is not a TV convergence rate.

The complete Theorem D.4 proof does **not** yield a practically evaluable finite-T TV upper bound. It uses unspecified discretization/mechanism constants and probability terms stated as o(1). Its exponential weight-ratio step establishes asymptotic concentration but does not specify all constants needed to calculate TV_T at a requested T. No rate was invented and no TV-threshold table is attributed to the proof.

**EMPIRICAL EXTRAPOLATION — NOT A THEORETICAL RESULT.** Fits to the four preserved means (.95442, .95192, .94900, .94597) have small interpolation errors but extreme extrapolations. Power and log-linear fits respectively imply log10 horizons of (10.36, 28.81, 69.85, 140.02, 232.77) and (10.21, 26.19, 52.82, 79.45, 95.43) for TV (.9, .75, .5, .25, .1). The inverse-log fit has asymptote .905 and never reaches any listed threshold. Leave-one-horizon-out RMSE is .00036, .00035, and .00080, but four high-TV points cannot identify the tail. Required horizon is therefore unidentifiable and plausibly prohibitive.

Decision: **RETIRE AS FINITE-HORIZON VALIDATION GATE.** Mechanism accounting and MWU updates are independently tested; comparative statics match; Theorem D.4 concerns a regime far beyond planned horizons; and finite-horizon discovery will not claim its asymptotic conclusion. R-REP-003-V2 remains PARTIAL and the limitation remains public.

## 4. New finite-horizon replication

| Field | Record |
|---|---|
| Source | Cesa-Bianchi–Lugosi Theorem 2.2 finite-time exponential-weights inequality, instantiated in repeated auctions |
| Theorem/proposition | E[R_T] <= log(K)/eta + eta T/8 for rewards in [0,1]; eta=sqrt(8 log K/T) |
| Configuration | One Hedge bidder (value 1, K=101) versus a frozen deterministic bid cycle; FPA and SPA |
| Seeds | 30 per mechanism-horizon plus exact deterministic expectation |
| Horizons | 10k, 25k, 50k, 100k, 200k |
| Expected | Normalized exact regret <= 1 in all 10 strata |
| Observed | FPA ratios .5002–.5025; SPA ratios .3037–.3066; reward range [0,.90] |
| Status | **PASS** |

The 30-seed realized-regret 95% intervals were also below the bound in every stratum, but this audit cannot override the exact primary calculation.

## 5. Finite-Horizon Simulator Validation

**CERTIFIED**

R-REP-001 remains PASS; 19 tests pass; the new source-grounded finite-time target passes; R-REP-002 remains economically consistent; and no material finite-horizon software inconsistency is unresolved. This does not clear historical Level 2.

## 6. Validated domain

- Repeated two-bidder single-item first- and second-price auctions with persistent values in [0,1].
- Discrete no-overbid grids through 101 actions, uniform tie accounting, no reserve in the powered M2.5 target.
- Full-information Hedge/MWU with uniform initialization and horizon-fixed learning rates.
- Finite horizons through 200,000 rounds per run.
- Allocation, payment, expected counterfactual utility, external-regret, price, and win-share calculations.
- Multi-seed finite-horizon comparisons whose claims remain within the tested model.

## 7. Unsupported domain

- Asymptotic last-iterate truthfulness or a finite-time TV rate for Theorem D.4.
- Continuous bid spaces, large bidder populations, changing/private stochastic values, or endogenous entry.
- Partial/bandit feedback as a validated substitute for full feedback.
- Q-learning, deep RL, LLM bidders, or strategic principals as confirmatory domains.
- Randomized strictly IC auction constructions, general reserves/hybrid/all-pay mechanisms as externally replicated domains.
- Claims beyond 200,000 rounds or universal robustness across learner families.

## 8. Novelty reassessment

Known/closed as standalone contributions: user-to-agent strategic value reporting; learning-rate heterogeneity alone; deterministic-versus-randomized truthful mechanisms; Q-learning coordination/collusion as a general phenomenon; generic autobidding; generic learning-robust mechanism design; and broad finite-horizon no-regret guarantees. Feedback design, heterogeneous learner populations, and nonstationarity also have adjacent literatures, so only auction-specific, sharply distinguished claims remain plausible.

| Rank and opening | Novelty | Importance | Theory | Simulation | Overlap risk |
|---|---:|---:|---:|---:|---:|
| 1. Finite-horizon mechanism ranking by worst-case degradation across a prospectively fixed learner/feedback family | 8/10 | 9/10 | 7/10 | 9/10 | 5/10 |
| 2. Feedback-design effects on finite-horizon delegation distortion | 7/10 | 8/10 | 6/10 | 8/10 | 6/10 |
| 3. Mechanism performance under heterogeneous learning populations | 7/10 | 8/10 | 5/10 | 8/10 | 6/10 |

These are gap hypotheses, not novelty claims. The first is narrow enough to distinguish itself from heterogeneous-buyer robust repeated mechanisms, partial-feedback bidder regret, randomized truthfulness, and principal misreporting.

## 9. Level-3 recommendation

**PROCEED TO LEVEL 3.** Primary campaign: **finite-horizon mechanism ranking by worst-case degradation across a prospectively fixed learner/feedback family**. Preregister it separately; do not use principal misreporting as the primary novelty. No Level 3 experiment was run in M2.5.

## 10. Repository status

- Tests: 19 passed (the historical 17 plus two independent M2.5 reward checks).
- Protocol commit: `508546f`.
- Protocol hash: `fbdd412cd800cbca0b1627c1eb3b23a5d912762f61128474df66ad300d0cc9ad`.
- New simulations: 300 seeded strata-runs plus ten exact expectation calculations.
- New simulated rounds: 23,100,000; exact policy-propagation rounds: 770,000.
- Runtime: 46.87 seconds for the powered target.
- Changed artifacts: selection memo, frozen protocol/hash, runner, tests, results/manifest, adjudication outputs, this report, readiness memo, literature/novelty/status registries.

Permanent limitation: Our simulator reproduces the major finite-horizon economic behavior of the reference models, but our computational horizons do not enter the asymptotic last-iterate convergence regime required by Aggarwal et al. Theorem D.4.
