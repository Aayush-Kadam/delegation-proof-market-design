# DELEGATION-PROOF MARKET DESIGN — LEVEL 2 FINAL REPLICATION STATUS

## Executive verdict

**LEVEL 2 REMAINS MIXED**

The remaining problems are finite-horizon and diagnostic, not substantive failures to reproduce the published economic direction. R-REP-001 remains a clean PASS. R-REP-002 reproduces the first-price price, allocation, and regret outcomes, but V2 narrowly misses its prospective half-to-half economic-stability thresholds. R-REP-003 now implements the theorem's actual diverging-rate condition and exact last-iterate TV object; the treatment moves monotonically toward truthfulness and dominates equal rates at every horizon, but the magnitude over 25k–200k is smaller than preregistered. Neither repaired target earns PASS. The Level 2 gate therefore remains closed, and no Level 3 work was performed.

## V1 vs V2

| Item | V1 | V2 | Why changed |
|---|---|---|---|
| Scientific record | Frozen and executed; gate failed | Prospectively frozen and executed | V1 remains untouched |
| R-REP-002 convergence diagnostic | Adjacent-window marginal empirical L1 | Source-relevant economic outcome stability; exact-policy TV/W1 descriptive | Null false-rejection reached 70–100%; source uses cumulative empirical joint distribution |
| R-REP-003 rate design | Fixed 1× vs 10× at T=50k | Equal vs `eta_R ∝ T^-1/3`, `eta_W ∝ T^-1/2` across four horizons | V2 ratio diverges as required by Theorem D.4 |
| R-REP-003 outcome | Tail sampled mean bid | Exact terminal TV to truthful point mass | Matches source last-iterate definition |
| Gate | One PASS | Still one PASS | Gate was not lowered |

## R-REP-001

Retained PASS: SPA price `.27058`, 95% CI `[.26998,.27117]`; high-value win share `.99998`; 30 seeds and 50,000 rounds. It was not rerun.

## R-REP-002

- **Source claim:** conditional on convergence of cumulative empirical joint dynamics, the high bidder wins asymptotically and average FPA price approaches the lower value up to grid error.
- **V2 metrics:** mean second-half price/winner share and half-to-half economic drift; exact-policy TV/W1 are descriptive.
- **Why V1 was inadequate:** under stationary policies, L1 `.10` false-rejection was `.700–1.000` for the preregistered null designs.
- **Seeds/horizon:** 30 / 50,000.
- **Price:** `.495504`, CI `[.495384,.495623]`.
- **Winner share:** `.980187`, CI `[.979794,.980579]`.
- **Convergence:** median price drift `.011347` versus `.01` threshold; win-share drift `.04112` versus `.02`.
- **Status:** **PARTIAL**.

## R-REP-003

- **Theorem assumption:** non-degenerate MWU rates and `eta_R(T)/eta_W(T)=omega(1)`; runner last-iterate policy converges in TV to truthful bidding with probability `1-o(1)`.
- **Schedule:** `eta_W=sqrt(log K_W/T)`; `eta_R=sqrt(log K_R)T^(-1/3)`; ratio grows as `T^(1/6)`.
- **Ladder:** 25k, 50k, 100k, 200k; 30 paired seeds per schedule/horizon.
- **TV trajectory:** `.95442, .95192, .94900, .94597` under diverging rates versus approximately `.975` throughout under equal rates.
- **Paired advantages:** `.02060, .02313, .02607, .02911`; every 95% CI excludes zero.
- **Trend:** TV reduction `.00845`, below required `.05`; expected-bid-distance improvement `12.9%`, below 25%.
- **Status:** **PARTIAL — direction consistent, asymptotic regime not reached**.

## Final Level 2 gate

\[
\boxed{\mathrm{FAIL}}
\]

One of three targets passes. The rule requires at least two.

## Scientific interpretation

**NO**, the simulator is not yet sufficiently validated under the project's own strict gate to begin original discovery. We trust its mechanism accounting and its reproduction of the central economic directions, but the finite-horizon convergence behavior remains unresolved relative to prospective thresholds.

## Repository integrity

- Tests before powered execution: 17 passing
- New powered simulations: 270
- New powered auction rounds: 24,000,000
- Runtime: 796 seconds wall clock with four workers
- V2 protocol hash: `b1a5cb3d11dc5e111475479557cfbd38cc316c9956603c0a2948da7af01832d1`
- Git: V1 preservation commit `2b92ec5`; V2 preregistration commit `a598b82`
- Outputs: seed table, aggregates, manifest, source mappings, null diagnostic, and two figures

## Exact next recommendation

Do not proceed to discovery. The remaining issue is computational asymptotics: derive or estimate the finite-horizon rate predicted by Theorem D.4 and determine, before further simulation, whether horizons capable of materially reducing last-iterate TV are computationally attainable. R-REP-002 should no longer be rerun without a source-grounded reason; its economic behavior has reproduced twice.

