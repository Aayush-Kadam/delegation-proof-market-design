# M11 constant-hybrid design limitation proof

## Model and mechanism class

Two persistent-value bidders have values `(1,v)`, high-bid actions `{0,v/2,v,1}`, and low-bid actions `{0,v/2,v}`. Ties are fair, initial weights are uniform, and both players use deterministic full-information mean-field Hedge. For M11's witness, `v=1/3`, `eta_H=4`, `eta_L=0`, and the finite horizon is `H=9`.

The covered mechanism class is C0:

`p_alpha=b_(2)+alpha*(b_(1)-b_(2)), alpha in [0,1]`,

with highest-bid allocation and existing tie rules. Let `R(alpha)` and `A(alpha)` denote nine-round average seller revenue and high-value-bidder allocation.

## Exact payoff construction

For every action pair, let `q_H` be high-bidder win probability (`0,1/2,1`). The payment is affine in alpha. Utilities are

`u_H=q_H*(1-p_alpha)` and `u_L=(1-q_H)*(v-p_alpha)`.

Expected utilities under current mixed policies update log weights by `ell_i^{t+1}(b)=ell_i^t(b)+eta_i E[u_i^t(b)]`. Softmax reconstructs the next policies. `src/delegation_market/m11_theory.py` implements these identities directly from the auction rules.

## Theorem: finite-horizon constant-hybrid incompatibility

For the witness above, throughout `alpha in [0,1]`:

1. `R'(alpha)>0`;
2. `A'(alpha)<0`.

Define half-endpoint safety levels

`R_half=(R(0)+R(1))/2` and `A_half=(A(0)+A(1))/2`.

Then no constant alpha satisfies both `R(alpha)>=R_half` and `A(alpha)>=A_half`.

## Certified quantitative bounds

The outward-rounded certificate gives:

- `R'(alpha) in [0.0214157305,0.6787484144]` globally;
- `A'(alpha) in [-0.5127730196,-0.0426592879]` globally;
- `R(0)=0.1587002873`, `R(1)=0.3348830147`, hence `R_half=0.2467916510`;
- `A(0)=0.9230171939`, `A(1)=0.7659477166`, hence `A_half=0.8444824553`;
- `R(.36)<R_half<R(.37)`;
- `A(.21)>A_half>A(.22)`.

By strict revenue monotonicity, revenue safety implies `alpha>.36`. By strict allocation monotonicity, allocation safety implies `alpha<.22`. Since `.36>.22`, the requirements are incompatible.

## Certification method

`src/delegation_market/m11_interval.py` uses 70-digit Decimal outward arithmetic and interval automatic differentiation. It exhaustively partitions `[0,1]` into 10,000 alpha subintervals and propagates value and derivative intervals through payoff construction, Hedge updates, softmax, revenue, and allocation. All six certificate checks close strictly. The certificate is `results/m11/constant_alpha_certificate.json`.

The 10,000 objects are interval subboxes for a single fixed witness, not additional stochastic or environment configurations.

## Scope and counterexamples

This is an existence/incompatibility theorem for one explicit finite-horizon delegated-learning environment and midpoint safety definition. It is not universal across parameters. A 1,500-configuration deterministic audit found 109 cases where at least one sampled monotonicity condition fails. For example, at `(v,eta_H,eta_L,H)=(.1,2,0,9)`, revenue is nonmonotone in alpha even though allocation remains decreasing.

The theorem does not use the empirical `.25/.10` M9/M10 thresholds. Its midpoint safety conditions are primitive objective guarantees. M9 supplies separate prospective evidence that analogous worst-case conflict appears across a broad computational family.

## Gap-only status

At uniform initialization, reduced-model normalized-gap distributions for `v=.1` and `v=.9` have overlap coefficient `5/6`, total variation `1/6`, and Wasserstein-1 distance `.1`; many exact gap values are shared. Thus gap alone is a lossy regime signal. However, this does not prove an L2 theorem because future gaps and policies respond endogenously to the payment rule. M11 therefore leaves gap-only impossibility as a conjecture/partial formalization.
