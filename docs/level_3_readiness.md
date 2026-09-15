# Level 3 readiness

## Decision

M2.5 finite-horizon simulator validation is **CERTIFIED**. Historical Level 2 remains **MIXED**. Level 3 may be preregistered separately; none was executed during M2.5.

## VALIDATED DOMAIN

- Repeated two-bidder single-item FPA and SPA.
- Persistent values in [0,1] and discrete no-overbid action grids through 101 actions.
- Full-information Hedge/MWU with uniform initialization.
- Uniform tie-breaking and expected counterfactual utilities.
- Finite horizons through 200,000 rounds per run.
- Revenue, payments, allocations, utility, regret, price, and win-share accounting.

## NOT VALIDATED

- Asymptotic last-iterate truthfulness or finite-T TV bounds for Theorem D.4.
- Deep RL, LLM bidders, and confirmatory Q-learning conclusions.
- Partial/bandit feedback, continuous bids, large populations, changing values, and endogenous composition.
- External replication of randomized strictly IC, reserve, hybrid, or all-pay mechanism families.

## Required Level 3 discipline

Freeze one primary question, estimand, learner/feedback family, mechanism set, horizon, power, correction rule, and holdout before discovery. The recommended campaign is finite-horizon mechanism ranking by worst-case degradation across the frozen family. Keep principal misreporting as a benchmark rather than the contribution.
