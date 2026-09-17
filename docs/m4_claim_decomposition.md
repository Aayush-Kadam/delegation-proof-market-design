# M4 claim decomposition

Frozen empirical source: Level 3 candidate commit `241577f`; completed evidence commit `6e683ec`. This decomposition uses existing Level 3 results only. It does not modify the candidate or initiate a new experiment.

## Environment and notation

There are two persistent-value bidders with `v_H=1` and `v_L=v<1`, discrete no-overbid grids of step `epsilon=.01`, uniform tie-breaking, and full expected-counterfactual feedback. Both bidders use Hedge with rates

`eta_i = c_i sqrt(log(K_i)/H)`.

The mechanism `M` is either first price (`FPA`) or second price (`SPA`). For the frozen holdout, `v` is in `{.1,.3,.5,.7,.9}`, `H` is in `{5,000;25,000;100,000}`, `(c_H,c_L)` is in `{(1,1),(.5,1),(1,.5),(1,2),(2,1)}`, and each cell has 30 paired seeds 2000--2029.

With benchmark revenue `R*=v`, efficient-allocation probability `AE*=1`, and efficient welfare `W*=1`, define

- `DL_R(M)=v-R(M)` and `NDL_R(M)=DL_R(M)/v`;
- `DL_E(M)=1-Pr(high bidder wins under M)`;
- `DL_W(M)=1-W(M)`;
- `Delta_X = DL_X(FPA)-DL_X(SPA)` (or the analogous difference for surplus).

Negative `Delta_NDL_R` favors FPA on revenue robustness. Positive `Delta_E` or `Delta_W` favors SPA on allocation or welfare.

## Exact selected and confirmatory results

The selected development cell `(v,H,c_H,c_L)=(.2,10,000,.5,1)` yielded:

| Contrast | Paired mean | Paired 95% CI |
|---|---:|---:|
| `Delta_NDL_R` | `-.662153` | `[-.663931,-.660374]` |
| `Delta_E` | `.012983` | `[.012544,.013423]` |
| `Delta_W` | `.010387` | `[.010035,.010738]` |
| high-bidder surplus, FPA-SPA | `-.142911` | `[-.143366,-.142456]` |
| low-bidder surplus, FPA-SPA | `.0000936` | `[.0000751,.0001120]` |
| total bidder surplus, FPA-SPA | `-.142817` | `[-.143264,-.142371]` |

All eight preregistered falsification attacks passed. In the independent frozen holdout, 54 of 75 environment cells met the directional/economic/significance gate. The strongest joint-magnitude passing cell `(v,H,c_H,c_L)=(.1,5,000,.5,1)` had `Delta_NDL_R=-1.042577`, `Delta_E=.006593`, and `Delta_W=.005934`; it passed through welfare, not the allocation-error floor.

## Atomic claims

### C-A — Finite-horizon revenue ranking

Within the frozen Hedge/full-information/fixed-value domain, FPA has lower normalized revenue delegation loss than SPA in 72 of 75 holdout cells. The cell-mean range is `[-1.042577,.028429]`. Sixty-eight cells satisfy the preregistered FPA-revenue magnitude and significance component.

This is a mechanism ranking over a finite, prospectively fixed environment family; it is not a theorem for arbitrary no-regret learners.

### C-B — Allocation and welfare ranking

SPA has lower allocation loss and lower welfare loss in all 75 holdout cells. `Delta_E` ranges from `.000433` to `.324087`; `Delta_W` ranges from `.000389` to `.058886`.

The welfare contrast is mechanically related to misallocation in the two-bidder persistent-value model: each low-bidder win loses `1-v` units of welfare. It should not be presented as an independent causal phenomenon.

### C-C — Objective conflict

FPA's revenue ranking and SPA's allocation/welfare ranking disagree economically and statistically in 54 of 75 holdout cells. Formally, for environment `z=(v,H,c_H,c_L,epsilon)`, define

`C = {z: Delta_NDL_R(z)<=-.05, CI_R^upper(z)<0, and [(Delta_E(z)>=.01 and CI_E^lower(z)>0) or (Delta_W(z)>=.005 and CI_W^lower(z)>0)]}`.

The validated statement is `|C intersect Z_holdout|=54`. It is a joint, vector-valued ranking result, not merely a revenue comparison.

### C-D — Valuation-gap dependence

Gate support is non-monotone at the extremes and broad in the interior:

| `v_L` | Passing cells / 15 |
|---:|---:|
| `.1` | 1 |
| `.3` | 15 |
| `.5` | 15 |
| `.7` | 15 |
| `.9` | 8 |

At very low `v`, revenue effects are large but allocation/welfare effects often fall below their economic floors. Near equal values, allocation effects are large but normalized revenue advantage weakens for some rate/horizon cells. The robust conflict is therefore primarily an interior valuation-gap region.

### C-E — Horizon dependence

Level 3 did not establish a horizon sign reversal. Each frozen horizon has 18 passing cells out of 25. Horizon changes magnitudes and, at boundary valuations, which rate pairs cross the fixed economic floors; it is not independently validated as a monotone threshold law.

### C-F — Learning-rate dependence

Every prespecified rate pair supports the conflict somewhere, with 9--12 passing cells out of 15. The rates modulate the surface but no one rate asymmetry is necessary for the holdout result. Therefore “under asymmetric adaptation” describes the selected development cell but is too narrow for the completed empirical region.

### C-G — Bidder-surplus redistribution

Across all 75 holdout cells, high-bidder surplus is lower under FPA and low-bidder surplus is higher under FPA. Total bidder surplus is lower under FPA in 74 cells and higher in one. At the selected development cell, the low bidder's positive difference is tiny relative to the high bidder's loss. This is consistent with FPA transferring surplus to the seller while SPA protects the high bidder and allocative efficiency.

### C-H — No worst-case/average or reversal claim

The preregistered C1 valuation reversal, C2 horizon reversal, C4 mean-versus-worst revenue-ranking conflict, and C5 sharp adjacent valuation sign boundary did not fire in development. M4 must not retrofit those rejected candidate classes into positive claims.

## Scope boundary

The evidence covers two bidders, persistent values, FPA/SPA, discrete no-overbid actions, full-information Hedge, fixed within-run learning rates, and finite horizons no greater than 200,000. It does not establish cross-algorithm robustness, stochastic/private-value equilibrium behavior, partial-feedback behavior, asymptotics, optimal mechanism design, or novelty.
