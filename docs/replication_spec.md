# Frozen Level 2 replication specification

Frozen before powered outputs were inspected. The independent seed is the unit of replication. All bids are restricted to each bidder's reported value, ties are uniform, values are fixed, and Hedge receives expected full-information utility for every permissible bid after each round.

## R-REP-001 — second-price low-revenue Hedge dynamics

- **SOURCE:** Kolumbus and Nisan (2022), *Auctions Between Regret-Minimizing Agents*, Theorem 1 and Appendix A.1, Figure 7(a).
- **SOURCE RESULT:** with values `(1, 0.5)`, discrete bids, and equal-rate Hedge, the high bidder asymptotically wins and average price is below `0.5`; their 50,000-round simulation reports `0.270 ± 0.005`.
- **ORIGINAL MODEL/ASSUMPTIONS:** two fixed-value bidders; repeated SPA; no overbidding; epsilon grid; uniform tie-breaking; full-information multiplicative weights; horizon-dependent fixed update rate.
- **OUR IMPLEMENTATION:** values `(1,0.5)`; bid step `.01`; `T=50,000`; Hedge with fixed `eta=sqrt(log(101)/T)` for the high bidder and `sqrt(log(51)/T)` for the low bidder; uniform initial weights.
- **UNAVOIDABLE DIFFERENCE:** the paper's displayed simulation does not state an exact finite-run eta formula in the accessible text; we use the standard horizon-calibrated Hedge rate and test both qualitative and quantitative agreement.
- **PRIMARY METRIC:** seed-level mean price over the final 25,000 rounds.
- **EXPECTED:** high bidder tail win share at least `.98`; price below `.40`; cross-seed mean within `.05` of `.270`.
- **SEEDS/ROUNDS:** 30 independent seeds; 50,000 rounds each.
- **PASS:** all three expected criteria hold and median average external regret per round is below `.02` for both bidders.
- **FAIL:** high bidder win share below `.95`, mean price at least `.45`, or regret criterion fails. Otherwise PARTIAL.

## R-REP-002 — first-price second-price outcome

- **SOURCE:** Kolumbus and Nisan (2022), Theorem 2 and Appendix A.2, Figure 8(a).
- **SOURCE RESULT:** for values `(1,0.5)`, mean-based agents that converge approach an outcome where the high bidder wins and pays the lower value up to grid error; simulations show Hedge approaching this outcome.
- **MODEL/IMPLEMENTATION:** same as R-REP-001 except FPA.
- **PRIMARY METRIC:** tail high-bidder win share and mean transaction price.
- **EXPECTED:** tail win share at least `.98`; cross-seed mean price in `[.48,.52]`; at least 80% of seeds classified `stable_tail` under the predeclared diagnostic.
- **SEEDS/ROUNDS:** 30; 50,000.
- **PASS:** all expected criteria and median regret per round below `.02`. **FAIL:** win share below `.95`, price outside `[.45,.55]`, or regret criterion fails. Otherwise PARTIAL.

## R-REP-003 — learning-rate effect in deterministic truthful auctions

- **SOURCE:** Aggarwal, Gupta, Perlroth, and Velegkas (2024), Section 4 / Theorems summarized in Section 4.1.
- **SOURCE RESULT:** in a non-degenerate deterministic truthful auction, an equal/not-faster runner-up rate yields a non-truthful distribution with mean below value, while an asymptotically faster runner-up rate converges to truthful bidding.
- **ORIGINAL MODEL:** two values on a discrete grid, MWU, deterministic truthful auction, non-degenerate horizon-dependent rates.
- **OUR IMPLEMENTATION:** SPA with `(1,.5)`, step `.01`, winner rate `sqrt(log(101)/T)`; compare runner ratios `1` and `10`; paired seeds.
- **UNAVOIDABLE DIFFERENCE:** a fixed ratio of 10 at one horizon is not the theorem's `omega(1)` asymptotic sequence, so this is a finite-horizon qualitative analogue, not a theorem replication.
- **PRIMARY METRIC:** difference in tail mean runner-up bid, fast minus equal.
- **EXPECTED:** equal-rate mean below `.45`; fast-rate mean exceeds equal-rate by at least `.05` and is at least `.45`.
- **SEEDS/ROUNDS:** 30 paired seeds per condition; 50,000.
- **PASS:** both expected directional criteria and median regret per round below `.02`; **NOT COMPARABLE** if the finite-ratio design cannot meaningfully approach the asymptotic claim; otherwise PARTIAL/FAIL by direction.

## Frozen convergence rule

Using the final two non-overlapping windows of 5,000 bids, label a bidder `stable_tail` only when empirical policy L1 distance is at most `.10` and absolute mean-bid drift is at most `.02`. This is finite-horizon tail stability, not proof of asymptotic convergence.

## Freeze record

The canonical hash is recorded separately in `docs/replication_spec.sha256`; any modification changes the protocol version.

