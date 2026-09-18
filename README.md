# Delegation-Proof Market Design

**Aayush Kadam**

**Research question.** What happens to standard auction rankings when bidders delegate repeated bidding decisions to adaptive algorithms?

**Main result.** Across prospectively frozen finite-horizon studies, first-price auctions tend to protect seller revenue while second-price auctions tend to protect efficient allocation and welfare. The pattern survives Hedge, FTPL, regret matching, and ordered heterogeneous learner pairs, although heterogeneous high-valuation cells include 29 revenue-ranking reversals. Exact Hedge results explain the conflict on finite-action parameter regions. Two natural mechanism repairs fail unchanged prospective gates, and a scoped certificate proves incompatible constant-hybrid safety requirements in one explicit environment.

No successful delegation-proof mechanism, universal impossibility, heterogeneous-learning theorem, or external independent replication is claimed.

## Paper and evidence

- Public repository: https://github.com/Aayush-Kadam/delegation-proof-market-design
- Manuscript: `paper/delegation-proof-market-design.pdf`
- Claim registry: `docs/FINAL_CLAIM_REGISTRY.md`
- Result index: `RESULTS_INDEX.md`
- Transparency statement: `docs/RESEARCH_TRANSPARENCY_STATEMENT.md`
- Reproduction guide: `REPRODUCIBILITY.md`
- Submission requirements and journal fit: `docs/CURRENT_SUBMISSION_REQUIREMENTS.md`

## Theorem summary

For deterministic full-information Hedge, explicit closed parameter rectangles yield higher FPA revenue and higher SPA allocation/welfare for finite horizons. The result survives a richer 4x3 action model. Separately, at `(v, eta_H, eta_L, H) = (1/3, 4, 0, 9)`, outward interval arithmetic certifies that revenue rises and allocation falls along the entire constant FPA/SPA interpolation; midpoint safety requires simultaneously `alpha > .36` and `alpha < .22`, which is impossible. These statements are deliberately scoped.

## Quick verification

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-lock.txt
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m pytest -q
.venv\Scripts\python scripts/build_release_artifacts.py
```

On POSIX systems use `.venv/bin/python`. The quick path reads compact committed evidence and does not rerun powered campaigns or open the unused mechanism holdout.

## Repository map

- `src/delegation_market/`: mechanisms, learners, runners, theory, certificates
- `configs/`: frozen scientific configurations and manifests
- `docs/`: protocols, proofs, status reports, audits, claim registry
- `results/`: compact evidence, certificates, figures, and campaign records
- `paper/`: manuscript, bibliography, publication figures
- `release/`: checksums and compact archival package
- `site/`: static academic project website
- `submission/`: journal submission materials
- `tests/`: software and mathematical regression tests

## Reproducibility status

Tier 1 verifies software and theorem certificates; Tier 2 regenerates paper tables, figures, and the manuscript from compact evidence; Tier 3 reruns the large checkpointed campaigns. See `REPRODUCIBILITY.md` for scope, runtime, and storage expectations. Internal clean-room reproduction is documented separately and is not represented as independent external replication.

## Citation

Suggested citation: **Aayush Kadam. _Delegation-Proof Market Design: Revenue–Allocation Tradeoffs under Adaptive Bidding_, v1.1.1.** Use `CITATION.cff` for machine-readable metadata. Affiliation, ORCID, and correspondence details remain explicit placeholders until verified.

## License and boundaries

See `LICENSE`. The unused mechanism holdout remains unopened. Historical recovery logs, credentials, and machine-local artifacts are excluded from the public package.
