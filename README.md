# Delegation-Proof Market Design

## Question

What survives when participants outsource repeated auction decisions to adaptive algorithms?

This repository is an auditable research laboratory, not a claim that the problem has been solved. It separates prior results, replications, computational findings, and proved statements. The current release implements fixed-value repeated single-item auctions and baseline learners; it does **not** claim a novel mechanism or theorem.

## Current contribution

- A deterministic simulator for first-price, second-price, reserve, hybrid-payment, and all-pay auctions.
- Truthful, symmetric-IPV equilibrium, Hedge, EXP3, tabular Q-learning, and UCB agents behind a common interface.
- Separate welfare, efficiency, revenue, surplus, shading, and win-share metrics.
- A source-backed novelty audit showing direct overlap with learning-in-auctions and autobidding research.
- Smoke experiments and tests intended to prevent accounting and mechanism errors.

## Quickstart

```bash
python -m venv .venv
python -m pip install -e ".[test,dashboard]"
pytest -q
python -m delegation_market.experiments --quick
streamlit run dashboard/app.py
```

Outputs are written to `results/processed/` and `results/tables/`.

## Evidence status

See `docs/result_registry.md`. No result becomes a project claim merely because the simulator emits it.

Historical Level 2 remains **MIXED** (V1 FAIL; V2 FAIL). The separate M2.5 finite-horizon simulator validation is **CERTIFIED** within the bounded domain in `docs/level_3_readiness.md`; asymptotic last-iterate convergence remains unvalidated.

## Repository map

- `src/delegation_market/`: mechanisms, learners, metrics, simulation, experiment runner
- `docs/`: research specification, literature map, novelty and protocols
- `configs/`: frozen machine-readable experiment settings
- `tests/`: mechanism, accounting, and reproducibility tests
- `dashboard/`: local research interface
- `paper/`: conservative manuscript scaffold

## Limitations

Current simulations use fixed values and discrete bids. Hedge receives full-information counterfactual rewards; bandit agents receive realized reward. Regret and coordination diagnostics are not yet sufficient for strong claims. Deep-RL and LLM agents, frozen holdout evaluation, a candidate robust mechanism, and formal theory are not yet completed.

## Citation

Use `CITATION.cff`. This is a pre-research software release, not a peer-reviewed result.
