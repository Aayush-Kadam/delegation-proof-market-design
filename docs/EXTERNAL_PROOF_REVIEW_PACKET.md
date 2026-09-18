# External proof review packet

**Status: EXTERNAL REVIEW PACKAGE READY. This is not an external verification claim.**

## Results for review

1. M6 3x2 finite-horizon rectangle: `docs/m6_proof.md`.
2. M8 4x3 richer-action rectangle and endogenous-history stability lemma: `docs/m8_proof.md`.
3. M11 L1 constant-hybrid limitation: `docs/m11_design_limitation_proof.md`.

## M11 assumptions

Two persistent-value bidders with values `(1,1/3)`; action sets `{0,v/2,v,1}` and `{0,v/2,v}`; fair ties; uniform initial weights; deterministic full-information Hedge; learning rates `(4,0)`; horizon nine; winner-preserving constant payment interpolation.

## Certificate command

```text
python -c "from pathlib import Path; from delegation_market.m11_interval import certify; certify(Path('results/m11/constant_alpha_certificate.review.json'))"
```

The default is 10,000 outward-rounded subintervals. Reviewers should verify directed rounding, dual-interval differentiation, payoff matrices, threshold bracketing, and independence from floating-point discovery code.

## Known counterexamples and boundaries

- 109 of 1,500 audited parameter/horizon configurations violate at least one sampled global-monotonicity condition.
- `(v,eta_H,eta_L,H)=(.1,2,0,9)` has a locally negative revenue derivative.
- M8 does not prove the full `.01`-grid empirical surface.
- The action-expansion transfer theorem is conditional and too loose under uniform initialization for the direct 4x3 result.
- No theorem covers FTPL, regret matching, heterogeneous learner pairs, or all gap-dependent mechanisms.

## Questions for reviewers

1. Are all counterfactual full-information utilities and tie cases correct?
2. Is the interval implementation genuinely outward rounded at every operation?
3. Are the theorem statements no broader than the certificates?
4. Is the welfare corollary stated only where the allocation identity applies?
5. Does the M11 midpoint-safety definition support the exact impossibility conclusion claimed?

