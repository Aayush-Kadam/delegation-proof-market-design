# M4 contribution positioning

## What prior literature knows

Prior work already shows that regret-minimizing agents can make FPA and SPA behave differently; that discrete FPA under appropriate mean-based/equilibrium-selection conditions earns revenue near the second value; that deterministic truthful auctions can retain runner-up underbidding and seller-revenue loss; that relative learning rates matter; and that no-regret/smoothness controls welfare. A 2026 result additionally gives polynomial finite-time FPA revenue guarantees under approximate correlated equilibrium/no-swap regret.

## What Level 3 demonstrated

Under a prospectively frozen persistent-value, full-information Hedge design, FPA has lower normalized revenue loss in 72/75 independent holdout cells, while SPA has lower allocation and welfare loss in all 75. The preregistered joint directional/economic/significance gate passes in 54 cells and all eight falsification attacks pass. The high bidder's surplus is lower under FPA in all 75 cells; total bidder surplus is lower in 74.

## What remains potentially new

The defensible novelty residual is the **joint finite-horizon robustness surface**: a prospectively validated map of when seller-revenue and allocation/welfare rankings point to different auction formats, including a broad interior valuation-gap region and explicit rate/horizon modulation. No matching theorem or equivalent prospectively thresholded phase map was located.

This is not yet enough for a strong paper claim. The surface combines mechanisms that prior papers largely predict, and its apparent valuation boundary partly reflects declared economic thresholds.

## What must still be proved

The strongest path is a finite-time theorem for deterministic mean-field Hedge that certifies a nonempty parameter region where FPA's revenue advantage and SPA's allocation advantage hold simultaneously. The proof must expose payoff-gradient/log-weight mechanisms and cannot merely fit the completed data. External regret alone cannot produce the needed SPA revenue bound.

## What must still be externally validated

Only after a theory residual survives should Level 5 test whether its predicted region transfers across algorithms or feedback regimes. Cross-algorithm validation before that proof would establish generality of a phenomenon whose intellectual distinctness remains uncertain.

## Skeptical referee test

### Referee A: “Is this just Kolumbus–Nisan with a larger grid?”

**Current answer:** partly. The FPA revenue mechanism and persistent-value regret-minimizer laboratory are directly inherited. What is added is independent prospective evidence for a joint, objective-specific finite-horizon region with uncertainty and fixed economic floors. Without a theorem for that joint region, “larger and better controlled map” remains a fair criticism.

### Referee B: “Is the objective conflict obvious once known FPA/SPA learning behavior is combined?”

**Current answer:** the sign intuition is close to obvious after the fact: FPA converts own bids into seller revenue; SPA encourages efficient high bidding while the runner-up can remain shaded. The non-obvious part is the size and breadth of the simultaneous region, not its qualitative possibility. A proof that identifies when both economic floors hold would materially strengthen the answer.

### Referee C: “Does the paper contribute a theorem or merely a computational surface?”

**Current answer:** currently a rigorously preregistered computational surface, not a theorem. The exact accounting identities and zero-regret counterexample are useful but not novel. Publication value depends on proving the finite-time conflict-region target.

## Positioning sentence

Do not claim discovery of FPA revenue superiority or SPA learning inefficiency. If the theorem target succeeds, position the work as a finite-time, objective-specific mechanism-selection result: known learning dynamics imply different preferred auction formats for seller revenue and allocative performance over an explicitly characterized persistent-value region.
