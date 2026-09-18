# M10 gap-adaptive mechanism protocol

## Mechanism

For top and second bids `b1>=b2`, define `g=0` when `b1=0`, otherwise `g=(b1-b2)/b1`. Set

`alpha(g;a,tau)=a+(1-a)*min(g/tau,1)`

and charge the winner `p=b2+alpha(g;a,tau)*(b1-b2)`. Allocation and fair ties are unchanged. The rule uses only submitted bids.

## Frozen development design

- The M9 development/holdout environment split is unchanged; the M9 holdout stays sealed.
- All nine homogeneous and ordered heterogeneous learner profiles are retained.
- Coarse grid: `a in {.20,.35,.50}` and `tau in {.20,.40,.60,.80}`.
- Paired development seeds: `7000,7001,7002`.
- Expected new runs: `12*15*9*3=4860`.
- Exact logical rounds: `124,740,000`.
- Verified M9 alpha `0` and `1` development records on matching seeds provide endpoint baselines; they are not rerun.

M10 is explicitly diagnosis-guided by M9 development evidence and is not an independent family-discovery exercise. Only the untouched holdout can support confirmation.

## Frozen metrics and floors

Use M9 definitions: `q_R=(best endpoint revenue-candidate revenue)/max(v_L,.1)`, `q_A=best endpoint allocation-candidate allocation`, and `q_joint=max(q_R,q_A)` at each profile/environment cell. Eligibility remains `max q_R<=.25` and `max q_A<=.10`.

Report mean, median, p90, p95, worst and CVaR90 regret; H/R and F/R; high valuations; role sensitivity; mean normalized bid gap; and mean realized interpolation weight by valuation stratum.

## Frozen selection and refinement

Among eligible candidates choose lexicographically: smallest worst joint regret, then worst revenue regret, then worst allocation regret. Quantities within `1e-9` are tied; only then prefer larger tau, then smaller a.

Refinement is allowed only if a coarse point is eligible or if one point misses *each* floor by at most `.02`. Refine around the single best coarse region, with at most six new pairs, frozen in a separate commit before execution. Otherwise stop development and do not open holdout.

## Holdout and later gates

If eligible, commit the exact candidate and hashes before evaluating SPA, FPA, and GAH on the untouched 10-environment, 9-profile, 30-seed holdout. Red team and theory require holdout success. If development fails, neither is run.
