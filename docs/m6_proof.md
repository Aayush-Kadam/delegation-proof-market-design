# Proof certificate for TH-M6-003

The payoff enumeration gives the exact recurrence recorded in `M6_STATUS.md`. Induction shows that the recurrence equals full-information Hedge because the three log-weight ratios reconstruct the mixed strategies exactly at every round.

For each mechanism and each parameter subbox, interval propagation encloses `(x_t,y_t,z_t)`, the induced probabilities, per-round revenue, and per-round allocation. Addition and division by `H` enclose the time averages. Subtracting the SPA revenue enclosure from FPA and the FPA allocation enclosure from SPA gives certified contrast intervals.

The 480 subboxes form an exact partition of

`[3/10,9/25] x [4/5,6/5] x [1/20,3/20]`.

For every `H=2,...,9`, the minimum lower endpoints stored in `results/m6/interval_box.json` are strictly positive. Therefore every point of the rectangle satisfies both strict inequalities. The welfare result follows from `W_S-W_F=(1-v)(A_S-A_F)`.

The enclosure at `H=10` crosses zero only for allocation. No negative point was found; no conclusion is asserted there.
