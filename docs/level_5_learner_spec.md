# Level 5 learner specification

All learners receive the same full counterfactual reward vector after every round and use the frozen no-overbid `.01` grids.

## Hedge control

`p_t(a) proportional to exp(eta U_{t-1}(a))`, with `eta_i=c_i sqrt(log K_i/H)`. Actions are sampled from `p_t`. This is the existing Level-3 implementation and has the standard `O(sqrt(T log K))` external-regret guarantee.

## FTPL

At initialization draw independent exponential perturbations `Z_a` with mean `1/eta`. At round `t`, choose uniformly among maximizers of `U_{t-1}(a)+Z_a`. The perturbation is fixed for the run, all action rewards are observed, and ties are uniform. This is classical full-information Follow-the-Perturbed-Leader: cumulative reward plus a random perturbation, with `O(sqrt(T log K))`-scale regret under the calibrated perturbation magnitude. It is deliberately not Gumbel FTPL, which would reproduce exponential weights exactly.

## External regret matching

Let `R_t(a)=U_{t-1}(a)-sum_{s<t}u_s(a_s)`. At round `t`, sample proportionally to `max(R_t(a),0)`; use the uniform distribution if every positive regret is zero. This is unconditional/external regret matching, a canonical positive-regret-driven full-information dynamic closely related to Hart–Mas-Colell regret matching. Multiplying rewards by a positive rate does not change this policy, so inherited `(c_H,c_L)` labels are retained for design comparability but do not tune regret matching.

Sources: Kalai–Vempala/classical FTPL as summarized by Suggala–Netrapalli (2020); Hart–Mas-Colell (2000) for regret matching; existing repository validation for Hedge.
