# Novelty audit

## Verdict

**No novelty claim is currently justified.** “Delegation robustness” is useful working language, but the underlying principal-to-learning-agent distinction substantially overlaps Kolumbus–Nisan. Learning-rate effects and randomized mechanisms for learning agents substantially overlap Aggarwal et al. (2024). Intermediate payment formats also occur in autobidding work.

## What is established or already close

1. Repeated auctions between regret-minimizing agents and strategic value reports to those agents.
2. Mean-based learner convergence in fixed-value first-price auctions.
3. Welfare guarantees under no-regret play in smooth mechanisms/games.
4. Autobidding under budget and return-on-investment constraints.
5. Revenue advantages of randomized truthful auctions with learning bidders and qualitative learning-rate-ratio effects.
6. LLM behavior in auction experiments.

## Potentially open contribution targets

- A precisely quantified worst-case robustness functional jointly indexed by mechanism, learner class, feedback regime, and perturbation set, if it is not equivalent to existing learning-robustness or auctioneer-regret notions.
- Frozen-holdout evidence that a mechanism selected on simple learners generalizes to disjoint learner families without sacrificing classical desiderata.
- A finite-horizon bound tying observable learner diagnostics to economic delegation gaps.
- A sharp impossibility/tradeoff involving incentive compatibility, information disclosure, and robustness across a declared algorithm class.

Each is a research question, not a contribution.

## Required next audit

Backward/forward citation tracing for the seven core papers; searches in EC, WINE, SODA/STOC/FOCS, NeurIPS/ICML, Management Science, RAND, Theoretical Economics, and ad-auction venues; and direct theorem comparison before naming any result.

