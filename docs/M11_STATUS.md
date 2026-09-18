# DELEGATION-PROOF MARKET DESIGN — M11 DESIGN LIMITATION STATUS

## 1. Executive verdict

**CONSTANT-HYBRID IMPOSSIBILITY PROVED**

M11 reaches limitation level **L1**. It proves an explicit finite-horizon delegated-Hedge environment in which no constant interpolation preserves at least half of both the SPA allocation advantage and FPA revenue advantage.

## 2. Strongest theorem

In the deterministic mean-field 4x3 Hedge model with values `(1,1/3)`, action sets `{0,v/2,v,1}` and `{0,v/2,v}`, uniform initial weights, fair ties, `eta_H=4`, `eta_L=0`, and `H=9`, consider `p_alpha=b_(2)+alpha(b_(1)-b_(2))`.

Revenue is strictly increasing and high-value allocation is strictly decreasing for every `alpha in [0,1]`. Let each objective's safety level be the midpoint of its SPA and FPA endpoint values. Revenue safety implies `alpha>.36`; allocation safety implies `alpha<.22`. Therefore no constant alpha satisfies both.

## 3. Mechanism class covered

C0 only: constant winner-preserving interpolation between second and first price. The theorem does not cover arbitrary gap rules C1/C2 or all top-two payment functions.

## 4. Parameter/environment region

One certified explicit point: `v=1/3, eta_H=4, eta_L=0, H=9`, within the existing exact 4x3 reduced action model. An open neighborhood is plausible by strict margins but was not interval-certified and is not claimed.

## 5. Revenue monotonicity result

Globally certified `R'(alpha) in [.0214157305,.6787484144]`.

## 6. Allocation monotonicity result

Globally certified `A'(alpha) in [-.5127730196,-.0426592879]`.

## 7. Conflicting safety requirements

Endpoint-midpoint safety gives `R_half=.2467916510` and `A_half=.8444824553`. Certification brackets the revenue threshold inside `(.36,.37)` and allocation threshold inside `(.21,.22)`.

## 8. Constant-alpha implication

No `alpha in [0,1]` simultaneously achieves both midpoint guarantees. This gives a formal structural explanation for a constant-family frontier, without importing M9's empirical thresholds as theorem assumptions.

## 9. Gap-adaptive implication

No gap-only impossibility is proved. M10 remains prospective empirical evidence that one natural monotone gap family fails. M11 shows gap observability is lossy and endogenous, but does not cover all `phi(g)`.

## 10. Observable-state collision

Uniform-initialization gap distributions overlap by `5/6` between reduced `v=.1` and `.9` environments, with TV `1/6` and Wasserstein-1 `.1`. Exact gap observations therefore do not uniquely identify the regime. This is diagnostic support, not an L2 theorem.

## 11. Counterexamples

Of 1,500 deterministic configurations, 109 violate at least one sampled global monotonicity condition. At `(.1,2,0,9)`, revenue becomes locally decreasing for intermediate alpha. Universal monotonicity and L3 claims are rejected.

## 12. Relationship to M9

M9 prospectively established failure of the constant family under broad empirical worst-case floors. M11 supplies an independent reduced-model theorem showing incompatible constant-alpha requirements under primitive midpoint safety guarantees.

## 13. Relationship to M10

M10 showed the bid gap tracks competitive intensity but its specified adaptive family fails development. M11 identifies substantial cross-regime gap overlap and the endogenous feedback loop, but stops short of a theorem for all gap-only rules.

## 14. Literature novelty

Revenue-efficiency tradeoffs and robust-mechanism impossibilities are known. The specific finite-horizon delegated-Hedge constant-interpolation incompatibility appears possibly distinct in the targeted audit. No broad auction-impossibility novelty is claimed.

## 15. Limitation level

**L1 — CONSTANT-HYBRID IMPOSSIBILITY.**

## 16. Publication readiness

**9/10**, unchanged. The theorem materially strengthens the paper, but the manuscript and external reproducibility/novelty review remain incomplete.

## 17. Exact remaining requirements for 10/10

- Independent theorem verification and reproduction of the interval certificate.
- Manuscript integration with precise separation of theorem, empirical evidence, and conjecture.
- Independent heterogeneous falsification or explicit justification for its omission.
- Complete reproducibility package and external novelty review.

## 18. Next gate

**WRITE FINAL PAPER**

## 19. Repository status

- Starting commit: `87621d073e0159492b4de0e391f44c0a1c22bdeb`.
- Deterministic parameter configurations audited: 1,500.
- Continuous alpha certificate: 10,000 outward interval subboxes for one fixed witness.
- Mechanism holdout: unopened.
- Final tests and commit are reported after finalization.
