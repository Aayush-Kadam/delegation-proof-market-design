# M9 delegation-robust mechanism protocol

## Frozen scientific question

Can an interior member of

`p_alpha = alpha * b_(1) + (1-alpha) * b_(2)`

reduce worst-case revenue/allocation regret relative to selecting FPA or SPA, across the validated environment family and nine homogeneous/ordered-heterogeneous learner profiles?

## Mechanisms and populations

- Coarse development alphas: `0.0, 0.1, ..., 1.0`.
- `alpha=0` is SPA and `alpha=1` is FPA; allocation and fair tie-breaking are unchanged.
- Profiles: `H/H`, `F/F`, `R/R`, `H/F`, `F/H`, `H/R`, `R/H`, `F/R`, `R/F`.
- Bid grids, full-information feedback, learning-rate construction, valuations, and horizon definitions are unchanged from Level 5/heterogeneous validation.

## Parameter-only split

The 25 frozen environments are numbered in their existing manifest order, `E00` through `E24`. No `M_alpha` outcome was used.

- Development (15): `E01,E03,E04,E05,E07,E08,E10,E11,E13,E16,E17,E19,E20,E21,E22`.
- Holdout (10): `E00,E02,E06,E09,E12,E14,E15,E18,E23,E24`.

Both partitions include every valuation level and short/medium/long horizons. The holdout includes `v_L=.7,.9`; every learner profile, including H/R and F/R, is evaluated in both partitions. Previously identified reversal cells are designated stress cases, not removed; their corresponding parameter environments are represented in the holdout by `E18,E23,E24` and in development by `E16,E17,E19,E20,E21,E22`.

## Seeds and compute stages

- Development seeds: `7000,...,7004`, paired across all alphas.
- Holdout seeds: `8000,...,8029`, untouched until candidate freeze and paired across `SPA,FPA,M_alpha*`.
- Four workers are the initial benchmark configuration. Worker count is engineering-only.

## Frozen objectives

For cell `c=(profile,environment)`, let the endpoint-best value for objective `j` be `B_j(c)=max(Y_j(alpha=0,c),Y_j(alpha=1,c))`.

- Revenue regret: `q_R(alpha,c)=(B_R(c)-R(alpha,c))/max(v_L,0.1)`.
- Allocation regret: `q_A(alpha,c)=B_A(c)-A(alpha,c)`.
- Welfare is reported independently and not folded into candidate selection because allocation and welfare are algebraically linked in the persistent two-value setting.
- Bidder surplus is reported separately.
- Cell loss: `q(alpha,c)=max(q_R(alpha,c),q_A(alpha,c))`.

For every alpha report mean, median, 90th/95th percentiles, worst case, and upper-tail CVaR at 90% for `q_R,q_A,q`.

## Frozen candidate rule

An alpha is eligible only if:

- worst-case normalized revenue regret `<=0.25`;
- worst-case allocation regret `<=0.10`.

Among eligible alphas select lexicographically by:

1. smallest worst-case `q`;
2. smallest CVaR90 `q`;
3. smallest 95th-percentile `q`;
4. smallest mean `q`;
5. closest alpha to `0.5`;
6. smaller alpha.

If no alpha is eligible, no candidate is frozen and M9 is D0/TRADEOFF FRONTIER ONLY. Local refinement occurs only when the winning coarse alpha is interior and one of its adjacent coarse alphas is within 10% of its worst-case loss. Refinement is restricted to the closed interval between those neighboring coarse points in increments of `0.025`, with the identical rule.

## Holdout and success ladder

After development, freeze `alpha*`, its exact implementation/config hashes, development metrics, and this selection rule in a candidate commit. Then evaluate only `alpha=0,alpha*,1` on holdout.

- D0: no eligible interior candidate or no improvement.
- D1: interior candidate improves mean loss only.
- D2: interior candidate has strictly lower holdout worst-case and CVaR90 joint loss than both endpoints, with neither objective's worst-case regret worse than both endpoints.
- D3: under tolerance `0.005` in normalized revenue and `0.005` in allocation, candidate weakly dominates one endpoint in every holdout cell and strictly improves at least 25% of cells in one objective.
- D4 additionally requires bounded red-team survival and a defensible analytic proposition.

## Role robustness

For unordered pair `{X,Y}`, role sensitivity is the absolute difference between ordered profiles in the same environment and seed aggregate: `S_R=|R(X/Y)-R(Y/X)|`, and analogously for allocation. Compare medians and 95th percentiles for SPA, FPA, and the candidate. No role-robustness claim is made unless the candidate improves both median or both tail sensitivities without worsening the counterpart by more than `0.005`.

## Red-team rule

Only after a D2-or-higher holdout result, freeze a bounded addendum using independent seeds, H/R and F/R, high valuations, weakest holdout cells, nearby learning-rate multipliers, and one horizon perturbation. No addendum is chosen or run for D0/D1.

## Sealing

Development output is analyzed only after development completeness. Holdout is not generated until `alpha*` is committed. Holdout is analyzed only after its completeness check. Every run has a deterministic ID and atomic durable record; resume skips valid IDs.
