# Independent reproduction guide

## Scope

This guide separates fast proof/software checks from expensive campaign reproduction.

| Target | Procedure | Expected runtime |
|---|---|---:|
| Full unit/integration suite | `python -m pytest -q` | under 1 minute |
| M8 theorem | Run the committed M8 interval certifier and compare its JSON certificate | minutes to tens of minutes, machine dependent |
| M11 theorem | Run `certify(..., parts=10000)` from `m11_interval.py` | approximately 7--10 minutes on the reference laptop |
| Level-3 result | Validate committed manifests, paired rows, cell table, and frozen verdict; full rerun uses frozen runner | validation: minutes; full rerun: hours |
| Level-5 summary | Recompute analysis from 4,500 committed runs | minutes; full 144M-round rerun: hours |
| Heterogeneous summary | Recompute analysis from 9,000 committed runs | minutes; full 288M-round rerun: hours |

## Independence checklist

1. Clone into a new directory and create a fresh virtual environment.
2. Record Python and dependency versions.
3. Verify protocol/config hashes before inspecting outcomes.
4. Run the test suite.
5. Regenerate M8 and M11 certificates without altering their committed inputs.
6. Recompute compact summaries from committed run records.
7. Compare counts, hashes, confidence intervals, and classifications with the status files.
8. Report deviations rather than modifying thresholds.

No external reproduction or proof review has yet been claimed.

