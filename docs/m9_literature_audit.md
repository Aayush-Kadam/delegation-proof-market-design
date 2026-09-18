# M9 targeted literature audit

## Scope

This audit was completed before any `M_alpha` outcomes were generated. It targets hybrid first-/second-price payments and auction design for adaptive or no-regret bidders.

## Findings

The rule in which the winner pays a convex combination of its own bid and the second-highest bid is not new. Syrgkanis's thesis explicitly discusses a hybrid auction with this payment and establishes smoothness-style welfare results. Earlier work also uses the term *hybrid auction* for mechanisms combining first- and second-price elements, although not always with the same single-stage convex-combination rule.

Learning-agent auction design is also an established area. Kolumbus and Nisan compare first- and second-price auctions populated by regret-minimizing agents. Feng et al. study convergence of mean-based learning in repeated auctions. Braverman et al. study revenue design against no-regret buyers, and Aggarwal et al. show that randomized auction design can improve guarantees with learning agents.

## Source map

- Vasilis Syrgkanis, *Efficiency of Mechanisms in Complex Markets*: explicitly identifies a hybrid auction in which the winner pays a convex combination of its own and the second-highest bid. https://www.vsyrgkanis.com/thesis.pdf
- Kolumbus and Nisan, *Auctions Between Regret-Minimizing Agents*: first-/second-price comparison with delegated no-regret bidding. https://arxiv.org/abs/2110.11855
- Feng et al., *Convergence Analysis of No-Regret Bidding Algorithms in Repeated Auctions*: convergence behavior in repeated FPA/SPA. https://arxiv.org/abs/2009.06136
- Braverman et al., *Selling to a No-Regret Buyer*: mechanism design can differ materially when the buyer learns. https://arxiv.org/abs/1711.09176
- Aggarwal et al., *Randomized Truthful Auctions with Learning Agents*: auction design expressly optimized for learning agents. https://arxiv.org/abs/2411.09517
- Balseiro et al., *Robust Repeated Auctions under Heterogeneous Buyer Behavior*: robust auction design under heterogeneous behavior. https://arxiv.org/abs/1803.00494

## Novelty classification before M9 outcomes

- Convex-combination payment family: **KNOWN**.
- General mechanism design for learning agents: **KNOWN**.
- Minimax multi-objective selection of an interpolation rule across homogeneous and ordered heterogeneous adaptive learners, with a prospectively frozen development/holdout design: **POSSIBLY DISTINCT APPLICATION**.

No priority claim is made without a broader systematic review. M9 tests a delegation-robust selection/design contribution, not invention of the payment family.
