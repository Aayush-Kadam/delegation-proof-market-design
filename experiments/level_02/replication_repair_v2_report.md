# Level 2 replication repair V2 report

Protocol SHA256: `b1a5cb3d11dc5e111475479557cfbd38cc316c9956603c0a2948da7af01832d1`. Frozen and committed before powered execution. V1 remains unchanged and failed its original gate.

## R-REP-002-V2 — PARTIAL

Thirty 50,000-round FPA seeds reproduce the source-relevant economics: second-half mean price `.495504` (95% CI `.495384–.495623`), high-value win share `.980187` (CI `.979794–.980579`), and median regret/round `.008972/.002519`. The prospective economic-stability diagnostic fails narrowly: median absolute half-to-half price change `.011347` exceeds `.01`, and win-share change `.04112` exceeds `.02`.

Exact-policy diagnostics show why categorical empirical L1 was misleading but do not erase the V2 failure: over the final 5,000 rounds, high-bidder exact-policy TV is `.08048` while Wasserstein-1 is only `.000843`; low-bidder values are `.003878` and `.000724`. Probability moves substantially among nearby bids but very little in economic bid distance.

## R-REP-003-V2 — PARTIAL

The implemented treatment satisfies source assumptions: both rates are non-degenerate and `eta_R/eta_W` grows as `T^(1/6)`. Exact last-iterate TV to truthful bidding is the primary source-matched metric.

| T | Rate ratio | Equal-rate TV | Diverging-rate TV | Paired TV advantage | Diverging expected-bid distance |
|---:|---:|---:|---:|---:|---:|
| 25,000 | 4.991 | .97502 | .95442 | .02060 | .16306 |
| 50,000 | 5.602 | .97505 | .95192 | .02313 | .15650 |
| 100,000 | 6.288 | .97507 | .94900 | .02607 | .14966 |
| 200,000 | 7.058 | .97508 | .94597 | .02911 | .14205 |

All paired advantages have 95% intervals excluding zero, and the treatment improves monotonically. However, TV falls only `.00845` from 25k to 200k (CI `.00786–.00904`), below the preregistered `.05`; expected-bid distance falls `12.9%`, below the required 25%. Regret criteria pass. The predicted direction is reproduced, but the asymptotic regime is not reached.

## Gate

R-REP-001 remains PASS. R-REP-002-V2 and R-REP-003-V2 are PARTIAL. Therefore **LEVEL 2 = MIXED; GATE = FAIL**.

