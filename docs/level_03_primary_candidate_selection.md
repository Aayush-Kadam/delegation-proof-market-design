# Frozen Level 3 primary candidate selection

Selection date: 2026-09-15. Development evidence commit: `e7ac539`. Holdout was not executed or inspected before this selection.

## Automatic candidate result

Only C3 fired. C1 valuation reversal, C2 horizon reversal, C4 mean-versus-worst revenue-ranking conflict, and C5 sharp revenue sign boundary did not meet the preregistered rules.

## Primary candidate

**Finite-horizon revenue-efficiency conflict under asymmetric adaptation.** At development cell v_H=1, v_L=.2, H=10,000, (c_H,c_L)=(.5,1), step=.01, FPA is substantially more revenue-robust than SPA relative to the common competitive benchmark, while SPA is more allocation-efficient and welfare-preserving.

Formally, with Delta_X=DL_X(FPA)-DL_X(SPA):

- Delta_NDL_R=-.662153, paired 95% CI [-.663931,-.660374];
- Delta_DL_AE=.012983, CI [.012544,.013423];
- Delta_DL_W=.010387, CI [.010035,.010738].

Thus FPA is preferred on revenue loss, whereas SPA is preferred on allocation and welfare loss. The full-horizon effect, not the tail alone, is primary. At the final 10%, revenue remains strongly FPA-favoring, while the AE effect falls below the preregistered one-percentage-point economic threshold; this attenuation is an explicit vulnerability to falsification.

## Candidate scores

| Dimension | Score |
|---|---:|
| Economic magnitude | 10/10 |
| Statistical robustness | 10/10 |
| Novelty potential before targeted audit | 6/10 |
| Theory tractability | 8/10 |
| Holdout testability | 9/10 |
| Policy relevance | 9/10 |
| Total | 52/60 |

## Holdout prediction

Without tuning: the conflict should appear in at least one frozen holdout cell with full-horizon |Delta_NDL_R|>=.05 favoring FPA and Delta_DL_AE>=.01 or Delta_DL_W>=.005 favoring SPA, with paired 95% CIs excluding zero. Broader persistence is descriptive support, not a revised gate.

## Falsification plan

Exactly the already preregistered attacks encoded in `configs/level_03/falsification/grid.json`: 50 independent seeds; finer .005 grid; v_L=.225; joint rate scaling .8 and 1.25; doubled horizon 20,000; and tail shares .05 and .20. The central independent-seed test must meet the original economic floors; all applicable attacks must preserve direction and at least half the development magnitude.
