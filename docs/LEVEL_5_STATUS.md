# DELEGATION-PROOF MARKET DESIGN — LEVEL 5 STATUS

## 1. Executive verdict

**STRONG CROSS-LEARNER GENERALIZATION** under the frozen primary gate. Hedge, full-information FTPL, and external regret matching each pass 25/25 primary environments. The separately frozen limited falsification qualifies this conclusion: FTPL passes all three attacks, whereas regret matching preserves positive signs but misses the allocation magnitude threshold in all three.

## 2. Protocol

- Preregistration commit: `1cc7c4e`
- Environment/config SHA-256: `f2cb5a268261dfbfc992562539eca7662e2e70d5243b78a0f6403b2fa4bfe2c0`
- Protocol-document SHA-256: `6984d79cf365787bbd070378b5c46809825f9654ec3de717f21b5237ff09d0b3`
- 25 parameter-selected environments; Hedge, canonical fixed-perturbation full-information FTPL, and external regret matching
- Seeds `3000,...,3029`, paired across FPA/SPA; 4,500 unique mechanism runs; 144,000,000 logical auction rounds
- Complete data audit: 4,500 expected, 4,500 unique, zero missing, duplicate, corrupt, unexpected, or identity-mismatched records
- Primary gate: `D_R/v >= .05`, `D_A >= .01`, with paired normal 95% CI lower endpoints for raw `D_R` and `D_A` above zero

Reported aggregate intervals below are deterministic bootstrap 95% intervals for the median of the 25 cell means. Cell decisions use the preregistered paired normal intervals, not these aggregate intervals.

## 3. Hedge control

Hedge passes 25/25 cells. Median cell effects (95% bootstrap interval):

- `D_R = 0.104907` `[0.098755, 0.126745]`
- `D_A = 0.067163` `[0.055363, 0.079483]`
- `D_W = 0.016860` `[0.015176, 0.019698]`

Every valuation stratum passes 5/5; all 10 short-, 10 medium-, and 5 long-horizon cells pass. This reproduces the qualitative Level-3 objective conflict.

## 4. FTPL

FTPL passes 25/25 primary cells: **STRONG GENERALIZATION**.

- Median `D_R = 0.109278` `[0.095120, 0.123481]`
- Median `D_A = 0.070892` `[0.063431, 0.079949]`
- Median `D_W = 0.017381` `[0.016229, 0.019292]`
- Mean per-round external regret, high/low bidder: FPA `0.022245 / 0.014651`; SPA `0.003891 / 0.003582`

Every valuation and horizon stratum passes completely.

## 5. Regret Matching

Regret matching passes 25/25 primary cells: **STRONG GENERALIZATION** under the frozen primary gate.

- Median `D_R = 0.106654` `[0.096655, 0.115510]`
- Median `D_A = 0.070283` `[0.062710, 0.077485]`
- Median `D_W = 0.016166` `[0.014089, 0.017096]`
- Mean per-round external regret, high/low bidder: FPA `0.000453 / 0.000088`; SPA `0.000077 / 0.000018`

Every primary valuation and horizon stratum passes. The independent-seed falsification below shows that the allocation magnitude is not stable for this learner at the selected representative environment.

## 6. Cross-learner comparison

Pairwise sign agreement across the 25 primary environments is 100% for both revenue and allocation:

| Pair | Revenue sign | Allocation sign |
|---|---:|---:|
| Hedge–FTPL | 1.00 | 1.00 |
| Hedge–Regret Matching | 1.00 | 1.00 |
| FTPL–Regret Matching | 1.00 | 1.00 |

## 7. Learner-specific failures

There are no primary disagreement cells and no primary gate failures. In falsification, regret matching's `D_A` is positive but only `0.000344–0.000924`, below `.01`; FTPL's `D_A` remains `0.075238–0.113848`.

## 8. Falsification

The addendum was frozen in commit `0cdd0a8` before its 120 runs. It used independent seeds `4000,...,4009`, the representative cell `(v=.50,H=25000,c_H=1,c_L=.5)`, a nearby valuation `.55`, and a doubled horizon `50000`.

- FTPL: 3/3 attacks pass the original joint gate.
- Regret matching: 0/3 pass. Revenue remains positive and clears magnitude, and allocation remains statistically positive, but allocation misses the preregistered `.01` economic threshold.

Thus FTPL is robust in this limited exercise; regret matching's strong primary result is seed-sensitive in effect magnitude.

## 9. Relationship to M8 theorem

**Theoretical result — Hedge:** M8 proves a finite-horizon conflict for its stated reduced action model and parameter rectangle.

**Computational cross-learner validation — FTPL / Regret Matching:** Level 5 supplies finite-grid empirical evidence only. The M8 theorem does not cover either learner.

## 10. Novelty implication

The primary result materially strengthens delegation robustness: the same mechanism-ranking conflict appears under exponential weighting, perturbed-leader selection, and positive-regret adaptation. The falsification qualification also shows that quantitative robustness can remain learner- and seed-dependent even when the primary sign structure agrees.

## 11. Publication readiness

**9/10** (previously 8/10). The project now has holdout evidence, Hedge theory, richer-action robustness, and preregistered cross-learner evidence. The regret-matching falsification limitation must be presented prominently.

## 12. Next gate

**TEST HETEROGENEOUS LEARNERS**. Do not launch it in this phase.

## 13. Repository and artifacts

- Primary analysis: `results/level_05/analysis/summary.json`, cell and paired-seed tables
- Falsification: `results/level_05/falsification_campaign/analysis/`
- Figures: `results/level_05/analysis/figures/`
- Figure 5 is explicitly a terminal-tail bid-distribution comparison because the frozen runner did not store within-run policy trajectories; no trajectory was fabricated.
- Historical Level-3 recovery evidence remains intentionally uncommitted and untouched.
