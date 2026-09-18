"""Build the compact, table-reproduction archive without rerunning campaigns."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release" / "compact-data"

SOURCES = [
    "configs",
    "results/level_03/holdout/analysis",
    "results/level_05/analysis",
    "results/heterogeneous/analysis",
    "results/m8",
    "results/m9/development/analysis",
    "results/m10/development/analysis",
    "results/m11",
    "docs/FINAL_CLAIM_REGISTRY.md",
    "RESULTS_INDEX.md",
]


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    copied: list[Path] = []
    for rel in SOURCES:
        src = ROOT / rel
        if not src.exists():
            continue
        dst = OUT / rel
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("runs", "raw", "*.tmp", "*.log", "__pycache__"))
            copied.extend(p for p in dst.rglob("*") if p.is_file())
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst); copied.append(dst)
    rows = []
    for path in sorted(copied):
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(OUT).as_posix()}")
    (OUT / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Compact reproduction data\n\nProcessed evidence sufficient to regenerate reported tables, figures, and certificates without rerunning powered campaigns. See the repository claim registry for scope.\n",
        encoding="utf-8",
    )
    print(f"{len(copied)} files -> {OUT}")


if __name__ == "__main__":
    main()
