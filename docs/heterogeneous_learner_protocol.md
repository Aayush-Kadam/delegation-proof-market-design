# Heterogeneous-learner validation protocol

## Frozen questions

- **QH1:** Does the FPA-revenue/SPA-allocation conflict survive ordered heterogeneous learner pairs?
- **QH2:** Is there material learner-role asymmetry under a role swap?
- **QH3:** Are profiles involving regret matching less quantitatively stable, consistent with Level-5 falsification?
- **QH4:** Does any ordered profile reverse either aggregate mechanism ranking?

## Scientific design

- Ordered `(high-value learner, low-value learner)` profiles: Hedge/FTPL, FTPL/Hedge, Hedge/RM, RM/Hedge, FTPL/RM, RM/FTPL.
- Exact reuse of Level 5's 25 environments, `.01` no-overbid grids, full-information feedback, FPA/SPA rules, learner implementations, and horizon/rate parameterization.
- Primary seeds: `6000,...,6029`, paired across mechanisms. Expected runs: 9,000. Exact logical auction rounds: 288,000,000.
- Pilot: five parameter-selected environments, seeds `4900,...,4909`, all six profiles and both mechanisms; 600 runs. Pilot cannot remove a primary profile.

## Frozen metrics and gates

For each profile/environment, paired seeds define `D_R=R_FPA-R_SPA`, `D_A=A_SPA-A_FPA`, and `D_W=W_SPA-W_FPA`. The Level-5 cell gate is unchanged: `D_R/v >= .05`, `D_A >= .01`, and paired normal 95% CI lower endpoints for raw `D_R` and `D_A` exceed zero.

Profile classification:

- **STRONG ROBUSTNESS:** 15–25 cells pass and median `D_R,D_A>0`.
- **PARTIAL ROBUSTNESS:** 10–14 cells pass and both medians are positive.
- **DIRECTION-ONLY:** fewer than 10 cells pass but both medians remain positive.
- **REVERSAL / FAILURE:** either aggregate median reverses.

Overall classification:

- **STRONG HETEROGENEOUS ROBUSTNESS:** at least five profiles are strong and no profile reverses either median.
- **HETEROGENEOUS ROBUSTNESS:** at least four profiles are strong/partial and no robust sign reversal occurs.
- **MIXED — ROLE/LEARNER DEPENDENT:** meaningful disagreements occur among ordered profiles.
- **HETEROGENEOUS FAILURE:** the conflict systematically collapses or reverses.

Role-swap quantities are `Gamma_R(X,Y)=D_R((X,Y))-D_R((Y,X))` and similarly for allocation. Report median effects, deterministic bootstrap 95% intervals, the share of environments whose gate changes, and any sign reversal caused by swapping roles.

Primary outcomes remain sealed until 9,000 unique, valid records exist with zero missing, duplicates, or corrupt outputs. The M8 theorem remains homogeneous-Hedge only.
