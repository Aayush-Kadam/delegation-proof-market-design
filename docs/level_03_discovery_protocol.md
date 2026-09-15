# Frozen Level 3 finite-horizon mechanism-ranking protocol

Freeze date: 2026-09-15. This protocol precedes all powered Level 3 outcomes. Historical Level 2 remains MIXED; M2.5 finite-horizon validation remains CERTIFIED.

## RESEARCH QUESTION

Does the finite-horizon economic ranking of first-price and second-price auctions under adaptive delegation vary systematically with valuation geometry, horizon, or prospectively fixed Hedge adaptation speeds? Can any ranking reversal, objective conflict, robustness conflict, or sharp boundary survive independent falsification and holdout?

## CERTIFIED DOMAIN

Two bidders, persistent values in [0,1], FPA/SPA, uniform ties, no-overbid discrete grids, full-information Hedge/MWU, and horizons no greater than 200,000. No unsupported learner or mechanism supplies evidence.

## MECHANISMS

First-price and second-price auctions, paired by seed and environment, with no reserve.

## VALUATIONS

v_H=1. Development v_L={.2,.4,.6,.8}; unopened holdout v_L={.1,.3,.5,.7,.9}. Values are exact grid points.

## HORIZONS

Development H={10,000;50,000;200,000}. Unopened holdout H={5,000;25,000;100,000}. No horizon is described as asymptotic.

## LEARNING RATES

eta_i=c_i sqrt(log(K_i)/H), fixed within a run. Rate-factor pairs (c_H,c_L) are {(1,1),(.5,1),(1,.5),(1,2),(2,1)}. The homogeneous pair is primary; asymmetric pairs are a prespecified environmental dimension, not a novelty claim.

## BID GRID

B_i={0,.01,...,v_i}. Each bidder therefore has a valuation-dependent no-overbid action count. The construction is identical across mechanisms.

## ECONOMIC REFERENCES

For v_H>v_L on this grid, truthful SPA yields price v_L and efficient high-bidder allocation. A discrete complete-information FPA equilibrium supporting the competitive price v_L has low bid v_L-.01 and high bid v_L: the low bidder cannot gain by winning above value and the high bidder does not prefer the uniform tie at v_L-.01 for any registered value. Hence R*=v_L, AE*=1, W*=1 for both mechanisms. This selects the minimum competitive equilibrium price rather than claiming uniqueness of the complete-information FPA equilibrium.

## SEEDS

Development uses 30 independent seeds 0–29 per condition; FPA/SPA share seed streams. Holdout uses independent seeds 2000–2029. Falsification uses 50 independent seeds 1000–1049. Seeds, not rounds, are replication units.

## PRIMARY METRICS

Full-horizon and final-10% seller revenue; DL_R=v_L-R and NDL_R=(v_L-R)/v_L. Mechanism contrast Delta_R=DL_R(FPA)-DL_R(SPA), so negative favors FPA revenue robustness and positive favors SPA. Paired seed mean and t-based 95% CI are primary.

## SECONDARY METRICS

DL_AE=1-Pr(high wins); DL_W=1-W; high and low bidder surplus; total bidder surplus; external regret per round; terminal expected bids, entropy, truthful mass, and final-window policy drift. Full-horizon and tail metrics are always reported together.

## HYPOTHESES

- H3.1: revenue delegation loss differs between mechanisms in meaningful regions.
- H3.2: Delta_R has opposite, economically meaningful signs in at least two environments.
- H3.3: Delta_R reverses meaningfully across horizons within a valuation/rate pair.
- H3.4: revenue and AE or welfare mechanism rankings disagree meaningfully.
- H3.5: rankings by mean and worst-case normalized revenue loss differ.

## MINIMUM ECONOMIC EFFECT

tau_R=.05 in normalized revenue-loss difference (five percent of the competitive revenue benchmark), tau_AE=.01 in high-winner probability, and tau_W=.005 in welfare per round. Prior 30-seed price confidence widths were far below one percentage point, so these floors target economic rather than merely statistical magnitude.

## CANDIDATE-DETECTION RULES

C1 valuation reversal and C2 horizon reversal require paired mean Delta_R/v_L on both sides of zero, absolute magnitude at least tau_R on each side, and paired 95% CIs excluding zero. C3 requires a meaningful revenue ranking and oppositely directed meaningful AE or welfare ranking with paired CIs excluding zero. C4 requires opposite mechanism orderings for mean versus worst-case NDL_R, with at least tau_R separation. C5 requires adjacent ordered valuation cells bracketing zero with at least tau_R magnitude and CIs excluding zero. Automatic rules operate only on the frozen development grid.

## DEVELOPMENT SET

Exactly `configs/level_03/development/grid.json`. All cells run before candidate selection. Outputs remain labeled exploratory.

## HOLDOUT SET

Exactly `configs/level_03/holdout/grid.json`, hashed before development. It must not be executed or inspected until primary-candidate selection, targeted literature review, and falsification are committed. The full frozen grid is evaluated without tuning.

## INITIAL CANDIDATE RANKING

Automatically detected candidate classes are scored /10 on economic magnitude, statistical robustness, pre-audit novelty potential, theory tractability, holdout testability, and policy relevance. Highest total wins; ties prefer the more specific falsifiable statement, then C1>C2>C3>C4>C5. If no automatic candidate fires, the campaign records no primary phenomenon and does not open holdout.

## FALSIFICATION RULES

The frozen primary candidate is attacked with 50 new seeds, step .005, a valuation perturbation of .025 toward the interior, rate factors multiplied jointly by .8 and 1.25, final-window shares .05 and .20, and a doubled horizon only when it remains <=200,000 (otherwise 200,000 is the certified cap). Direction must survive every applicable test and magnitude must remain at least half its development value; the central independent-seed test must retain the relevant tau threshold and a paired CI excluding zero. Failure rejects or downgrades the candidate before holdout.

## NOVELTY PROCEDURE

After selection and before holdout, search primary literature using repeated-auction, finite-horizon, valuation-gap, FPA/SPA learning, no-regret revenue, mechanism ranking, robust finite-time performance, and synonymous terms. Record closest theorem-level overlaps and classify LIKELY KNOWN, SUBSTANTIAL OVERLAP, POSSIBLE GAP, or STRONG GAP CANDIDATE. Never label the result novel in this phase.

## LEVEL-3 PASS CRITERION

PASS requires one prospectively detected, economically meaningful candidate with paired-seed robustness, survival of all major applicable falsifications, meaningful independent holdout evidence, no obvious implication by known baseline literature, and a credible learning-dynamic explanation. MIXED applies when a candidate is interesting but fails one important robustness/holdout/novelty condition. FAIL applies when no useful candidate fires or the primary candidate is killed. No parameter expansion or replacement candidate is allowed after outcomes.
