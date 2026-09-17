# Level 5 limited falsification addendum

Frozen after the complete primary table established eligibility for the protocol's limited-falsification clause, and before any falsification run.

- Learners: FTPL and regret matching only.
- Mechanisms: FPA and SPA, paired.
- Independent seeds: `4000,...,4009`.
- Baseline: `(v=.50, H=25000, c_H=1, c_L=.5)`.
- Nearby parameter attack: change only `v` to `.55`.
- Horizon attack: change only `H` to `50000`.
- Total: 120 mechanism runs and 4,000,000 logical auction rounds.
- The original cell gate is applied to each learner/attack: `D_R/v >= .05`, `D_A >= .01`, and paired normal 95% CI lower endpoints for raw `D_R` and `D_A` exceed zero.
- This addendum does not modify or enter the 4,500-run primary analysis.
