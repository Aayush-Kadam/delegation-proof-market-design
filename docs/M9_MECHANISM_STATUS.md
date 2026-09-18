# DELEGATION-PROOF MARKET DESIGN — M9 MECHANISM STATUS

## 1. Executive verdict

**TRADEOFF FRONTIER ONLY**

The known convex-combination family produces a smooth revenue/allocation frontier, but no coarse-grid interior alpha satisfies the prospectively frozen joint safety floors. Consequently no candidate was frozen, the holdout remains untouched, and the success level is **D0**.

## 2. Literature overlap

The payment interpolation is known. Syrgkanis explicitly discusses a hybrid auction where the winner pays a convex combination of its own and the second-highest bid. Learning-agent auction design is also established in work by Kolumbus–Nisan, Feng et al., Braverman et al., Aggarwal et al., and others. The prospective contribution tested here was delegation-robust selection across mixed learner populations, not invention of the family. See `docs/m9_literature_audit.md`.

## 3. Development/holdout split

The parameter-only split and selection rule were committed before any hybrid outcomes in `4e5c8ff5bf70a1e42da20418cfec04f7d101c03b`.

- Development: 15 environments, all nine profiles, five paired seeds.
- Holdout: 10 untouched environments, all nine profiles, 30 paired seeds.
- Both partitions cover all valuation levels and short/medium/long horizons.
- H/R, F/R, `v_L=.7,.9`, and prior reversal regions were retained as stress cases.

## 4. Mechanism family

The winner is the highest bidder under the existing fair tie rule and pays

`p_alpha = alpha*b_(1) + (1-alpha)*b_(2)`.

Thus `alpha=0` is SPA and `alpha=1` is FPA. The coarse grid was `0,.1,...,1`.

## 5. Coarse frontier

| alpha | Mean revenue | Mean allocation | Worst normalized revenue regret | Worst allocation regret | Worst joint regret | CVaR90 joint regret |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | .364700 | .984413 | 1.035120 | .000080 | 1.035120 | .693965 |
| 0.1 | .399966 | .981451 | .733148 | .024760 | .733148 | .550301 |
| 0.2 | .416868 | .976539 | .593666 | .053960 | .593666 | .469024 |
| 0.3 | .430549 | .969813 | .491898 | .090360 | .491898 | .403143 |
| 0.4 | .441431 | .961092 | .405841 | .138120 | .405841 | .343758 |
| 0.5 | .450718 | .950256 | .328534 | .214000 | .328534 | .286003 |
| 0.6 | .456611 | .940374 | .257002 | .228896 | .257002 | .231443 |
| 0.7 | .461240 | .930971 | .188695 | .253320 | .253320 | .224136 |
| 0.8 | .464142 | .922356 | .123590 | .279528 | .279528 | .247681 |
| 0.9 | .465916 | .913457 | .061174 | .299376 | .299376 | .267938 |
| 1.0 | .466266 | .904899 | .063555 | .328640 | .328640 | .285072 |

The frontier is monotone in its central economic tradeoff: moving toward FPA improves revenue robustness while sacrificing allocation robustness. Alpha `.9` minimizes the unconstrained global worst joint regret, but fails the allocation safety floor by a large margin. In the `v_L>=.7` stress subset, the best mean/worst compromise shifts toward roughly `.4-.5`, demonstrating that a single global alpha cannot simultaneously address the low- and high-valuation regimes.

## 6. Selected alpha

**None.**

No alpha satisfies both frozen eligibility conditions:

- worst normalized revenue regret `<=.25`;
- worst allocation regret `<=.10`.

The closest boundary point, alpha `.6`, has worst normalized revenue regret `.257002` and worst allocation regret `.228896`. Relaxing the floors after seeing this result is prohibited.

## 7. Selection criterion

Among eligible mechanisms the frozen rule minimized, lexicographically: worst joint regret, CVaR90, 95th percentile, mean joint regret, distance from `.5`, and then alpha. Since the eligible set is empty, no local refinement was authorized.

## 8. Development result

- Runs: 7,425/7,425 valid.
- Logical rounds: 190,575,000.
- Missing/duplicates/corrupt/identity mismatches/unexpected: 0/0/0/0/0.
- Worker failures/retries/pool restarts: 0/0/0.
- The family traces a meaningful average Pareto frontier but fails the preregistered worst-case joint constraints.

## 9. Frozen holdout result

**NOT OPENED.** The protocol forbids holdout execution without an eligible frozen candidate. All 10 holdout environments and seeds `8000,...,8029` remain untouched.

## 10. High-valuation reversal result

On development stress environments with `v_L>=.7`, alpha `.4` has mean joint regret `.08417`, alpha `.5` `.09377`, SPA `.14913`, and FPA `.16467`. This indicates that interpolation can improve the average stress-case compromise. It does not rescue the global worst-case eligibility failure and is not a holdout claim.

## 11. Role-robustness result

Revenue role sensitivity generally falls as alpha approaches FPA. For H/R, median revenue sensitivity declines from `.22210` at SPA to `.00681` at FPA; H/F falls from `.17930` to `.02104`. Allocation role sensitivity does not uniformly improve and often rises. Therefore no joint role-robustness claim is supported.

## 12. Red-team result

**NOT RUN.** The frozen protocol authorizes red-team testing only after a D2-or-higher holdout result.

## 13. Theory result

**NOT ATTEMPTED.** No candidate succeeded, so deriving candidate-specific hybrid Hedge theory would be post-selection work without a selected object.

## 14. Success level

**D0 — NO IMPROVEMENT under the preregistered eligibility rule.**

This does not mean every interior alpha is economically useless. It means the one-parameter family did not produce a defensible globally robust candidate under the frozen worst-case floors.

## 15. Limitations

- Development uses five seeds, adequate for frontier selection but not a powered final claim.
- Only the coarse alpha grid was evaluated because refinement was not authorized.
- Normalization makes low-valued environments stringent for revenue regret.
- A single state-independent alpha cannot adapt to the strong valuation-regime difference.
- No holdout, independent red team, or candidate theorem exists.

## 16. Publication readiness

**9/10**, unchanged. M9 contributes a clean preregistered negative design result and identifies why this family is inadequate, but it does not add a validated mechanism.

## 17. Exact remaining requirements for 10/10

- Integrate the full empirical/theory chain into a manuscript.
- Produce a clean reproducibility package and independent rerun instructions.
- Add an independently preregistered heterogeneous falsification study.
- Either validate a richer interpretable mechanism prospectively or frame the impossibility/tradeoff frontier rigorously enough to stand as the design conclusion.
- Complete external scholarly review of novelty and theorem statements.

## 18. Next gate

**TEST SECOND MECHANISM FAMILY**

A second family should be separately preregistered and motivated by the diagnosed regime conflict—most plausibly a capped or valuation-independent nonlinear interpolation—not tuned retroactively in M9.

## 19. Repository status

- Starting evidence commit: `c2204effe669c890497eac009786fb93cd6bb61b`.
- M9 preregistration commit: `4e5c8ff5bf70a1e42da20418cfec04f7d101c03b`.
- M9 analysis-tool commit: `1d290b3f475789b7e3393bdc75f85b882f8d6f71`.
- Development runs/logical rounds: 7,425 / 190,575,000.
- Holdout/red-team runs: 0 / 0.
- Failures/retries/restarts: 0/0/0.
- Tests and final evidence commit are reported after finalization.
