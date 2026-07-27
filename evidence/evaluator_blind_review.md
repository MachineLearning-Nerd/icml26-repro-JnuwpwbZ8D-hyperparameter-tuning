# Evaluator-blind pre-publication review

Candidate lineage: the immutable published predecessor is
`8fa3b003ec2081f5c84a2e453c9c76fb4bc9d63a`; the correction is the child
`orx/empirical-theorem-signature-release`.
Candidate construction: a fresh clone of the child was overlaid, using the
planned text-only upload set, onto the immutable judged Space revision
`a928c531f0d7b6784a4bfa3e7944bf0e20a49b26`.

The reviewer was given only the candidate directory and the evaluator rubric.
Traversal began at `README.md`, `logbook.json`, and the root file named by
`logbook.json`; no OpenResearch run database, worktree path, or unpublished
branch was used to fill gaps.

## First pass

Files opened, in order:

1. `README.md`
2. `logbook.json`
3. `pages/current-verification/page.md`
4. `pages/current-c1/page.md` through `pages/current-c6/page.md`
5. `pages/current-release/page.md`
6. all 12 historical pages reachable from navigation
7. the six report SVGs, `reports/theorem-certificates/report.md`,
   `notebooks/theorem_certificates.py`, and `uv.lock`
8. every contract, raw JSON, checker output, control, proof certificate,
   falsification route, limitation, and linked verifier source
9. `evidence/judged-space-a928c531.sha256` and
   `evidence/run_metadata.json`

Conclusions: all six current verifiers and verdicts were locatable; every
visibility-matrix scientific cell was complete. Exactly three release-control
links were missing because their files had not yet been generated:
`evidence/evaluator_blind_review.md`,
`evidence/hf_upload_allowlist.txt`, and
`evidence/candidate_text_manifest.sha256`.

## Fix and repeated pass

The three release-control files were added. The same root-only traversal was
then repeated against a fresh candidate overlay. It opened all previously
listed files plus those three controls, reported zero missing paths, and found
all required C1–C6 fields: exact statement, assumptions, command, inline data,
raw data, verifier, checker, negative control, limitation, and verdict.

Reviewer conclusion: **release visibility PASS**, subject to the final formal
gate and post-upload hash/traversal repetition. C6's negative-weight
proof-domain risk remained visible and was not reclassified as falsification.

## Corrective empirical-signature pass

After the live comparison with the public 12/12 artifact, the blind reviewer
was restarted from the same three canonical entrypoints without being told
where the new evidence lived. For every claim it located the empirical
verifier, independent checker, per-claim raw JSON, inline pattern/region
counts, fixed formula-independent budgets, three seeds, scaling sweep, and
failing applicability control. It also opened the new signature figure and
confirmed that the pages distinguish finite corroboration from the symbolic
universal proof. No cell in the visibility matrix was missing. The result
remains **release visibility PASS**.
