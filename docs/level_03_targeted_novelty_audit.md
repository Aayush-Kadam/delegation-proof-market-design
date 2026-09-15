# Level 3 targeted novelty audit

Audit date: 2026-09-15. Candidate frozen in commit `241577f` before this search. Classification: **SUBSTANTIAL OVERLAP**.

## Selected candidate

Finite-horizon revenue-efficiency conflict under asymmetric Hedge adaptation: FPA is closer to (and can exceed) the competitive revenue benchmark while SPA preserves allocation and welfare more strongly.

## Search vocabulary

Repeated auctions learning finite horizon; FPA SPA learning dynamics; valuation asymmetry/gap; horizon-dependent mechanism ranking; finite-time auction performance; no-regret auction revenue; MWU price/revenue; revenue-welfare tradeoff; robust mechanism performance.

## Closest work

- Kolumbus and Nisan (2022), *Auctions Between Regret-Minimizing Agents*, https://arxiv.org/abs/2110.11855. Directly studies persistent-value FPA/SPA with regret-minimizing agents and establishes the central revenue contrast. This makes “FPA revenue exceeds SPA revenue under Hedge” known background.
- Aggarwal et al. (2024), *Randomized Truthful Auctions with Learning Agents*, https://arxiv.org/abs/2411.09517. Explicitly attributes SPA revenue loss to the runner-up retaining mass below value and develops finite-horizon auctioneer regret. It also establishes learning-rate effects. Both ingredients of the candidate's mechanism are therefore known.
- Feng et al. (2020), *Convergence Analysis of No-Regret Bidding Algorithms in Repeated Auctions*, https://arxiv.org/abs/2009.06136. Studies mean-based convergence and efficiency-relevant equilibrium selection, but in stochastic-value settings unlike the persistent asymmetric environment here.
- Bichler, Gupta, and Oberlechner (2023), *Revenue in First- and Second-Price Display Advertising Auctions: Understanding Markets with Learning Agents*, https://arxiv.org/abs/2312.00243. Directly compares FPA/SPA revenue with learning agents, mostly in advertising/ROI and complete/incomplete-information models.
- Syrgkanis et al. (2015), *Fast Convergence of Regularized Learning in Games*, https://arxiv.org/abs/1507.00407. Gives finite-time welfare guarantees from regret in smooth games and compares learning dynamics, creating adjacent overlap for the welfare side.
- Hoy, Jain, and Wilkens (2013), *A Dynamic Axiomatic Approach to First-Price Auctions*, https://arxiv.org/abs/1304.7718. Gives dynamic conditions under which FPA revenue is at least SPA revenue, so broad revenue superiority is not new.

## Classification rationale

The exact prospectively measured object—a seed-paired, vector-valued finite-horizon conflict between normalized revenue loss and allocation/welfare loss across persistent valuation geometry and adaptation factors—was not found as a named theorem or matching phase map. That narrow packaging may be a useful computational characterization. However, its causal ingredients and broad direction are strongly anticipated by the cited literature: FPA can preserve revenue, SPA can shade the runner-up without losing the high-value allocation, and learning-rate variation matters.

Therefore the candidate is not a strong originality claim. It proceeds to falsification and holdout because it may still supply a precise robustness region, but even perfect survival can support at most a **PROMISING PHENOMENON** or **MIXED** Level 3 verdict absent a sharper non-implied boundary.

## Status by category

- **Known:** FPA/SPA differ under regret-minimizing bidders; SPA runner-up shading reduces revenue; learning rates affect behavior.
- **Overlapping:** learning-agent FPA/SPA revenue comparisons, finite-time auctioneer regret, and no-regret welfare guarantees.
- **Potentially new:** a prospectively frozen vector-valued finite-horizon robustness surface showing when a revenue advantage is purchased with measurable allocation/welfare loss.
- **Uncertain:** whether an equivalent objective-conflict surface appears in unpublished or differently termed computational work.
