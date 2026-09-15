# R-REP-002 source mapping

## Source claim

Kolumbus and Nisan (2022), Theorem 2: in a repeated first-price auction between two mean-based regret-minimizing agents on a discrete epsilon grid, **if the dynamics converge to a single distribution**, the high-value bidder wins with probability approaching one and average price converges to the second value up to `O(epsilon)`. Their Hedge simulation with values `(1,.5)` is described as converging to this economic outcome.

## Mathematical object that converges

The paper defines `p_t^T` as the **cumulative empirical distribution of joint bid tuples** through time `t`. Convergence means this time-average distribution remains close to a fixed joint distribution for all sufficiently late fractions of a horizon sequence. The theorem is conditional on that convergence. It does not require adjacent-window marginal action histograms to have categorical L1 below a fixed finite-sample threshold, nor does it assert last-iterate policy convergence.

## Assumptions and learning rule

Fixed additive values; repeated single-item FPA; epsilon-grid bids; no overbidding; uniform tie-breaking; mean-based regret minimization. The displayed simulations include exponential multiplicative weights/Hedge. The update parameter is horizon-dependent and fixed within a run.

## Horizon/asymptotic status

Theorem 2 is asymptotic and conditional. The simulation is supporting finite-horizon evidence, not a quantitative convergence-rate theorem.

## What V1 measured

V1 compared two disjoint 5,000-draw **marginal empirical action histograms** using categorical L1 and required L1 at most `.10` plus mean drift at most `.02` in 80% of seeds.

## Source match verdict

V1's economic price and winner metrics match the theorem's predicted outcome. Its stability gate does **not** match the source convergence object: it uses adjacent-window marginal histograms rather than the cumulative empirical joint distribution, and its fixed threshold was not calibrated for multinomial sampling over 101/51 bins. V2 therefore treats economic outcome agreement as the source-matching criterion and reports exact-policy TV/Wasserstein and empirical L1 only as explicitly project-defined diagnostics.

