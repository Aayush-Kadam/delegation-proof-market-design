# R-REP-003 theorem mapping

## Exact source result

Aggarwal, Gupta, Perlroth, and Velegkas (2024), Theorem D.4, “Effect of Learning Rate on Convergence.” For fixed values and a non-degenerate deterministic truthful single-item auction, bidders use MWU with non-degenerate learning rates. If `eta_R(T)/eta_W(T)=omega(1)`, then with probability at least `1-o(1)` the runner-up's **last-round bid distribution** converges to a point mass on its truthful bid; the winner's last-round distribution is supported between its minimum winning bid and value.

## Learner and feedback

MWU initializes all feasible no-overbid actions uniformly and updates `w_j <- w_j exp(eta_T u_j^t)`. Full feedback supplies the expected counterfactual utility of every bid. The paper's Algorithm 1 gives the canonical equal rate `sqrt(log Delta/T)`.

## Rate requirements

Each rate is non-degenerate: `eta_T T -> infinity` and `eta_T log T -> 0`. The faster-runner theorem additionally requires `eta_R(T)/eta_W(T) -> infinity`.

## Implemented representative family

V2 uses `eta_W(T)=sqrt(log K_W/T)` and `eta_R(T)=sqrt(log K_R) T^(-1/3)`. Both are non-degenerate, and their ratio grows proportionally to `T^(1/6)`, hence diverges. The equal-rate control uses each bidder's canonical `sqrt(log K_i/T)` rate.

## Convergence object

The source uses last-iterate total-variation convergence. Accordingly, V2's primary quantity is terminal exact-policy truthfulness distance `D_T = 1-pi_R^T(v_R)`, which is precisely TV distance from the runner's last policy to the truthful point mass. Expected-bid distance is secondary.

## Probability mode and asymptotic status

The result holds with probability `1-o(1)` over algorithmic play as `T -> infinity`. A finite horizon ladder can test directional approach but cannot prove the theorem.

