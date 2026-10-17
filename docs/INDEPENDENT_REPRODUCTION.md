# Independently evaluate the bounded auction laboratory

For computational economics researchers and research software engineers: inspect a small auction example, deliberate rejections and a fixed finite-model interval certificate. This supplements the existing [proof-review packet](EXTERNAL_PROOF_REVIEW_PACKET.md); it is not a new research result or evidence of independent review.

## Environment and source

This proposed `m3/reviewer-ready` branch starts from main `5c2cf7abff4aa044d5911e86ab8c908aa80e9c73`. Record actual HEAD. For a delivered reviewer package, use its exact source commit rather than silently replacing it with latest main. Python 3.11 is the reference runtime; Windows Python 3.12.14 was additionally verified. Ubuntu 3.11 is covered by current project CI; macOS is not newly qualified. Git and package-registry access are required initially. No model key or paid service is needed.

```powershell
git clone https://github.com/Aayush-Kadam/delegation-proof-market-design.git
cd delegation-proof-market-design
git checkout m3/reviewer-ready
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
.venv/Scripts/python.exe -m pip install --no-deps -e .
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe scripts/reviewer_check.py
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe scripts/reviewer_check.py --full
git rev-parse HEAD
.venv/Scripts/python.exe -m pip freeze
```

On Ubuntu use `python3.11 -m venv .venv` and `.venv/bin/python`. On Windows use `py -3.11` if that reference interpreter is installed. The lock pins direct dependencies, not every transitive package; save the actual environment. It includes optional dashboard packages although the evaluation needs no dashboard. Cold cloning/installation has no five-minute guarantee: the repository contains about 29,000 tracked entries. Author observation on one Windows machine: 72 tests took 17.68s and the complete interval calculation took 385.052s after installation. Hardware/load can change this; it is not a performance promise.

## Expected output and deliberate failures

The quick procedure must exit zero with first_price=0.8, second_price=0.2, negative_bid_rejected=true and altered_witness_rejected=true. It checks the committed certificate record and labels mode **COMMITTED_RECORD_CHECK_ONLY**. It does not recompute a proof. The `--full` procedure must instead report **RECOMPUTED_10000_INTERVALS**, alpha_subintervals=10000, certified=true and all six certificate predicates true. It writes only temporary output; the canonical certificate is not overwritten.

The negative cases exercise actual invalid-bid rejection and rejection of the known wrong witness eta_low=0.9. The witness/flag sanity check is not a cryptographic or general mathematical proof checker. Full reproduction reruns this project's interval implementation; independent proof validation also requires inspecting directed rounding, payoff matrices, dual differentiation and assumptions in the existing packet.

Save complete stdout/stderr, exit codes, source and environment, including failures. Full test discovery includes the existing negative-case regressions. The current CI additionally runs quick and full reviewer procedures; an earlier 50-part CI smoke calculation alone does not establish the 10,000-part result.

## Scope, prior art and measurement

The witness fixes values (1,1/3), Hedge rates (4,0), horizon nine and finite actions. It is not a theorem for all auction formats, learners or parameters. [Claim registry](FINAL_CLAIM_REGISTRY.md) and the proof packet preserve 29 heterogeneous revenue reversals, two failed repair families, and 109/1500 sampled monotonicity counterexamples. The unused M9 mechanism holdout must remain unopened; do not run powered campaigns for this evaluation.

Auction-learning research predates this project; see the manuscript references, including Kolumbus/Nisan's Auctions Between Regret-Minimizing Agents. Gambit already analyzes finite games/equilibria. The evaluation concerns scoped reproducibility and usefulness of this laboratory, not first-ever adaptive bidding, a new general solver, a speed advantage or an originality certificate. Existing runtime observations are author measurements, not an external benchmark.

## Permissions, privacy and feedback

The exact [LICENSE](../LICENSE) grants use, copying, modification, merging, publication, redistribution, sublicensing and sale subject to preserving its copyright and permission notice. Its disclaimer is shortened; it is not byte-identical standard MIT and GitHub reports NOASSERTION. No license is changed by this review branch. External referenced material and dependency rights remain separate; ownership is not established by an author badge.

Use synthetic inputs in an isolated environment. This local research code has no production security certification. Submit a [normal issue](https://github.com/Aayush-Kadam/delegation-proof-market-design/issues/new) using the included reproduction template fields. If the template is not yet on default main, copy those fields into a blank issue. Include installation problems, failed results, claim corrections, feature requests and a concrete task where the tool helps or fails to help. Disclose author assistance/affiliation. Do not post secrets, home paths, private research data or confidential correspondence. Identity/quotation in an evidence ledger requires permission; a private channel must be agreed separately. Negative reports are welcome. Author tests and prepared packets never count as independent external validation.
