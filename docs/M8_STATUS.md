# DELEGATION-PROOF MARKET DESIGN — M8 STATUS

## Executive verdict

**MAJOR ADVANCE**

The conflict survives when both bidders receive the intermediate bid `v/2`. A closed `4x3` rectangle is certified for `H=2,...,6`. An endogenous-history stability lemma and conditional transfer theorem are proved, but their general bound is too loose to establish R6 under uniform initialization.

## TH-M8-002: 4x3 theorem

With values `(1,v)`, high actions `{0,v/2,v,1}`, low actions `{0,v/2,v}`, fair ties, uniform weights, and deterministic full-information Hedge, suppose

`v in [.31,.35]`, `eta_H in [.85,1.15]`, `eta_L in [.06,.14]`.

For every integer `H=2,...,6`, average FPA revenue exceeds average SPA revenue, while SPA allocation and welfare exceed FPA. The minimum certified lower bounds are `.1726472483` for revenue and `.0166436423` for allocation at `H=6`.

The larger M7 rectangle `[.30,.36]x[.8,1.2]x[.05,.15]` certifies directly through `H=5`; its H=6 allocation enclosure is inconclusive.

## Recurrence

High ratios remain `(x,y,r)`. For the low bidder define `a=log(w_L(v)/w_L(v/2))` and `b=log(w_L(v/2)/w_L(0))`. Then high probabilities are proportional to `(1,e^r,e^(r+y),e^(r+y+x))` and low probabilities to `(1,e^b,e^(a+b))`. Each ratio increments by `eta` times the corresponding adjacent expected-utility difference. The implementation generates every payoff entry directly from allocation and payment rules, independently auditing the symbolic recurrence.

## Expansion comparison

At `(1/3,1,.1), H=2`, `(D_R,D_A)` equals:

- `3x2`: `(.3544147,.0433438)`;
- `4x2`: `(.2820985,.0307515)`;
- `4x3`: `(.2905256,.0373292)`.

The first expansion weakens both margins; adding the low intermediate action partially restores them. Degradation is therefore smooth but not monotone, and no collapse occurs.

## TH-M8-003: endogenous-history stability

Let `rho_t` and `tilde rho_t` be core-conditional policies in two coupled Hedge systems, `d_t=sum_i ||rho_i^t-tilde rho_i^t||_1`, and `e_t=sum_i epsilon_{i,t}` the total off-core mass. Auction utilities lie in `[0,1]`, so changing an opponent distribution changes every expected action utility by at most one half its L1 distance. Softmax is 1-Lipschitz from logit `L-infinity` to policy `L1`. With `bar_eta=max_i eta_i` and equal initial core logits,

`d_{t+1} <= bar_eta sum_{s<=t}(d_s+2e_s)`.

Discrete Gronwall yields

`d_t <= 2 bar_eta sum_{s<t}(1+bar_eta)^(t-1-s)e_s`.

For revenue or allocation, each bounded per-round outcome error is at most `(d_t+2e_t)/2`. Averaging supplies explicit `E_R(H)` and `E_A(H)`. Comparing two mechanisms adds their respective errors. Thus core conflict margins transfer whenever the sum of FPA and SPA error bounds is below the corresponding core margin.

This is a conditional transfer theorem. It is nonempty for sufficiently small off-core masses, but uniform initialization gives the new low action mass `1/3` initially, making the generic bound too loose for the actual 4x3 expansion. The direct interval theorem, not this bound, proves the 4x3 result.

## Classification and stop rule

- 4x3 result: **THEOREM / RECTANGLE**.
- Endogenous-history lemma: **PROVED**.
- Transfer: **CONDITIONAL TRANSFER ONLY**; R6 not proved.
- Full-grid relationship: **PARTIALLY BRIDGED**.
- Publication readiness: **8/10**.
- Next gate: **PROCEED TO CROSS-LEARNER VALIDATION**.

No further dedicated bridge-theory phase is recommended unless a sharper stability constant appears immediately.
