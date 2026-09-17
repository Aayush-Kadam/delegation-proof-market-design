# DELEGATION-PROOF MARKET DESIGN — M4 STATUS

## 1. Executive verdict

**PROMISING BUT NARROW**

Level 3 is real and reproducible. Most ingredients are already known, but the prospectively validated joint finite-horizon conflict surface may support a narrow contribution if converted into an explicit finite-time theorem. There is not yet a strong novelty residual.

## 2. Exact Level 3 result

For two persistent-value bidders `(1,v)`, no-overbid `.01` grids, full-information Hedge with `eta_i=c_i sqrt(log K_i/H)`, and FPA versus SPA, define normalized seller-revenue loss `NDL_R=(v-R)/v`, allocation loss `DL_E=1-Pr(H wins)`, and welfare loss `DL_W=1-W`. Let `Delta` denote FPA minus SPA loss.

The selected development cell `(v,H,c_H,c_L)=(.2,10,000,.5,1)` produced `Delta_R=-.662153`, `Delta_E=.012983`, and `Delta_W=.010387`, all with paired CIs excluding zero. All eight falsification attacks passed.

Across 75 independent frozen holdout environments (2,250 paired seeds), `Delta_R<0` in 72 cells and both `Delta_E>0` and `Delta_W>0` in all 75. Fifty-four cells satisfy the preregistered joint economic/significance gate. Support by value is 1/15 at `.1`, 15/15 at `.3`, 15/15 at `.5`, 15/15 at `.7`, and 8/15 at `.9`. The high bidder's surplus is lower under FPA in all 75 cells; total bidder surplus is lower in 74.

## 3. Literature overlap

- Kolumbus--Nisan already provide the persistent-value regret-minimizer FPA/SPA framework and FPA convergence near the second-price outcome under mean-based/CCE conditions.
- Aggarwal--Gupta--Perlroth--Velegkas already establish persistent runner-up non-truthfulness in deterministic truthful auctions, qualitative learning-rate effects, and finite-time auctioneer-regret rates.
- Hoy--Jain--Wilkens already give behavioral conditions under which repeated FPA revenue is at least SPA revenue.
- Feng et al. establish mean-based equilibrium-selection/allocation convergence in repeated auctions under a different stochastic-value model.
- Syrgkanis et al. and auction smoothness results already connect no regret to welfare.
- Ipsen--Skoulakis (2026) give polynomial finite-time FPA revenue bounds under approximate correlated equilibrium/no-swap regret.

Therefore broad revenue, efficiency, horizon, rate, and regret-to-welfare claims are not new.

## 4. Novelty residual

**Prior work separately explains FPA revenue robustness, SPA runner-up shading, allocation convergence, and learning-rate effects; Level 3 adds a prospectively frozen, paired finite-horizon map showing that these ingredients jointly produce an objective-specific mechanism-ranking conflict over a broad interior persistent-value region, with seller revenue favoring FPA while allocation, welfare, and high-bidder surplus favor SPA.**

Classification: possibly distinct but presently computational, not theorem-level.

## 5. Formal framework

For environment `z=(v,c_H,c_L,epsilon)`, define

`Delta_R(H,z)=NDL_R(FPA,H,z)-NDL_R(SPA,H,z)`

and

`Delta_E(H,z)=DL_E(FPA,H,z)-DL_E(SPA,H,z)`.

The sign-conflict region is `C_sign={(H,z): Delta_R<0<Delta_E}`. The frozen meaningful region additionally requires `Delta_R<=-.05` and either `Delta_E>=.01` or `Delta_W>=.005`, with paired confidence intervals excluding zero in the specified directions.

Exactly, `Delta_W=(1-v)Delta_E`; welfare and allocation are not independent in this model. Also `S_FPA-S_SPA=v Delta_R-Delta_W`, so the conflict signs imply lower total bidder surplus under FPA.

## 6. Mechanism explanation

SPA lets the high bidder raise its bid to protect allocation without raising its own payment, but the losing bidder can retain low-bid mass because many losing actions have the same zero payoff. Allocation becomes efficient before the runner-up bid becomes revenue-revealing. FPA makes the winning own bid the payment; competition pushes relevant mass toward the low value and protects revenue, while simultaneous exploration creates more inefficient low-bidder wins. The seller/high-bidder surplus split changes accordingly.

The region is interior because it requires both a dollar revenue advantage `R_FPA-R_SPA>=v tau_R` and an allocation gap `Delta_E>=min(tau_E,tau_W/(1-v))`. At low `v`, the allocation gap is too small; near one, the FPA revenue advantage weakens. Rates affect the crossings, so a universal scalar `v*(H)` is unsupported.

## 7. Small-game result

Exact `.25`-grid payoff matrices and deterministic mean-field Hedge updates were evaluated for 60 tiny cells. The sign conflict reappears in 59: FPA revenue is higher in 59 and SPA allocation is better in all 60. The counterexample `(v,H,c_H,c_L)=(.75,1600,1,2)` rejects universal revenue dominance. This supports the mechanism explanation but is not new confirmatory evidence.

## 8. Theory candidates

| Candidate | Status | Assumptions | Evidence | Literature overlap | Next proof step |
|---|---|---|---|---|---|
| Welfare-allocation identity | RESTRICTED-PROPOSITION | Persistent two-value, one-item model | Exact accounting | Elementary | Use only to simplify |
| Regret-only SPA revenue bound | COUNTEREXAMPLE FOUND | External regret only | Zero-regret `(1,0)` bid path has zero revenue | Runner-up obstruction known | Abandon |
| Universal FPA revenue dominance | COUNTEREXAMPLE FOUND | Tiny mean-field Hedge | One of 60 cells reverses | FPA guarantees require conditions | Restrict region |
| Finite-time conflict region | THEOREM-POSSIBLE | Explicit deterministic mean-field Hedge model | 59/60 tiny cells; 54/75 holdout cells | Joint region not located | Bound log-weight ratios and payoff gaps |
| Scalar `v*(H)` boundary | NOT TRACTABLE | Rate-independent monotonicity | Empirical premise absent | No exact match | Replace by multi-parameter sufficient region |

## 9. Strongest theorem target

Prove a **finite-time objective-conflict region for deterministic mean-field Hedge**: explicit sufficient conditions on `(v,H,c_H,c_L,epsilon)` under which

`R_FPA-R_SPA >= v tau_R`

and

`A_SPA-A_FPA >= min(tau_E,tau_W/(1-v))`.

The proof should use payoff-gradient and Hedge log-weight-ratio bounds, exhibit a nonempty region, and state its grid and initialization dependence.

## 10. Publication assessment

**4/10.** The empirical execution is unusually disciplined and the surface is robust, but current novelty is a recombination of known mechanisms and there is no theorem. A successful finite-time conflict-region proof could raise the assessment materially; another algorithm sweep without that proof would not.

## 11. Next gate

**PROVE THEORY BEFORE LEVEL 5**

## 12. Estimated computational need for next phase

The next phase should be proof-led: zero new stochastic seed runs and zero large simulations. Expected computational work is exact matrix algebra, symbolic inequalities, and at most 500--1,000 deterministic tiny-grid/interval checks. Estimated machine runtime is under 30 minutes; expected human/theory time is one to three focused days. Only after the theorem is proved or sharply falsified should any Level 5 experiment count be specified.
