# DELEGATION-PROOF MARKET DESIGN — THEORY STATUS

## 1. Executive verdict

**RESTRICTED THEOREM PROVED**

The broad finite-horizon claim remains false, but a nonempty, explicit two-round conflict region is provable on the minimal asymmetric bid grid that retains the mechanism. This is a genuine theorem, not a floating-point generalization of the Level-3 surface.

## 2. Final theorem

**Theorem TH-M5-003 (two-round delegation conflict).** Let bidder values be `v_H=1` and `v_L=v`, with `0<v<2/5`. Let the high bidder's bids be `{0,v,1}` and the low bidder's bids be `{0,v}`. Ties are split uniformly. Both bidders start from uniform weights and use deterministic full-information Hedge

`w_i^{t+1}(b)=w_i^t(b) exp(eta_i u_i^t(b))`, `pi_i^t(b)=w_i^t(b)/sum_a w_i^t(a)`.

Run the FPA and SPA separately for `H=2`, with the same positive rates `(eta_H,eta_L)`. Define

`Q_F=softmax(eta_H(1/4,3(1-v)/4,0))`, `p_F=(1+exp(eta_L v/6))^{-1}`,

`Q_S=softmax(eta_H(1/4,(3-v)/4,1-v/2))`, `p_S=(1+exp(-eta_L v/6))^{-1}`,

where `Q_M=(q_M0,q_Mv,q_M1)` and `p_M` is the low bidder's probability of bid `v` in round two. Put

`Phi(v,eta_H,eta_L) = [q_S0(1-p_S)/2 + q_Sv(1-p_S/2)+q_S1] - [q_F0(1-p_F)/2 + q_Fv(1-p_F/2)+q_F1]`.

On the explicit region

`C_2={(v,eta_H,eta_L): 0<v<2/5, eta_H>0, eta_L>=0, Phi(v,eta_H,eta_L)>0}`,

time-average FPA revenue strictly exceeds time-average SPA revenue and time-average SPA allocation efficiency strictly exceeds FPA allocation efficiency. In particular,

`R_FPA(2)-R_SPA(2) >= (2-5v)/12 > 0`,

`A_SPA(2)-A_FPA(2)=Phi/2>0`.

The region is nonempty: `(v,eta_H,eta_L)=(1/3,1,1/10)` has exact analytic revenue lower bound `1/36` (actual gap `0.3544...`) and interval-certified allocation gap `0.04334...`. Exact rational arithmetic with a 40-term exponential Taylor remainder certifies positivity; the decimals are summaries, not premises. Continuity gives an open neighborhood around that point.

## 3. Assumptions

- Two persistent values, one item, independent mean-field mixed play.
- No overbidding; high grid `{0,v,1}`, low grid `{0,v}`.
- FPA winner pays own bid; SPA winner pays opponent's bid.
- Fair tie breaking, including expected payment and utility in ties.
- Full-information Hedge, uniform initial weights, fixed nonnegative learning rates.
- Two-round time average. The result does not claim long-horizon persistence or cover the `.01` Level-3 grid.

## 4. Proof outline

At the uniform first round the high bidder wins with probability `2/3` in both mechanisms. FPA and SPA revenues are `(3v+2)/6` and `v/3`; hence the first-round FPA advantage is `(v+2)/6`.

Against the uniform opponent, the high bidder's payoff vectors on `{0,v,1}` are

- FPA: `(1/4,3(1-v)/4,0)`;
- SPA: `(1/4,(3-v)/4,1-v/2)`.

The low bidder's vectors on `{0,v}` are `(v/6,0)` in FPA and `(v/6,v/3)` in SPA. One Hedge update therefore gives exactly `Q_F,p_F,Q_S,p_S` above. In round two,

`A_M=q_M0(1-p_M)/2+q_Mv(1-p_M/2)+q_M1`,

`R_F=v(q_Fv+p_F q_F0)+q_F1`, and `R_S=v p_S(q_Sv+q_S1)`.

The allocation conclusion is the defining explicit inequality `Phi>0`. For revenue, round-two FPA revenue is nonnegative and SPA revenue is at most `v`; combining this with the exact first-round advantage and dividing by two gives `(2-5v)/12`. This is positive precisely under the theorem's simple value restriction.

For any actions `a,b`, Hedge also obeys the reusable identity

`log(w_i^t(a)/w_i^t(b))=log(w_i^1(a)/w_i^1(b))+eta_i sum_{s<t}[u_i^s(a)-u_i^s(b)]`.

Thus a per-round gap at least `gamma` implies a weight-ratio multiplier at least `exp(eta_i gamma(t-1))`. The two-round theorem uses its one-update equality rather than an asymptotic concentration approximation.

