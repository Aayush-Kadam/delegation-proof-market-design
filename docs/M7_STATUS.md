# DELEGATION-PROOF MARKET DESIGN — M7 STATUS

## Executive verdict

**MAJOR BRIDGE ADVANCE**

The conflict survives a genuine additional strategic action. A closed `4x2` rectangle is proved for six consecutive horizons, and a general fixed-payoff-sequence action-expansion lemma is established.

## TH-M7-003: richer-grid conflict theorem

Let values be `(1,v)`, high actions `{0,v/2,v,1}`, low actions `{0,v}`, fair ties, uniform action weights, and deterministic full-information Hedge. If

`v in [.30,.36]`, `eta_H in [.8,1.2]`, `eta_L in [.05,.15]`,

then for every integer `H=2,...,6`, average FPA revenue is strictly higher than SPA revenue, while SPA allocation and welfare are strictly higher than FPA allocation and welfare.

Across the entire rectangle, the smallest certified margins over the covered horizons are `0.1531588670` for revenue and `0.00840680569` for allocation, both attained in the aggregate certificate at `H=6`.

## Exact 4x2 recurrence

Let `x=log(w_1/w_v)`, `y=log(w_v/w_h)`, `r=log(w_h/w_0)`, `z=log(w_L(v)/w_L(0))`, where `h=v/2`. Then

`q proportional to (1,e^r,e^(r+y),e^(r+y+x))`, `p=e^z/(1+e^z)`.

High-bidder utilities are:

- FPA: `u(0)=(1-p)/2`, `u(h)=(1-p)(1-v/2)`, `u(v)=(1-v)(1-p/2)`, `u(1)=0`.
- SPA: `u(0)=(1-p)/2`, `u(h)=1-p`, `u(v)=1-p(1+v)/2`, `u(1)=1-vp`.

The high ratios update by adjacent utility gaps. The low ratio obeys

- FPA: `z'=z-eta_L v q_0/2`;
- SPA: `z'=z+eta_L v(q_0+q_h)/2`.

Thus the added action preserves—and strengthens the low bidder's opposing mechanism-specific drift.

## Uniform-initialization effect and comparison with M6

Round-one high action mass changes from `1/3` to `1/4`. At the shared witness `(1/3,1,.1)`, adding `v/2` weakens both margins but never reverses them through `H=9`. At `H=2`, revenue falls from `.3544147` to `.2820985` and allocation from `.0433438` to `.0307515`. At `H=6`, the reductions are approximately `.05961` and `.03543`.

The result is therefore not invariant to action expansion, but it is not knife-edge either.

## TH-M7-004: action-expansion lemma

For Hedge facing a fixed payoff sequence, add actions `a` to a core set with equal initial weights. If each added action has a core witness `b(a)` satisfying cumulative gap `U_t(b(a))-U_t(a)>=G_a(t)`, then

`w_t(a)/w_t(b(a)) <= exp(-eta G_a(t))`

and total off-core mass is at most `sum_a exp(-eta G_a(t))`. Conditional on selecting a core action, expanded Hedge has exactly the core Hedge distribution when the core cumulative payoffs are unchanged. Hence any `[0,1]` outcome statistic changes by at most the off-core mass.

This lemma is exact for a common fixed payoff history. In an endogenous multi-agent auction, expansion changes opponents' play and therefore core payoff histories; a transfer theorem additionally needs a stability/coupling bound. That step is not proved.

## Certification and limits

The full continuum rectangle was partitioned into 480 subboxes and propagated with outward-rounded 70-digit Decimal intervals. Horizons 2–6 certify. The enclosure crosses zero for allocation at H=7; deterministic reconnaissance remains positive through H=9, so H=7 is inconclusive rather than a counterexample.

No `4x3` theorem or full `.01`-grid transfer is claimed. Universal rankings remain rejected by the earlier counterexamples.

## Classification

- Theory ladder: **R5** because both an R3 richer-grid theorem and a qualified general action-expansion lemma are proved.
- Full-grid relevance: materially improved but incomplete; endogenous-history stability remains the missing link.
- Novelty: **POSSIBLY DISTINCT**.
- Publication readiness: **7/10**.
- Next gate: **STRENGTHEN RICHER-GRID THEORY**.
