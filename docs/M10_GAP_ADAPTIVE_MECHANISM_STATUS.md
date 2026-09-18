# DELEGATION-PROOF MARKET DESIGN — M10 GAP-ADAPTIVE MECHANISM STATUS

## 1. Executive verdict

**SECOND FAMILY FAILED DEVELOPMENT GATE**

No coarse gap-adaptive candidate satisfied the unchanged M9 safety floors, and none came within the preregistered `.02` refinement tolerance of both floors. No candidate was frozen; the M9 holdout remains unopened. Success level: **G0**.

## 2. Literature overlap

Hybrid first-/second-price rules, gap rules in other auction constructions, robust auction design, and mechanisms for adaptive bidders are known. The targeted pre-outcome search did not locate the exact normalized-gap interpolation with the same delegation-robust claim. This is not proof of formula novelty, so M10 makes no invention claim. See `docs/m10_literature_audit.md`.

## 3. Mechanism equation

For top and second bids `b1>=b2`,

`g=0` if `b1=0`, otherwise `g=(b1-b2)/b1`,

`alpha(g;a,tau)=a+(1-a)*min(g/tau,1)`,

and the winner pays

`p_(a,tau)=b2+alpha(g;a,tau)*(b1-b2)`.

The implementation verifies `b2<=p<=b1`, scale-free normalized gap, deterministic payment conditional on bids, fair existing tie-breaking, zero-bid behavior, monotonic interpolation, and threshold saturation.

## 4. Frozen development search

- `a in {.20,.35,.50}`.
- `tau in {.20,.40,.60,.80}`.
- 12 candidates, 15 M9 development environments, 9 learner profiles, 3 paired existing development seeds.
- New runs: 4,860.
- Logical rounds: 124,740,000.
- M9 endpoints on matching seeds were reused, not rerun.
- Protocol and implementation frozen in commit `673b4a1ffe5c92f1c567c4cfb4b42663fa856dfd` before outcomes.

## 5. Coarse results

| a | tau | Worst q_R | Worst q_A | Worst joint | Mean joint | Mean gap | Mean realized alpha |
|---:|---:|---:|---:|---:|---:|---:|---:|
| .50 | .20 | .483696 | .317733 | .483696 | .102570 | .196854 | .740676 |
| .35 | .20 | .489957 | .324267 | .489957 | .102935 | .198130 | .664562 |
| .50 | .80 | .495053 | .277267 | .495053 | .098567 | .210747 | .627411 |
| .50 | .40 | .495899 | .318000 | .495899 | .098970 | .202199 | .683157 |
| .20 | .20 | .496250 | .343933 | .496250 | .103387 | .197788 | .588636 |

The table reports the five smallest worst-joint-regret candidates. Full results are in `results/m10/development/analysis/coarse_frontier.csv`. Every candidate fails both floors materially.

## 6. Refinement

**NOT TRIGGERED.** Frozen refinement required eligibility or a candidate missing each floor by at most `.02`. Eligible count: 0. Near-eligible count: 0.

## 7. Selected `(a,tau)`

**None.**

## 8. Development safety floors

Required:

- `max q_R<=.25`;
- `max q_A<=.10`.

The smallest observed worst revenue regret was `.483696`; the smallest observed worst allocation regret was approximately `.264`. The second family therefore misses the revenue floor by at least `.233696` and the allocation floor by at least roughly `.164`.

## 9. Bid-gap mechanism diagnostics

The proposed state signal behaves in the intended direction:

| v_L | Mean normalized gap | Mean realized alpha |
|---:|---:|---:|
| .1 | .356065 | .731476 |
| .3 | .261456 | .632072 |
| .5 | .213051 | .587784 |
| .7 | .132639 | .510172 |
| .9 | .071775 | .447498 |

Thus weak competition produces larger gaps and more FPA-like payments, while high valuations produce smaller gaps and more moderate payments. The engineering/economic mechanism activates exactly as intended; the failure is that this signal is insufficient to control worst-case objective regret across learner/environment cells.

## 10. High-`v_L` result

Joint regret rises sharply at `v_L=.9` despite the lower realized alpha. Mean joint regret by valuation, pooled over candidates, is `.12267,.04199,.05129,.07622,.19777` for `v_L=.1,.3,.5,.7,.9`. The gap rule recognizes high competition but does not preserve enough revenue and allocation robustness in the hardest high-valuation cells.

## 11. H/R and F/R stress result

H/R can perform locally well: `(a=.20,tau=.60)` has H/R mean/worst joint regret `.04896/.10107`. F/R remains substantially harder: its best listed worst joint regret is `.38338` at `(.50,.20)`. Good behavior in H/R does not compensate for failure across the full learner/environment family.

## 12. Holdout status

**UNOPENED.** No `results/m9/holdout` data were created.

## 13. Holdout result

**NOT RUN — development failure.**

## 14. Role-sensitivity result

GAH often reduces median revenue sensitivity between role swaps, but allocation tail sensitivity remains material. For F/R, allocation-sensitivity p95 ranges roughly `.150-.213` for several candidates. No candidate clears the primary floors, so no delegation-role robustness claim is made.

## 15. Red-team result

**NOT RUN.** Red-team execution requires holdout success.

## 16. Theory result

**NOT ATTEMPTED.** Candidate-specific theory requires a successful holdout candidate.

## 17. Success level

**G0 — candidate fails development.**

Together, M9 and M10 show that neither constant nor this bid-gap-adaptive interpolation satisfies the stringent frozen revenue/allocation robustness floors across the full delegated learner population. This is evidence of a design limitation for these two simple families, not a universal impossibility theorem.

## 18. Publication readiness

**9/10**, unchanged. M10 adds a clean prospective negative result and sharper diagnosis, but no validated mechanism or formal impossibility theorem.

## 19. Exact requirements remaining for 10/10

- Manuscript integration of positive findings and both prospective design failures.
- Independent heterogeneous falsification and reproducibility packaging.
- Formalize the mechanism-family limitation or clearly bound its scope.
- External novelty/theorem review.
- If further design is pursued, preregister it as a new phase rather than extending M10 post hoc.

## 20. Next gate

**FORMALIZE DESIGN LIMITATION**

Do not test a third mechanism family automatically. First determine whether the M9/M10 frontier failures admit a useful lower bound or impossibility-style proposition for simple interpolation rules.

## 21. Repository status

- Starting M9 commit: `37d808ab69fa18c1e22c18a57e6cc9f9a043fab1`.
- M10 protocol commit: `673b4a1ffe5c92f1c567c4cfb4b42663fa856dfd`.
- M10 analysis-tool commit: `7a8d0799d86faec9a2adc0d5895bdadc374990c3`.
- Development: 4,860 runs / 124,740,000 rounds.
- Missing/duplicates/corrupt/mismatched/unexpected: 0/0/0/0/0.
- Failures/retries/restarts: 0/0/0.
- Refinement/holdout/red-team runs: 0/0/0.
- Final tests and evidence commit are reported after finalization.
