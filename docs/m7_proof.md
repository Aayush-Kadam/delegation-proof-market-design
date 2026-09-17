# M7 proof and payoff audit

For high bids `(0,h=v/2,v,1)` and low bids `(0,v)`, direct enumeration gives the utilities in `M7_STATUS.md`. Allocation probabilities against low bid probability `p` are `(1-p)/2`, `1-p/2`, `1-p/2`, and `1`. FPA revenue is `v q_h/2+v q_v+q_1+pvq_0`; SPA revenue is `pv(q_v+q_1)+pvq_h/2`.

The four log ratios reconstruct the mixed policies exactly, so the displayed recurrence is algebraically identical to full-information Hedge. The 480 interval subboxes exactly partition `[3/10,9/25]x[4/5,6/5]x[1/20,3/20]`. Positive lower endpoints in `results/m7/interval_box.json` prove TH-M7-003 for every H=2,...,6. Welfare follows from the allocation identity.

For TH-M7-004, Hedge gives `w_t(a)/w_t(b)=w_0(a)/w_0(b) exp(-eta[U_t(b)-U_t(a)])`. Equal initial weights and the gap assumption give the ratio bound. The denominator contains each witness weight, so summing yields the off-core mass bound. Renormalizing on core cancels the common expanded denominator and recovers core probabilities. A bounded statistic changes by at most total variation, which here equals off-core mass.
