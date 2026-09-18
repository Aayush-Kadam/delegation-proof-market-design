# Reproducibility

## Environment

Python 3.11 or later is recommended.

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-lock.txt
.venv\Scripts\python -m pip install -e .
```

On POSIX systems use `.venv/bin/python` instead.

## Fast validation

```text
python -m pytest -q
```

Expected release result: 66 passing tests.

## Key theorem certificate

The committed M11 certificate is `results/m11/constant_alpha_certificate.json`. Regeneration is deterministic but CPU intensive:

```text
python -c "from pathlib import Path; from delegation_market.m11_interval import certify; certify(Path('results/m11/constant_alpha_certificate.json'))"
```

This evaluates 10,000 outward-rounded alpha subintervals. The certified witness is `(v,eta_H,eta_L,H)=(1/3,4,0,9)`.

## Main tables and figures

Compact canonical summaries are already committed under each `results/*/analysis` directory. Rebuild publication figures and the manuscript with:

```text
python scripts/build_release_artifacts.py
```

The command reads committed compact results; it does not rerun powered campaigns or open the unused mechanism holdout.

## Powered campaigns

The Level-3, Level-5, and heterogeneous runners are checkpointed and deterministic-ID based. Full powered reruns are intentionally not part of the quick path: they comprise hundreds of millions of logical auction rounds. Frozen protocols, hashes, seeds, environments, and commands are documented in `docs/LEVEL_3_STATUS.md`, `docs/level_05_protocol.md`, and `docs/heterogeneous_learner_protocol.md`.

## Evidence hierarchy

Use `docs/FINAL_CLAIM_REGISTRY.md` for paper wording, `RESULTS_INDEX.md` for artifact locations, and the phase status documents for full audit trails. Development and holdout evidence must never be pooled.

