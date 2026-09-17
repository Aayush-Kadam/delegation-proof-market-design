# M5 theorem novelty audit

## Candidate audited

TH-M5-003 compares time-average FPA and SPA revenue and allocation after exactly two deterministic full-information Hedge rounds for persistent values `(1,v)` and bid grids `{0,v,1}` and `{0,v}`. It supplies an explicit conflict region and a positive revenue margin.

## Theorem-level comparison

| Work | Closest result | Difference from TH-M5-003 |
|---|---|---|
| Kolumbus & Nisan (WWW 2022), arXiv:2110.11855 | Mean-based FPA convergence near the second-price outcome when dynamics converge; MW behavior in SPA | Not a two-round joint FPA/SPA revenue-and-allocation ordering with explicit Hedge weights. |
| Aggarwal et al. (NeurIPS 2024), arXiv:2411.09517 | Runner-up non-truthfulness for deterministic truthful auctions, qualitative rate effects, and finite-time auctioneer-regret rates | Different mechanism-design objective and comparator; no matching simultaneous objective-conflict region found. |
| Feng et al. (AAAI 2021), arXiv:2009.06136 | Mean-based convergence to truthful SPA and Bayesian FPA equilibria with stochastic values and exploration | Different value model, algorithm assumptions, and asymptotic/anytime convergence target. |
| Hoy, Jain & Wilkens (EC 2013), arXiv:1304.7718 | FPA revenue at least SPA under a loser-raises-quickly behavioral axiom | Revenue-only and axiom-based; no allocation reversal or exact Hedge transient. |
| Syrgkanis et al. (NeurIPS 2015), arXiv:1507.00407 | Regret-to-welfare guarantees and fast convergence in smooth games | Welfare lower bounds, not mechanism ranking or seller/allocation sign conflict. |
| Ipsen & Skoulakis (ICML 2026), arXiv:2606.06085 | FPA revenue at least `v_2-Theta(1/k)-Theta(epsilon k^2)` for approximate CE/no-swap regret | FPA-only, equilibrium/regret based, and much longer time scale; no SPA allocation comparison. |

## Verdict

**POSSIBLY DISTINCT.** No equivalent theorem was located, but the contribution is narrow: an exact transient theorem on a minimal grid. The safe novelty sentence is: “Existing results separately bound revenue, characterize learning convergence, or explain SPA shading; TH-M5-003 gives an explicit small-grid finite-horizon region in which the two mechanisms are ranked oppositely on seller revenue and allocation.”

Primary sources: https://arxiv.org/abs/2110.11855, https://arxiv.org/abs/2411.09517, https://ojs.aaai.org/index.php/AAAI/article/view/16680, https://arxiv.org/abs/1304.7718, https://arxiv.org/abs/1507.00407, https://arxiv.org/abs/2606.06085.
