# Privacy and release audit

## Secret scan

Repository text was scanned for common API-key, token, password, private-key, bearer-token, personal-email, and absolute Windows user-path patterns. No credential or personal-path match was found in the tracked release material.

The Git configuration uses a non-personal invalid example address and is not manuscript author metadata.

## Historical recovery evidence

`docs/RECOVERY_STATUS.md` and the six root `work_level3_*` logs are local operational evidence. They are excluded by exact `.gitignore` entries and are not part of the public release. They remain on disk and were not deleted.

## Large files

The working directory is approximately 0.065 GiB. The largest tracked files are the Level-3 holdout and development seed tables (approximately 3.6 MB and 2.9 MB). Git contains code, compact tables, figures, certificates, and selected provenance data. For an archival deposit, large per-run collections should be compressed and accompanied by SHA-256 checksums rather than attached as tens of thousands of loose files.

## Release decision

- Git package: code, configs, protocols, compact results, selected seed tables, figures, manuscript, proofs, certificates, and checksums.
- Archival package: compressed raw Level-5 and heterogeneous run records plus the Git source archive.
- Excluded: recovery logs, caches, temporary renders, credentials, machine-specific paths, and the unopened mechanism holdout.

