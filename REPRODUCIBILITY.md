# Reproducibility

Python 3.11 is the reference runtime. Install from the deterministic lock file:

```text
python -m venv .venv
.venv\Scripts\python -m pip install --no-cache-dir -r requirements-lock.txt
.venv\Scripts\python -m pip install --no-cache-dir -e .
```

Use `.venv/bin/python` on POSIX systems.

## Tier 1 — quick verification

Target: under 10 minutes on a recent four-core laptop after dependency installation.

```text
python -m pytest -q
python -c "from pathlib import Path; from delegation_market.m11_interval import certify; certify(Path('results/m11/constant_alpha_certificate.json'))"
python scripts/build_release_artifacts.py
```

The M11 command deterministically evaluates 10,000 outward-rounded alpha subintervals for `(v,eta_H,eta_L,H)=(1/3,4,0,9)`. It overwrites only the same certificate artifact. Expected workspace growth is below 100 MB beyond dependencies.

## Tier 2 — core paper reproduction

Tier 2 regenerates all reported compact summaries, paper figures, checksums, and the manuscript from committed records. It does not repeat the auction campaigns.

```text
python -m delegation_market.level3_holdout_final --input results/level_03/holdout/analysis/paired_cell_summary.csv --output results/level_03/holdout/analysis
python -m delegation_market.level5_analysis --root .
python -m delegation_market.heterogeneous_analysis --root .
python scripts/build_release_artifacts.py
python scripts/build_compact_archive.py
```

These commands are checked by the clean-room report. Target runtime is under 30 minutes and additional storage under 1 GB.

## Tier 3 — full simulation reproduction

Tier 3 reruns the checkpointed Level-3, Level-5, and heterogeneous campaigns from frozen manifests. Together they represent hundreds of millions of logical auction rounds. The runners assign deterministic IDs, persist each completed record atomically, validate identity hashes, and skip valid completed IDs when resumed.

Plan for many hours to days depending on CPU, at least 20 GB of free local storage, and four stable workers unless a frozen protocol says otherwise. Exact seeds, environments, horizons, mechanisms, hashes, and runner commands are recorded in `docs/LEVEL_3_STATUS.md`, `docs/level_05_protocol.md`, and `docs/heterogeneous_learner_protocol.md`. Tier 3 is intentionally excluded from ordinary CI.

## Evidence hierarchy

`docs/FINAL_CLAIM_REGISTRY.md` controls scientific wording. `RESULTS_INDEX.md` maps claims to artifacts. Development and holdout evidence must not be pooled. The M9 mechanism holdout must remain unopened because neither candidate passed development.

## Portable environment

`Dockerfile` provides a minimal Python 3.11 environment for Tier 1. It does not bundle large raw campaigns. The lock file records exact Python package versions used for the release.
