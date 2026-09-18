# Current submission requirements

Checked 2026-09-18. Journal portals can change without notice; the submitting author must re-open the official page immediately before upload. Elsevier and ACM returned anti-bot pages to automated retrieval during this audit, so items below distinguish stable publisher-wide requirements from portal items that require final visual confirmation.

## ACM Transactions on Economics and Computation (primary target)

Official sources:

- TEAC author guidelines: https://dl.acm.org/journal/teac/author-guidelines
- ACM journal submission workflow: https://authors.acm.org/journals/submitting-a-manuscript
- ACM LaTeX authoring: https://authors.acm.org/proceedings/production-information/accepted-latex-packages
- ACM artifact review and badging: https://www.acm.org/publications/policies/artifact-review-and-badging-current

Submission preparation:

- Use the current `acmart` class and the journal/manuscript option required by the TEAC portal. Source and bibliography must compile without nonstandard private dependencies.
- Submit a clean manuscript PDF and editable source. Author identity, conflict, ORCID, funding, and rights information belong in portal fields or the title page as instructed.
- ACM requires original work and disclosure of related submissions. A public preprint is generally compatible with ACM policy, but the author must identify it where the portal requests prior dissemination.
- Supplemental code/data can be submitted and may be evaluated under ACM artifact-review criteria. The repository should expose documented installation, exact commands, and immutable artifacts.
- No universal word limit was found in the accessible author guidance. Length must be justified by contribution; the expanded manuscript should remain concise and move implementation detail to the supplement.
- A cover letter is not a substitute for portal metadata but is useful to explain fit, prior dissemination, and the relationship between theory, computation, and negative design results.

Final portal checks: exact review anonymity mode, current `acmart` option, page-charge/open-access choices, required data availability field, and whether suggested reviewers are requested.

## Games and Economic Behavior (backup 1)

Official source:

- Guide for authors: https://www.sciencedirect.com/journal/games-and-economic-behavior/publish/guide-for-authors
- Elsevier research-data guidance: https://www.elsevier.com/researcher/author/policies-and-guidelines/research-data

Stable Elsevier preparation points:

- Initial submissions normally permit flexible formatting under “Your Paper Your Way,” provided the manuscript is readable, complete, and consistently referenced; editable source is required later.
- Journal portals commonly require a separate title page for anonymized review, declarations of interest, funding disclosures, a data/code availability statement, and separate supplementary files.
- Preprints are generally permitted under Elsevier sharing policy, but the author should disclose the preprint and link the accepted version according to the final agreement.
- Highlights may be requested by the submission system. A five-item highlights file is included in the package but should be uploaded only if the portal requests it.

Final portal checks: exact anonymization model, required highlights, cover-letter requirement, current file formats, and any article-type-specific length guidance.

## Journal of Economic Behavior & Organization (backup 2)

Official source:

- Guide for authors: https://www.sciencedirect.com/journal/journal-of-economic-behavior-and-organization/publish/guide-for-authors
- Elsevier research-data guidance: https://www.elsevier.com/researcher/author/policies-and-guidelines/research-data

Preparation follows the same publisher-wide principles: readable initial manuscript, editable source at revision, separate declarations and data availability, and clearly labeled supplementary materials. The behavioral framing must emphasize algorithmic delegation and heterogeneous adaptive behavior rather than present the study as a human-subject experiment.

Final portal checks: anonymization, highlights, word/page guidance, graphical-abstract status, and requested classification codes.

## arXiv and SSRN

Official arXiv sources:

- Submission help: https://info.arxiv.org/help/submit/index.html
- TeX submission: https://info.arxiv.org/help/submit_tex.html
- Endorsement: https://info.arxiv.org/help/endorsement.html
- Ancillary files: https://info.arxiv.org/help/ancillary_files.html

arXiv prefers TeX source when the paper is authored in TeX. Upload a self-contained source bundle with bibliography and figures, verify the generated PDF, select an appropriate category, and satisfy any account/endorsement requirement. Do not upload local paths, generated caches, or large raw data as ancillary files.

SSRN author guidance is available through its submission portal: https://www.ssrn.com/index.cfm/en/submit-paper/. SSRN is an alternative economics-facing preprint path. Neither service was used in this phase because authenticated upload was not authorized.

## Package decision

Primary target: **ACM Transactions on Economics and Computation**.  
Backup 1: **Games and Economic Behavior**.  
Backup 2: **Journal of Economic Behavior & Organization**.

The package includes an anonymous manuscript, separate title page, cover letter, highlights, declarations template, transparency/data statement, supplemental guide, and source bundle. Missing verified author metadata remains the only submission-package blocker.

