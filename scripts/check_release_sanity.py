"""Semantic release checks for the canonical M11 design-limitation witness."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

EXPECTED_WITNESS = {"v": "1/3", "eta_high": "4", "eta_low": "0", "H": 9}


def check_certificate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    witness = data.get("witness")
    if witness != EXPECTED_WITNESS:
        raise AssertionError(f"M11 certificate witness mismatch: {witness!r}")
    if data.get("certified") is not True:
        raise AssertionError("M11 certificate is not marked certified")


def design_limitation_section(manuscript: str) -> str:
    match = re.search(
        r"^##\s+\d+\.\s+Design limitation\s*$([\s\S]*?)(?=^##\s+\d+\.|\Z)",
        manuscript,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        raise AssertionError("M11 design-limitation section not found")
    return match.group(1)


def normalize_math(text: str) -> str:
    normalized = text.lower()
    normalized = re.sub(r"\\(?:left|right)", "", normalized)
    normalized = re.sub(r"\\frac\s*\{?1\}?\s*\{?3\}?", "1/3", normalized)
    normalized = normalized.replace("\\eta", "eta")
    normalized = re.sub(r"[\s{}$]", "", normalized)
    return normalized


def check_manuscript_text(manuscript: str) -> None:
    section = normalize_math(design_limitation_section(manuscript))
    if re.search(r"eta_l=(?:0?\.9|9/10)(?:[^0-9]|$)", section):
        raise AssertionError("Known erroneous M11 witness eta_L=0.9 found")
    required = {
        "low value v=1/3": "values((1,1/3))",
        "eta_H=4": "eta_h=4",
        "eta_L=0": "eta_l=0",
        "H=9": "h=9",
    }
    missing = [label for label, token in required.items() if token not in section]
    if missing:
        raise AssertionError("M11 manuscript witness mismatch; missing " + ", ".join(missing))


def check_manuscript(path: Path) -> None:
    check_manuscript_text(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path("results/m11/constant_alpha_certificate.json"))
    parser.add_argument("--manuscript", type=Path, default=Path("paper/manuscript.md"))
    args = parser.parse_args()
    check_certificate(args.certificate)
    check_manuscript(args.manuscript)
    print("Release sanity PASS: canonical M11 witness is (v, eta_H, eta_L, H)=(1/3, 4, 0, 9).")


if __name__ == "__main__":
    main()
