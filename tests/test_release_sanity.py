import json
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "check_release_sanity.py"
SPEC = importlib.util.spec_from_file_location("check_release_sanity", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
release_sanity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_sanity)

EXPECTED_WITNESS = release_sanity.EXPECTED_WITNESS
check_certificate = release_sanity.check_certificate
check_manuscript_text = release_sanity.check_manuscript_text


def section(statement: str) -> str:
    return f"# Paper\n\n## 10. Design limitation\n\n{statement}\n\n## 11. Discussion\n"


def test_canonical_release_artifacts_pass():
    check_certificate(Path("results/m11/constant_alpha_certificate.json"))
    check_manuscript_text(Path("paper/manuscript.md").read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "statement",
    [
        r"values ((1,1/3)), $\eta_H=4$, $\eta_L=0$, and $H=9$.",
        r"values \left((1,\frac{1}{3})\right), \eta_H = 4, \eta_L = 0, H = 9.",
        r"values \left((1,\frac13)\right), \eta_H=4, \eta_L=0, H=9.",
    ],
)
def test_harmless_latex_formatting_passes(statement):
    check_manuscript_text(section(statement))


def test_wrong_eta_low_witness_fails():
    bad = section(r"values ((1,1/3)), $\eta_H=4$, $\eta_L=0.9$, and $H=9$.")
    with pytest.raises(AssertionError, match="eta_L=0.9"):
        check_manuscript_text(bad)


def test_certificate_witness_mismatch_fails(tmp_path):
    artifact = tmp_path / "certificate.json"
    wrong = {"witness": {**EXPECTED_WITNESS, "eta_low": "0.9"}, "certified": True}
    artifact.write_text(json.dumps(wrong), encoding="utf-8")
    with pytest.raises(AssertionError, match="certificate witness mismatch"):
        check_certificate(artifact)
