# M4 claim-by-claim novelty matrix

Audit date: 2026-09-17. Scope: primary papers and official proceedings available through the audit date. Classifications distinguish a known ingredient from the jointly validated Level 3 object.

## Closest literature, model by model

### Kolumbus and Nisan (WWW 2022)

Yoav Kolumbus and Noam Nisan, “Auctions Between Regret-Minimizing Agents,” *The Web Conference 2022*, DOI `10.1145/3485447.3512055`, [arXiv:2110.11855](https://arxiv.org/abs/2110.11855).

- **Model:** repeated FPA/SPA, persistent values, discrete bids, regret-minimizing/mean-based agents; multiplicative-weights simulations.
- **Result:** SPA principals can benefit from misreporting to their agents; FPA truthful reporting is dominant at the principal layer. Their Theorem 2 states that, conditional on convergence to a CCE, two mean-based agents in discrete FPA approach the second-price outcome: the high-value bidder wins with probability approaching one and average price approaches the low value up to grid error. Lemma 3 localizes co-undominated CCE support near the low value.
- **Overlap:** directly establishes the broad FPA revenue/efficiency mechanism and uses essentially the same persistent-value learning laboratory. It does not provide the Level 3 seed-paired finite-horizon vector surface or its fixed economic conflict gate.

### Aggarwal, Gupta, Perlroth, and Velegkas (NeurIPS 2024)

Gagan Aggarwal, Anupam Gupta, Andres Perlroth, and Grigoris Velegkas, “Randomized Truthful Auctions with Learning Agents,” *NeurIPS 2024*, [paper](https://papers.nips.cc/paper_files/paper/2024/file/434958fd1edf1f027306cb7f1b75fbf5-Paper-Conference.pdf), [arXiv:2411.09517](https://arxiv.org/abs/2411.09517).

- **Model:** two persistent-value no-regret bidders in deterministic and randomized truthful auctions; finite and asymptotic horizons; learning-rate comparisons.
- **Result:** the runner-up need not converge to truthful bidding in general deterministic truthful auctions; relative learning rates can qualitatively change convergence. Randomized truthful auctions can improve revenue guarantees. Their non-asymptotic auctioneer-regret results are almost tight at `T^(3/4)` for a fixed auction and `sqrt(T)` when the auction may change obliviously.
- **Overlap:** closes runner-up shading, learning-rate dependence, and finite-time seller-revenue loss as broad novelty claims. It does not rank FPA and SPA jointly on seller revenue and allocation/welfare over the Level 3 finite grid.

### Feng, Guruganesh, Liaw, Mehta, and Sethi (AAAI 2021)

Zhe Feng, Guru Guruganesh, Christopher Liaw, Aranyak Mehta, and Abhishek Sethi, “Convergence Analysis of No-Regret Bidding Algorithms in Repeated Auctions,” *AAAI 35(6)*, 5399--5406, DOI `10.1609/aaai.v35i6.16680`, [official page](https://ojs.aaai.org/index.php/AAAI/article/view/16680).

- **Model:** repeatedly redrawn values from unknown distributions; mean-based algorithms; SPA, VCG, and FPA.
- **Result:** high-probability last-iterate convergence to truthful pure Nash equilibrium in SPA/VCG and Bayesian Nash equilibrium in FPA under their assumptions.
- **Overlap:** establishes strong allocation/equilibrium-selection behavior for mean-based learners. The stochastic-value model and asymptotic/high-probability object differ from Level 3's persistent asymmetric values and finite-horizon losses.

### Hoy, Jain, and Wilkens (EC 2013)

Darrell Hoy, Kamal Jain, and Christopher A. Wilkens, “A Dynamic Axiomatic Approach to First-Price Auctions,” *EC 2013*, 583--584, DOI `10.1145/2492002.2482567`, [arXiv:1304.7718](https://arxiv.org/abs/1304.7718).

- **Model:** repeated FPA under behavioral axioms rather than equilibrium; comparison to SPA.
- **Result:** when losing bidders raise bids sufficiently quickly, FPA generates at least SPA revenue; stronger behavioral axioms yield stronger guarantees.
- **Overlap:** makes broad dynamic FPA revenue superiority known. It does not supply Hedge-specific finite-horizon efficiency tradeoffs.

### Syrgkanis, Agarwal, Luo, and Schapire (NeurIPS 2015)

Vasilis Syrgkanis, Alekh Agarwal, Haipeng Luo, and Robert E. Schapire, “Fast Convergence of Regularized Learning in Games,” *NeurIPS 2015*, [proceedings](https://papers.neurips.cc/paper/5763-fast-convergence-of-regularized-learning-in-games), [arXiv:1507.00407](https://arxiv.org/abs/1507.00407).

- **Model:** finite normal-form smooth games and regularized no-regret dynamics with recency bias.
- **Result:** Proposition 2 gives average welfare at least `lambda/(1+mu) OPT - (sum_i r_i(T))/((1+mu)T)`; their special dynamics obtain faster welfare convergence.
- **Overlap:** regret-to-welfare control is known generically. It is a lower bound relative to smoothness/PoA, not a sharp FPA-versus-SPA allocation-loss difference or seller-revenue bound.

### Bichler, Gupta, and Oberlechner (working paper, 2023; later revisions)

Martin Bichler, Alok Gupta, and Matthias Oberlechner, “Revenue in First- and Second-Price Display Advertising Auctions: Understanding Markets with Learning Agents,” [arXiv:2312.00243](https://arxiv.org/abs/2312.00243).

- **Model:** complete/incomplete-information display-ad auctions, common online learners, and payoff/ROI objectives.
- **Result:** examines FPA/SPA convergence and revenue; revenue equivalence can fail, with conclusions sensitive to bidder objectives and market model.
- **Overlap:** direct computational mechanism comparison makes an unqualified empirical FPA/SPA revenue comparison incremental. Its ROI/ad-market model does not match the Level 3 persistent-value Hedge surface.

### Ipsen and Skoulakis (ICML 2026)

Anders Bo Ipsen and Stratis Skoulakis, “Revenue Efficiency of Correlated Equilibria in First Price Auctions” / “Revenue Guarantees of No-Swap-Regret Dynamics in First Price Auctions,” *ICML 2026*, [arXiv:2606.06085](https://arxiv.org/abs/2606.06085).

- **Model:** discrete FPA and approximate correlated equilibrium/no-swap-regret dynamics.
- **Result:** revenue of any epsilon-approximate correlated equilibrium is at least `v_2 - Theta(1/k) - Theta(epsilon k^2)`; this yields polynomial finite-time revenue rates for no-swap-regret bidders.
- **Overlap:** substantially narrows any claim that finite-horizon FPA revenue robustness itself is open. Hedge supplies external regret, not generally swap regret, so the theorem does not directly certify the Level 3 dynamics.

## Novelty matrix

| Atomic claim | Closest literature | Already known? | Our extension | Classification | Novelty confidence |
|---|---|---|---|---|---|
| C-A: FPA usually has lower finite-horizon normalized revenue loss | Kolumbus--Nisan; Hoy--Jain--Wilkens; Ipsen--Skoulakis | Broad direction and asymptotic/equilibrium revenue mechanism are known | Prospective 75-cell Hedge surface with paired uncertainty and fixed economic floors | INCREMENTAL | High |
| C-B: SPA has lower allocation and welfare loss | Feng et al.; Kolumbus--Nisan; smoothness literature | Truthful/efficient SPA learning and FPA efficiency bounds are known | Persistent-value finite-horizon FPA-SPA difference in all 75 holdout cells | INCREMENTAL | Medium-high |
| C-C: revenue and efficiency rankings conflict in 54/75 cells | Combination of the above; no exact matching theorem found | Ingredients are known; joint vector classification was not located | Prospective, jointly thresholded finite-horizon conflict surface | POSSIBLY DISTINCT | Medium |
| C-D: conflict support is broad for `v_L=.3--.7` and weak at extremes | No matching value-gap phase map found; Kolumbus--Nisan contains value-gap dependence in FPA bounds | Qualitative value-gap relevance is known | Empirical interior support region across rates and horizons | POSSIBLY DISTINCT | Medium-low; thresholds partly induce the shape |
| C-E: horizon changes magnitudes but no sign reversal was established | Aggarwal et al. finite-time auctioneer regret; convergence papers | Finite-time dependence is known | Descriptive surface only; no new law or threshold | KNOWN | High |
| C-F: rate factors modulate the surface | Aggarwal et al. explicitly prove qualitative learning-rate effects | Yes | Paired map over five fixed rate pairs | INCREMENTAL | High |
| C-G: FPA shifts surplus from high bidder toward seller; SPA protects high-bidder surplus | Accounting identities plus Kolumbus--Nisan/Aggarwal et al. mechanisms | Broad distributional mechanism is anticipated | Exact paired finite-horizon decomposition | INCREMENTAL | Medium-high |
| Regret-to-welfare bound | Syrgkanis et al.; auction smoothness/PoA literature | Yes | None needed | KNOWN | High |
| External-regret-only seller-revenue bound for SPA | Kolumbus--Nisan; Aggarwal et al. runner-up non-truthfulness | Impossible without added assumptions | A zero-regret, zero-revenue SPA counterexample restates the obstruction | KNOWN | High |

## Novelty residual

**Strongest surviving one-sentence contribution:** Prior work separately explains FPA revenue robustness, SPA runner-up shading, allocation convergence, and learning-rate effects; Level 3 adds a prospectively frozen, paired finite-horizon map showing that these ingredients jointly produce an objective-specific mechanism-ranking conflict over a broad interior persistent-value region, with seller revenue favoring FPA while allocation, welfare, and high-bidder surplus favor SPA.

This is a **promising but narrow computational characterization**, not yet a theorem and not a new broad auction-learning phenomenon.
