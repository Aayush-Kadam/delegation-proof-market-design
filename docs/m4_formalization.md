# M4 formalization and mechanism analysis

## Formal environment

Let bidders `i in {H,L}` have persistent values `v_H=1` and `v_L=v in (0,1)`. Bid sets are finite no-overbid grids `B_i={0,epsilon,...,v_i}`. In each round `t<=H`, each bidder independently samples from a Hedge distribution `p_i^t`; uniform ties are resolved independently. Full-information counterfactual payoffs update log weights with fixed rate `eta_i=c_i sqrt(log |B_i|/H)`.

For mechanism `M in {FPA,SPA}`, let `R_M(H,z)`, `W_M(H,z)`, and `A_M(H,z)` denote trajectory-expected average seller revenue, welfare, and probability that the high-value bidder wins, where `z=(v,c_H,c_L,epsilon)`. Define

`DL_R(M,H,z)=v-R_M(H,z)`, `NDL_R=DL_R/v`,

`DL_E(M,H,z)=1-A_M(H,z)`, and `DL_W(M,H,z)=1-W_M(H,z)`.

Mechanism contrasts are

`Delta_R=NDL_R(FPA)-NDL_R(SPA)`,

`Delta_E=DL_E(FPA)-DL_E(SPA)`, and `Delta_W=DL_W(FPA)-DL_W(SPA)`.

The sign-conflict region is

`C_sign={ (H,z): Delta_R<0 and Delta_E>0 }`.

The frozen economically meaningful region is

`C_tau={ (H,z): Delta_R<=-tau_R and CI_R^upper<0 and [(Delta_E>=tau_E and CI_E^lower>0) or (Delta_W>=tau_W and CI_W^lower>0)] }`,

with `(tau_R,tau_E,tau_W)=(.05,.01,.005)`.

## Exact accounting propositions

For two persistent values with one item allocated every round,

`W_M = v + (1-v) A_M`.

Therefore

`DL_W(M)=(1-v)DL_E(M)` and `Delta_W=(1-v)Delta_E`.

Thus allocation and welfare are not independent objectives in this model. The frozen union gate can be rewritten as an allocation-loss condition

`Delta_E >= min(tau_E, tau_W/(1-v))`,

plus the respective confidence requirement. This effective allocation floor is approximately `.00556,.00714,.01,.01,.01` at holdout values `.1,.3,.5,.7,.9`.

Let `S_M` be total bidder surplus. Since `W_M=R_M+S_M`,

`S_FPA-S_SPA = v Delta_R - Delta_W`.

Hence every cell with the frozen conflict signs (`Delta_R<0`, `Delta_W>0`) necessarily has lower total bidder surplus under FPA. This observed 74/75 pattern is mostly an accounting consequence, not a separate novelty claim.

## Exact tiny game

The M4 exact game uses `B_H={0,.25,.5,.75,1}` and `B_L={0,.25,...,v}` for `v in {.25,.5,.75}`. For bid pair `(b_H,b_L)`, let `q_H` equal `1`, `1/2`, or `0` according as `b_H` is greater than, equal to, or less than `b_L`.

In FPA,

`u_H=q_H(1-b_H)`, `u_L=(1-q_H)(v-b_L)`, and `R=q_H b_H+(1-q_H)b_L`.

In SPA,

`u_H=q_H(1-b_L)`, `u_L=(1-q_H)(v-b_H)`, and `R=min(b_H,b_L)`.

`results/m4/small_game/payoff_matrices.json` contains the exact rational matrices. The deterministic mean-field Hedge calculation replaces sampled opponent actions by their exact mixed distribution at every update. Across three values, four horizons `{25,100,400,1600}`, and five rate pairs, it produces 60 cells: FPA revenue is higher in 59, SPA allocation is better in all 60, and the sign conflict appears in 59. The sole counterexample is `(v,H,c_H,c_L)=(.75,1600,1,2)`, where SPA revenue is also higher. This is explanatory evidence only; it is not independent confirmation and proves that an unconditional sign theorem is false.

## Economic mechanism

In SPA, raising one's bid while remaining below value can improve allocation without raising the winner's own payment. Truthful bidding is therefore weakly dominant, and the high bidder rapidly removes low bids that risk losing. But the low bidder's payoff gradients can be weak when the high bidder already bids above it: many low bids all lose and all earn zero. Finite-time Hedge can consequently preserve substantial runner-up mass below `v`, depressing the price while keeping allocation nearly efficient.

In FPA, a winner pays its own bid. The high bidder trades off win probability against payment, while the low bidder's support creates direct competitive pressure. The two distributions can place winning high-bid mass near the low value, raising revenue, yet simultaneous experimentation causes more low-bidder wins than in SPA. The seller captures revenue at the expense of the high bidder and, in conflict cells, total bidder surplus.

## Why the conflict is interior

The frozen conflict requires two different gaps:

1. Dollar revenue advantage `R_FPA-R_SPA >= v tau_R`.
2. Allocation disadvantage `Delta_E >= min(tau_E,tau_W/(1-v))`.

At small `v`, FPA's normalized revenue advantage can be enormous, but both mechanisms usually allocate efficiently enough that the allocation/welfare floor fails. Near `v=1`, misallocation is common and the allocation floor is easy, but FPA's revenue advantage weakens or can reverse for some rate/horizon cells. Intermediate values satisfy both. This two-constraint explanation matches the 1/15, 15/15, 15/15, 15/15, 8/15 holdout support pattern.

There is no evidence for a single scalar boundary `v*(H)`: rate factors change the crossing, and the preregistered horizon-reversal rule did not fire. A defensible theoretical object is a multi-parameter boundary defined by the two inequalities above, not a fitted curve.

## Regret-to-market-outcome assessment

Generic smoothness already bounds welfare using bidder regret. It does not give the sharp FPA-versus-SPA difference in `Delta_E`, and revenue is not social welfare.

No seller-revenue bound that vanishes solely with external regret can hold for SPA. Consider persistent values `(1,v)`, the high bidder always bidding `1`, and the low bidder always bidding `0`. The high bidder wins, pays zero, and obtains utility one; the low bidder obtains zero and cannot profitably deviate because every no-overbid action loses to bid `1`. Both external regrets are zero while seller revenue is zero and `DL_R=v`. Kolumbus--Nisan and Aggarwal et al. establish the broader runner-up obstruction. Any useful revenue theorem must add equilibrium selection, mean-based path conditions, swap regret, exploration, or direct policy-mass assumptions.

For FPA, Ipsen--Skoulakis (2026) now gives finite-time revenue control under approximate correlated equilibrium/no-swap regret. Since Level 3 Hedge guarantees external rather than swap regret, a mechanism-specific Hedge path theorem remains logically distinct but narrower than originally believed.
