# Level 3 holdout recovery protocol

Recovery authorization date: 2026-09-16. The failed first holdout attempt produced no durable rows. This recovery run is explicitly authorized to recompute the unchanged frozen holdout; it does not reopen development, falsification, candidate selection, or tuning.

## Frozen inputs

- Primary-candidate freeze: commit `241577f`.
- Holdout grid: `configs/level_03/holdout/grid.json`.
- Frozen grid SHA-256: `5b65a1c9ee21e89484b93c43df5706ed35138c67be84234d75d7deffea6d4729`.
- Seeds: 2000--2029, paired between FPA and SPA.
- Expected paired units: 2,250; expected mechanism-level rows: 4,500.

## Failure diagnosis

The preserved traceback ends in `BrokenProcessPool`: one of 12 worker processes terminated abruptly. It contains no worker-side Python exception, so the exact external cause cannot be recovered. The original runner submitted mechanism-level tasks, accumulated every result in `list(pool.map(...))`, and wrote output only after all 4,500 tasks returned. A single vanished worker therefore destroyed the pool and left zero auditable rows even if other tasks had completed in memory.

## Recovery execution rule

The resumable runner treats one seed/environment configuration as a paired unit containing exactly one FPA and one SPA row. Its pair ID is a deterministic hash of valuation, horizon, both rate factors, bid step, tail share, and seed. Each completed pair is written through a flushed temporary file and atomically renamed. The checkpoint is also atomically replaced after every pair.

Reruns validate existing pair files and skip completed IDs. Work is assigned only up to the worker limit at a time. If a process pool breaks, the parent records the failure, reconstructs the pending set from durable completions, creates a fresh pool, and continues. Deterministic index-based sharding is available through `--shard-index` and `--shard-count`.

The powered run must use the committed repair, conservative workers, and the unchanged grid. A small `--max-pairs` invocation is a smoke shard whose valid rows remain part of the powered dataset; the subsequent full invocation idempotently skips them.
