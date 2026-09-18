# DELEGATION-PROOF MARKET DESIGN — HETEROGENEOUS LEARNER STATUS

## 1. Executive verdict

**HETEROGENEOUS ROBUSTNESS** under the frozen gate. Five of six ordered profiles are strong or partial, no profile reverses either aggregate median, and the sixth is direction-only. This is materially weaker than homogeneous Level 5: role assignment changes gate outcomes and creates revenue-ranking reversals in high-valuation cells.

## 2. Frozen protocol

- Protocol commit: `ddbad29`
- Main-config SHA-256: `94a4a4c18eafce6755ace88522a3fca5e92ee2ee7ccf4758e43110290628037d`
- Profiles: `H/F`, `F/H`, `H/R`, `R/H`, `F/R`, `R/F`; first learner is the high-value bidder
- 25 frozen Level-5 environments; seeds `6000,...,6029`; FPA and SPA
- 9,000 mechanism runs; 288,000,000 logical auction rounds
- Unchanged cell gate: `D_R/v >= .05`, `D_A >= .01`, with paired normal 95% CI lower endpoints for raw `D_R,D_A` above zero

## 3. Completeness

9,000 expected and 9,000 unique valid records; zero missing, duplicates, corrupt outputs, unexpected IDs, or identity mismatches. All frozen hashes match. Worker failures/retries/pool restarts: `0/0/0`.

## 4. Ordered-profile results

Intervals are deterministic bootstrap 95% intervals for the median of 25 cell means. Cell gates use the frozen paired normal intervals.

| Ordered profile | Gate cells | Median D_R [95% CI] | Median D_A [95% CI] | Median D_W [95% CI] | Classification |
|---|---:|---:|---:|---:|---|
| H/F | 13/25 | 0.037176 [-0.005319, 0.042728] | 0.084021 [0.036324, 0.153363] | 0.025654 [0.021572, 0.033381] | PARTIAL ROBUSTNESS |
| F/H | 19/25 | 0.170537 [0.154252, 0.237339] | 0.035280 [0.014391, 0.120789] | 0.018302 [0.009022, 0.025020] | STRONG ROBUSTNESS |
| H/R | 2/25 | 0.014794 [-0.001118, 0.019801] | 0.021432 [0.006129, 0.076617] | 0.010716 [0.004291, 0.021915] | DIRECTION-ONLY |
| R/H | 15/25 | 0.245904 [0.158853, 0.311459] | 0.017869 [0.001492, 0.102076] | 0.008935 [0.001044, 0.020967] | STRONG ROBUSTNESS |
| F/R | 14/25 | 0.148903 [0.122371, 0.164982] | 0.012840 [0.004731, 0.046604] | 0.005502 [0.003311, 0.013981] | PARTIAL ROBUSTNESS |
| R/F | 11/25 | 0.028907 [-0.000721, 0.035471] | 0.072129 [0.030693, 0.135060] | 0.021842 [0.019082, 0.028343] | PARTIAL ROBUSTNESS |

Valuation is central. H/F, H/R, and R/F lose FPA revenue dominance throughout most or all `v=.7,.9` cells while retaining a strong SPA allocation advantage. F/H and R/H instead become strongest at high valuations. Horizon generally reduces allocation magnitude in profiles with FTPL or RM in the high-value role, but the ordering effect is larger than the horizon effect.

## 5. Role-swap analysis

| Swap contrast | Median Gamma_R [95% CI] | Median Gamma_A [95% CI] | Gate changed | Revenue sign changed | Allocation sign changed |
|---|---:|---:|---:|---:|---:|
| H/F minus F/H | -0.195584 [-0.220302, -0.109459] | 0.019573 [0.011627, 0.024049] | 72% | 40% | 0% |
| H/R minus R/H | -0.230792 [-0.323643, -0.138323] | 0.001900 [-0.006290, 0.007753] | 68% | 36% | 0% |
| F/R minus R/F | 0.152646 [0.104938, 0.174222] | -0.027415 [-0.049127, -0.017856] | 68% | 40% | 0% |

Learner role is therefore an economically material experimental primitive. Assigning FTPL or RM to the high-value role typically increases FPA's revenue advantage but reduces SPA's allocation advantage. These are experimental associations, not claims of causal invariance outside the frozen design.

