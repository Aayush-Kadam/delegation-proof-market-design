# DELEGATION-PROOF MARKET DESIGN — PHASE II STATUS

## 1. Executive verdict

**REPLICATION FAILED**

“Failed” refers to the preregistered Level 2 gate, not a total failure to reproduce the literature. The second-price Hedge result is a clean PASS and matches the published price almost exactly. The first-price economic outcome also matches closely, but a frozen policy-stability criterion fails. The learning-rate experiment strongly matches the predicted direction but does not reach the preregistered truthfulness threshold and is not fully comparable to the asymptotic theorem. With only one strict PASS, Level 2 cannot be marked PASS. The required gate therefore prohibits M3 discovery, the principal-instruction campaign, M4 refinement, M5 validation, and Level 6 mechanism work. The main methodological finding is that the empirical high-dimensional L1 convergence diagnostic was inadequately calibrated, despite negligible mean-bid drift. No novel phenomenon is claimed.

## 2. Level scorecard

- Level 1: MIXED
- Level 2: MIXED (gate FAIL)
- Level 3: NOT RUN
- Level 4: MIXED (unchanged preliminary framework)
- Level 5: NOT RUN
- Level 6 pilot: NOT RUN

## 3. Replication results

### Kolumbus–Nisan SPA

- **Configuration:** 30 seeds, 50,000 rounds, `(1,.5)`, `.01` no-overbid grids, full-information Hedge.
- **Result:** price `.27058` (95% CI `.26998–.27117`), high win share `.99998`.
- **Expected:** price near `.270` and below `.40`; high win share at least `.98`.
- **Agreement:** PASS.
- **Caveat:** standard horizon-calibrated eta substitutes for an unstated displayed-simulation eta formula.

### Kolumbus–Nisan FPA

- **Configuration:** same, FPA.
- **Result:** price `.49550` (CI `.49538–.49562`), high win share `.98019`, but only 3.3% high-bidder stable-tail labels.
- **Expected:** price near `.50`, high win share at least `.98`, 80% stable-tail rate.
- **Agreement:** PARTIAL.
- **Caveat:** economic result agrees; frozen convergence diagnostic fails.

### Aggarwal et al. learning-rate effect

- **Configuration:** paired 30 seeds, SPA, runner rate ratios 1 and 10.
- **Result:** runner bid rises from `.27058` to `.37563`; paired gain `.10505` (CI `.10373–.10637`).
- **Expected:** gain at least `.05` and fast mean at least `.45`.
- **Agreement:** PARTIAL; not theorem-comparable.
- **Caveat:** fixed ratio 10 is not an asymptotically divergent ratio.

## 4. Primary discovery

None. Discovery was barred by the Level 2 gate.

## 5. Candidate ranking

No discovery candidates were scored. Treating replication diagnostics as candidates would violate the frozen sequence.

## 6. Principal-instruction result

Not run. No estimate of `hat v_i*` is reported.

## 7. Cross-algorithm results

Not run; no generalization matrix exists.

## 8. Falsification

The main internal falsification was semantic: bidder-specific grids removed overbidding, and full-information tie rewards were changed from sampled outcomes to exact uniform-tie expectations. Thirteen tests then passed. The frozen stability criterion itself was challenged by observing policy L1 around `.16` alongside mean drift below `.001`, revealing poor calibration for many-bin empirical distributions. The criterion was not changed after results.

## 9. Formal framework

No M4 finalization occurred. Existing finite-horizon delegation gaps remain preliminary and must explicitly index benchmark, learner class, feedback, valuation process, and horizon.

## 10. Theory candidates

No new theorem candidate is warranted. Three future questions, not conjectures, are: finite-sample calibration of policy-distance convergence tests; the rate at which runner-up bids approach truthfulness under diverging MWU rate ratios; and finite-horizon bounds linking external regret to auction revenue distortion. Proof progress: none. Literature overlap is substantial.

## 11. Level 6 recommendation

**DO NOT PROCEED YET.** The replication gate did not pass and no diagnosed new failure exists.

## 12. Repository status

- Tests: 13 passing before final audit
- Powered experiments: 90
- Independent seeds: 30 per condition
- Powered auction rounds: 4,500,000
- Powered runtime: approximately 800 seconds summed across runs
- Git commits/tags: none; the directory is not a Git repository
- New core artifacts: frozen replication specification/hash, corrected full-information semantics, diagnostics, replication runner, manifests, seed results, aggregate table, report, and expanded tests

## 13. Publication readiness

**3/10**, up from 2/10. The simulator now reproduces one central published quantitative result and closely matches another economic outcome, but the Level 2 gate remains uncleared and there is no original result.

## 14. Exact next move

Freeze a Level 2 protocol revision that replaces the uncalibrated empirical-bin L1 threshold with a simulation-calibrated or exact-policy stability measure, and instantiates Aggarwal et al.'s diverging learning-rate sequence across multiple horizons; then rerun only the failed replication targets.

