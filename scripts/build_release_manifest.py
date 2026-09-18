"""Write checksums for the public v1.1.1 release attachments."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "paper/delegation-proof-market-design.pdf",
    ROOT / "release/delegation-proof-market-design-source-v1.1.1.zip",
    ROOT / "release/delegation-proof-market-design-compact-data-v1.1.1.zip",
    ROOT / "release/SHA256SUMS.txt",
    ROOT / "preprint/arxiv/source-v1.1.1.zip",
    ROOT / "submission/acm-teac/anonymous-manuscript.pdf",
]


def main() -> None:
    rows = []
    for path in FILES:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    output = ROOT / "release/RELEASE_SHA256SUMS_v1.1.1.txt"
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