## 6. Regret-Matching role dependence

RM's role strongly matters. R/H is strong (15/25) with the largest median revenue gap; H/R is direction-only (2/25) with the smallest median revenue gap. F/R is partial (14/25) and R/F is partial (11/25), but they trade revenue against allocation magnitude. Quantitative instability is therefore concentrated particularly when RM is the low bidder opposite Hedge, not uniformly whenever RM appears.

RM's external regret is very low in either role. Low regret does not imply preservation of the joint economic-magnitude gate: H/R combines low RM regret with only 2/25 passing cells.

## 7. Homogeneous versus heterogeneous comparison

| Profile | Gate cells | Median D_R | Median D_A | Median D_W |
|---|---:|---:|---:|---:|
| H/H | 25 | 0.104907 | 0.067163 | 0.016860 |
| F/F | 25 | 0.109278 | 0.070892 | 0.017381 |
| R/R | 25 | 0.106654 | 0.070283 | 0.016166 |
| H/F | 13 | 0.037176 | 0.084021 | 0.025654 |
| F/H | 19 | 0.170537 | 0.035280 | 0.018302 |
| H/R | 2 | 0.014794 | 0.021432 | 0.010716 |
| R/H | 15 | 0.245904 | 0.017869 | 0.008935 |
| F/R | 14 | 0.148903 | 0.012840 | 0.005502 |
| R/F | 11 | 0.028907 | 0.072129 | 0.021842 |

Mixing learners materially weakens uniform gate support and creates role-dependent tradeoffs absent from the 25/25 homogeneous primary tables.

## 8. Mechanism-ranking reversals

There are 29 profile/environment reversal cells, all with `D_R<0` and `D_A>0`; no allocation reversal occurs. They comprise H/F (10 cells), H/R (9), and R/F (10), concentrated at `v=.7` and `.9`. Thus SPA can dominate both revenue and allocation in those cells. The complete list is in `results/heterogeneous/analysis/ranking_reversals.csv`.

Across environments, all six profiles jointly have positive `D_R,D_A` in 15/25 environments; at least four profiles do so in 16/25.

## 9. Falsification

No falsification was run. The frozen heterogeneous protocol specifies no falsification addendum, selection rule, seeds, or perturbations. Adding one after observing results would not be preregistered.

## 10. Economic interpretation

Heterogeneous learning preserves the aggregate revenue-allocation conflict but changes its strength and sometimes its sign. A learner placed in the high-value role controls how quickly winning probability concentrates; the low-value learner affects competitive pressure and the price path. Swapping the same two algorithms can therefore move FPA revenue substantially while leaving the direction of SPA's allocation advantage intact.

## 11. Relationship to M8 theorem

**M8 theory:** homogeneous Hedge in its stated reduced model only.

**Heterogeneous result:** computational evidence on the `.01` bid grid. No theorem presently covers mixed algorithms.

## 12. Novelty interpretation

The targeted audit found established work on heterogeneous buyer behavior, mean-based learning in auctions, bidder convergence, and strategizing against online learners. It did not identify a prior result matching this exact finite-horizon claim: an FPA/SPA revenue-allocation ranking comparison across ordered mixtures of Hedge, FTPL, and regret matching with role-dependent reversals. Classification: **POSSIBLY DISTINCT APPLICATION**, while the general fact that heterogeneous learning dynamics matter is known.

## 13. Limitations

- Full-information, two-bidder, persistent-value simulations on a fixed discrete grid.
- Only three classical learner families and one frozen hyperparameter scheme.
- Cell estimates use 30 seeds; some median bootstrap intervals include zero.
- No heterogeneous theorem and no preregistered post-primary falsification.
- The 29 revenue reversals show the conflict is not universally robust.

## 14. Publication readiness

**9/10**, unchanged. Evidence is materially stronger, but manuscript integration, heterogeneous falsification, and theory remain incomplete.

## 15. Recommended next gate

**DESIGN DELEGATION-ROBUST MECHANISM**

## 16. Repository status

- Tests: reported after final verification
- Primary runs: 9,000; pilot runs: 600; falsification runs: 0
- Primary logical rounds: 288,000,000
- Failures/retries/restarts: `0/0/0`
- Historical recovery evidence remains intentionally uncommitted