## 5. Explicit conflict region

The theorem's region is `C_2` above. It is closed-form and directly checkable; it is not a fitted threshold. The conservative revenue face is `v<2/5`, while the allocation face is the exact exponential inequality `Phi>0`. The certificate point proves nonemptiness.

## 6. Boundary intuition

SPA adds an increasing payoff tilt `(0,v/2,1-v/2)` to the high bidder's three actions relative to FPA. It especially rewards bid `1`, which always wins but costs the high bidder nothing beyond the opponent's bid. In FPA, bid `1` gives the high bidder zero surplus. This makes SPA protect allocation faster. FPA nevertheless collects a large payment immediately from uniform exploration; for `v<2/5`, even the worst possible second SPA round cannot erase that advantage.

The proof deliberately does not explain the full long-horizon interior surface. Its low-`v` revenue guarantee is absolute while Level 3 uses normalized and economically meaningful gates; as `v` approaches zero, the available benchmark revenue also vanishes. Near `v=1`, the coarse revenue bound changes sign and the value asymmetry driving welfare effects disappears.

## 7. Comparison with Level 3

The theorem proves the same qualitative objective conflict and identifies the same high-bidder SPA force, but only for `H=2` on a three-by-two grid. It does not explain all of the `.01`-grid holdout surface, the stronger interior support, or rate-dependent long-horizon reversals. It is a minimal mechanism theorem, not a theorem-level restatement of the empirical result.

## 8. Counterexamples and limits

- The symmetric `{0,v}`/`{0,v}` reduction fails: after one equal-rate update, SPA allocation moves slightly in the wrong direction. The high bidder's action `1` is essential to this proof.
- The known M4 counterexample `(v,H,c_H,c_L)=(.75,1600,1,2)` remains and rejects universal FPA revenue dominance.
- `750` deterministic two-round environments were scanned for theorem discovery/falsification; the scan is numerical support only. It found an allocation-sign failure at `(v,eta_H,eta_L)=(.95,.25,8)`, outside `C_2`. The proof does not depend on the scan.
- Outside `Phi>0`, the theorem is silent. At `v>=2/5`, its coarse revenue argument is also silent, even when the exact gap is positive.

## 9. Literature novelty

**POSSIBLY DISTINCT.** The nearest work proves asymptotic/convergence or one-objective guarantees: Kolumbus–Nisan analyze regret-minimizing bidders and FPA/SPA behavior; Aggarwal et al. prove runner-up non-truthfulness, rate effects, and auctioneer-regret bounds; Feng et al. prove mean-based convergence under stochastic values/exploration; Hoy–Jain–Wilkens derive FPA revenue guarantees from behavioral axioms; Syrgkanis et al. connect no-regret dynamics to welfare in smooth games; Ipsen–Skoulakis give finite-time FPA revenue bounds under approximate CE/no-swap regret. None located states this exact finite-horizon, fixed-Hedge, simultaneous revenue-versus-allocation ranking. The distinction is narrow because the theorem is a two-round small-grid result.

## 10. Publication readiness

**5/10.** The project now has a correct theorem exposing the minimal mechanism, but the theorem is too restricted to carry the Level-3 empirical surface by itself.

## 11. Next gate

**STRENGTHEN THEORY FURTHER**

## 12. Estimated next-phase compute

Before Level 5, a proof-led extension should use at most `1,000` deterministic configurations, zero stochastic seeds, and horizons up to roughly `10,000` only where recurrence bounds are evaluated. Expected machine time is under 30 minutes; no new holdout is authorized.

## Result registry

| ID | Status | Result |
|---|---|---|
| TH-M5-001 | DISPROVEN | Symmetric two-action grid yields the target two-round allocation sign. |
| TH-M5-002 | COUNTEREXAMPLE | Universal finite-horizon FPA revenue dominance; M4 counterexample preserved. |
| TH-M5-003 | THEOREM | Explicit two-round three-by-two conflict region `C_2`. |
| TH-M5-004 | RESTRICTED-PROPOSITION | Hedge cumulative log-weight ratio identity and concentration consequence. |

## Analytic versus computational role

- **ANALYTIC PROOF:** payoff vectors, Hedge/softmax formulas, definition of `C_2`, allocation identity, revenue lower bound, welfare corollary.
- **INTERVAL CERTIFICATION:** nonemptiness witness `(1/3,1,1/10)` using exact fractions and a rigorous Taylor remainder bound.
- **NUMERICAL SUPPORT:** the 750-environment boundary/counterexample scan and representative table. Neither is used as a proof premise.
