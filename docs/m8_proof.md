# M8 proof

The `4x3` payoff matrices are generated from the auction definitions: high win probability is `1`, `1/2`, or `0`; FPA utilities are `p_i(v_i-b_i)` and revenue is the winner's bid; SPA utilities are `p_i(v_i-b_{-i})` and revenue is the lower bid. Because the ordered actions are fixed for every `0<v<1`, all entries are exact affine functions of `v`.

The five adjacent log-weight ratios reconstruct both policies. Hedge therefore gives the recurrence by adding learning rate times adjacent expected-utility gaps. The 384 interval subboxes partition `[.31,.35]x[.85,1.15]x[.06,.14]`. Every revenue and allocation lower endpoint in `results/m8/interval_box_narrow.json` is positive for H=2,...,6, proving TH-M8-002.

For stability, a bounded payoff vector is `1/2`-Lipschitz in opponent L1 distance. Core conditioning plus off-core mass gives full-policy distance at most `d_t+2e_t`. Cumulative logit discrepancy is therefore at most `eta_i/2 sum(d_s+2e_s)`. The tight softmax `L-infinity` to `L1` Lipschitz bound and summing players gives the displayed recurrence. Induction proves the discrete Gronwall expression. Bounded revenue/allocation expectations differ by at most half the joint L1 distance, giving the conditional transfer criterion.
