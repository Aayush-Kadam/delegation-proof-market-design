# M2.5 finite-horizon replication selection

Selection date: 2026-09-15. This memo was frozen before any M2.5 powered run. No candidate output was inspected.

## CANDIDATE PAPERS

1. Aggarwal, Gupta, Perlroth, and Velegkas, *Randomized Truthful Auctions with Learning Agents* (2024), Section 5 and Appendix F.
2. Cesa-Bianchi and Lugosi, *Prediction, Learning, and Games* (2006), Theorem 2.2 (exponentially weighted average/Hedge finite-time regret), instantiated in the repeated-auction environment studied by Kolumbus and Nisan and Aggarwal et al.

## CANDIDATE RESULTS

- Aggarwal et al. Proposition 5.1 / Proposition 5.2: approximately T^(3/4) auctioneer-regret upper/lower results for a constant truthful auction.
- Aggarwal et al. Theorem 5.3 / Corollary 5.6: approximately sqrt(T) auctioneer regret for a predetermined two-epoch schedule using a strictly IC auction and then SPA.
- Exponential-weights finite-time inequality: for K actions and reward vectors in [0,1]^K, the expected external regret of weights proportional to exp(eta times cumulative reward) is at most log(K)/eta + eta*T/8. At eta=sqrt(8 log(K)/T), this is sqrt(T log(K)/2).

## WHY EACH IS RELEVANT

The Aggarwal results are the closest market-design targets because they measure seller revenue against truthful SPA. The Hedge inequality is one layer more primitive but validates the exact bidder update, full counterfactual feedback, action grids, and mechanism-generated utilities used in every planned finite-horizon MWU experiment.

## IMPLEMENTABILITY

The constant-auction Aggarwal lower bound contains an unspecified positive discretization-dependent constant, so it does not furnish a numerical pass region. Its upper-bound construction requires choosing and implementing a strictly IC randomized auction and its incentive gap. The changing-auction construction additionally requires a source-faithful switching time involving mean-basedness parameters. Implementing these would add a new mechanism family and would test that new implementation at least as much as the existing simulator.

The Hedge inequality is directly implementable without changing simulator fundamentals. Utilities from no-overbid FPA and SPA lie in [0,1], the simulator already computes full counterfactual reward vectors, and its Hedge policy is exactly proportional to exponentiated cumulative rewards.

## SOURCE ASSUMPTIONS

For the selected result: a finite action set, uniform initial weights, fixed positive eta, full-information reward vectors bounded in an interval of width one, and sampling from the exponential-weights policy before updating on the current reward vector. Reward sequences may be arbitrary; the preregistered auction opponent sequence is deterministic and independent of the learner's current random draw.

## EXPECTED METRIC

External regret, both (a) exact expected regret obtained by propagating the Hedge distribution and (b) realized regret over independent learner seeds. The direct theoretical comparator is B(T,K,eta)=log(K)/eta+eta*T/8.

## WHY FINAL TARGET WAS SELECTED

It is an explicit finite-T inequality with known constants, tests components needed in Level 3, and does not require an unvalidated new auction. Both FPA and SPA are used so the same learner/feedback calculation is checked under two payment rules.

## WHY SELECTION DID NOT USE SIMULATION OUTCOMES

The source, configurations, deterministic opponent sequence, horizon grid, metrics, and decision rule were written here and in the protocol before execution. No M2.5 result existed at selection time.
