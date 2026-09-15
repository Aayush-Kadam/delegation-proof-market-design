# Frozen Level 2 replication specification — V2 repair

## Record and rationale

V1 remains frozen at SHA256 `7bcd8f4754009ddb9eff0d9989e6c126aa8d6fa2fc94f636498fdb6a0df395d8`; it was executed and its Level 2 gate failed. V2 does not alter R-REP-001 or reinterpret V1.

V1 R-REP-002 failed because an uncalibrated adjacent-window marginal empirical L1 threshold was imposed in addition to the source's economic prediction. A prospective stationary-policy null study using no R-REP-002 outcomes shows false rejection rates of `.856` (uniform K=51), `.700` (smooth K=51), and `1.000` for both K=101 policies. The source instead defines convergence of a cumulative empirical **joint** distribution and Theorem 2 conditionally derives high-winner/second-value economic outcomes.

V1 R-REP-003 used a fixed 10x ratio at one horizon, whereas source Theorem D.4 requires non-degenerate rates with `eta_R(T)/eta_W(T)=omega(1)` and studies last-iterate TV convergence. V2 implements that rate family and exact policy object.

## R-REP-002-V2 — first-price economic outcome repair

- **Source match:** Kolumbus–Nisan Theorem 2 and Hedge simulation, as mapped in `r_rep_002_source_mapping.md`.
- **Environment:** FPA; fixed values `(1,.5)`; `.01` bidder-specific grids; no overbidding; uniform ties; full expected-counterfactual feedback; Hedge initialized uniformly.
- **Rate:** `eta_i(T)=sqrt(log(K_i)/T)`, fixed within run.
- **Power:** 30 independent seeds; 50,000 rounds.
- **Primary source-match metrics:** second-half mean transaction price and high-value win share.
- **Economic PASS region:** cross-seed mean price `[.48,.52]`; mean high-value win share at least `.98`; median external regret/round below `.02` for both agents.
- **Finite-horizon economic-stability diagnostic:** median absolute first-half/second-half price change at most `.01` and median high-win-share change at most `.02`. These one-grid-unit/two-percentage-point thresholds are project diagnostics, not attributed to the source.
- **Policy diagnostics (descriptive, not pass gates):** exact Hedge policy TV and Wasserstein-1 between rounds `T-5000` and `T`; exact expected-bid change; V1 empirical L1 retained for comparison.
- **PASS:** all economic and economic-stability criteria hold. **PARTIAL:** source-match outcomes hold but stability or regret fails. **FAIL:** source-match price or winner criterion fails.

## R-REP-003-V2 — theorem-comparable rate sequence

- **Source:** Aggarwal et al. Theorem D.4 and Definition C.2, mapped in `r_rep_003_theorem_mapping.md`.
- **Environment:** deterministic truthful SPA; fixed values `(1,.5)`; `.01` no-overbid grids; uniform ties; full expected-counterfactual feedback; source MWU/Hedge update and uniform weights.
- **Equal-rate control:** `eta_i(T)=sqrt(log(K_i)/T)`.
- **Diverging-rate treatment:** `eta_W(T)=sqrt(log(K_W)/T)` and `eta_R(T)=sqrt(log(K_R))*T^(-1/3)`. Each rate satisfies `eta T -> infinity` and `eta log T -> 0`; the ratio is proportional to `T^(1/6) -> infinity`.
- **Horizon ladder:** `25,000; 50,000; 100,000; 200,000`.
- **Power:** 30 paired seeds per schedule and horizon.
- **Primary metric:** exact terminal last-iterate truthfulness distance `D_T=TV(pi_R^T,delta_{v_R})=1-pi_R^T(v_R)`.
- **Secondary:** terminal expected-bid distance `|E_pi[b]-v_R|`, regret, and rate ratio.
- **PASS requires:** (1) mean treatment `D_200000` is at least `.05` below `D_25000`, with paired 95% CI for the reduction excluding zero; (2) treatment mean `D_T` is below equal-rate mean at every horizon, with paired 95% CI excluding zero at every horizon; (3) treatment mean expected-bid distance falls by at least 25% from 25,000 to 200,000; and (4) median regret/round is below `.02` in all conditions.
- **PARTIAL:** all treatment effects have the predicted sign but one quantitative/trend criterion fails. **FAIL:** treatment is not closer to truthful at the final horizon or regret fails materially.
- **Interpretation boundary:** PASS is a finite-horizon computational replication of the theorem's predicted asymptotic direction, not proof of asymptotic convergence.

## Final Level 2 gate

R-REP-001 remains PASS. Level 2 clears if at least one of R-REP-002-V2 or R-REP-003-V2 passes prospectively. V2 results do not overwrite V1 labels.

## Freeze record

The canonical SHA256 is stored in `replication_spec_v2.sha256` before powered execution.

