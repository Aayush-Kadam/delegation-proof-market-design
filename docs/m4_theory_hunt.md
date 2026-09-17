# M4 theory hunt

No statement below is registered as a theorem. Each was attacked with literature, accounting, exact matrices, or the tiny deterministic Hedge calculation.

| Candidate | Status | Assumptions | Evidence / attack | Literature overlap | Next proof step |
|---|---|---|---|---|---|
| T1. `Delta_W=(1-v)Delta_E` in the persistent two-bidder model | RESTRICTED-PROPOSITION | One item always allocated; values `(1,v)` | Exact accounting proof in `m4_formalization.md` | Elementary welfare accounting | None; use as simplification, not contribution |
| T2. External regret alone yields a vanishing SPA seller-revenue loss | COUNTEREXAMPLE FOUND | Only no-overbid external regret | Zero-regret path `(b_H,b_L)=(1,0)` has revenue zero forever | Kolumbus--Nisan and Aggarwal et al. establish the broader obstruction | Abandon without stronger assumptions |
| T3. FPA revenue exceeds SPA revenue for every tiny-grid Hedge environment | COUNTEREXAMPLE FOUND | Exact mean-field Hedge, `.25` grid | Fails at `(.75,1600,1,2)`; SPA revenue is higher | Dynamic FPA guarantees require behavioral/equilibrium assumptions | Restrict to an explicit parameter region |
| T4. A nonempty finite-horizon mean-field Hedge region has `Delta_R<0<Delta_E` | THEOREM-POSSIBLE | Two persistent values, finite grid, full-information deterministic mean-field MWU, specified initialization and rates | Sign conflict in 59/60 exact tiny cells and 54/75 stochastic holdout cells | Ingredients known; no matching joint finite-time region theorem found | Derive finite-time log-weight-ratio bounds that certify both inequalities over an explicit region |
| T5. The conflict admits a universal scalar boundary `v*(H)` | NOT TRACTABLE as stated | Would need rate-independent monotonicity | Holdout rate pairs cross floors differently; no horizon reversal; thresholds create part of the boundary | No matching theorem found, but empirical premise is absent | Replace with a multi-parameter sufficient region, not a scalar boundary |

## Strongest theorem target

**Finite-time objective-conflict region for deterministic mean-field Hedge.** For explicit grid spacing `epsilon`, uniform initialization, persistent values `(1,v)`, and rate constants `(c_H,c_L)` in a stated compact set, derive computable sufficient conditions on `(v,H,c_H,c_L,epsilon)` such that

`R_FPA(H)-R_SPA(H) >= v tau_R`

and

`A_SPA(H)-A_FPA(H) >= min(tau_E,tau_W/(1-v))`.

The theorem must exhibit a nonempty region and may not assert universality. Its proof should control Hedge log-weight ratios using exact payoff-gradient gaps, separately for the high bidder's allocation-support movement and the low bidder's SPA runner-up mass. A successful proof would convert the possibly distinct computational surface into a genuine finite-time contribution. Failure would leave the result mostly an empirical recombination of known mechanisms.
