# Level 2 replication report

Protocol frozen as SHA256 `7bcd8f4754009ddb9eff0d9989e6c126aa8d6fa2fc94f636498fdb6a0df395d8` before the powered results. Inference unit: independent seed. All confidence intervals below are normal-approximation 95% intervals across 30 seeds.

## R-REP-001 — Kolumbus–Nisan second-price Hedge dynamics: PASS

- **Configuration:** two bidders, values `(1,.5)`, bidder-specific `.01` grids prohibiting overbidding, full-information Hedge, 50,000 rounds, 30 seeds.
- **Expected:** high bidder wins at least .98; tail price below .40 and within .05 of published .270; median regret/round below .02.
- **Result:** price `.27058` (CI `.26998–.27117`); high win share `.99998`; median regrets/round `.00146` and `.00055`.
- **Agreement:** all frozen criteria pass; published simulation reports approximately `.270 ± .005`.
- **Caveat:** exact finite-run learning-rate formula was not stated in accessible source text; standard horizon-calibrated Hedge was used.

## R-REP-002 — Kolumbus–Nisan first-price second-price outcome: PARTIAL

- **Configuration:** same, first-price auction.
- **Expected:** high win share at least `.98`; price `.48–.52`; at least 80% stable-tail classification; median regret/round below `.02`.
- **Result:** price `.49550` (CI `.49538–.49562`); high win share `.98019`; median regrets `.00897` and `.00252`; high/low stable-tail rates only `.033/.200`.
- **Agreement:** economic direction and magnitude reproduce closely; frozen policy-stability criterion fails.
- **Diagnosis:** the empirical L1 statistic over 101/51 bins and two 5,000-action windows has substantial sampling distance even with little mean drift (`.00075/.00225`). The criterion appears poorly calibrated for broad mixed policies. This is recorded as a protocol failure and was not redefined post hoc.

## R-REP-003 — Aggarwal et al. learning-rate effect: PARTIAL / NOT THEOREM-COMPARABLE

- **Configuration:** SPA, values `(1,.5)`, winner standard Hedge rate, runner rate ratio 1 versus 10, paired 30 seeds, 50,000 rounds.
- **Expected:** equal-rate runner bid below `.45`; fast rate at least `.45` and at least `.05` above equal.
- **Result:** equal `.27058`; fast `.37563`; paired increase `.10505` (CI `.10373–.10637`); fast target `.45` not reached.
- **Agreement:** strong predicted direction, failed preregistered level criterion.
- **Caveat:** fixed ratio 10 at one horizon does not instantiate the paper's asymptotic `omega(1)` rate ratio; this cannot be called a full theorem replication.

## Gate decision

Only one target is a strict PASS. **LEVEL 2 = MIXED; the PASS gate is not cleared.** Per protocol, Level 3 discovery, principal-instruction search, M4 formalization, and M5 generalization were not run.

## Reproducibility

Seed results: `results/replication/seed_results.csv`. Aggregates: `results/replication/aggregate.csv`. Each condition has a machine-readable manifest. Powered workload: 90 runs and 4,500,000 auction rounds; summed per-run runtime approximately 800 seconds.

