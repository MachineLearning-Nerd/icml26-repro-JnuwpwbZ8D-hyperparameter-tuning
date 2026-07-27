# Evaluator-blind pre-publication review

Candidate lineage: the live-judged published predecessor is
`01db7fab41d2c338894316b6e83cbc0cede75756`; the winning correction is
`orx/inline-executed-claim-verifiers` at
`965d3915a574ab325f1411e4811cddd121ccead7`.
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

## Live-judge failure of the link-only audit

That conclusion was too optimistic. The live evaluator judged the intended
Space revision `01db7fab41d2c338894316b6e83cbc0cede75756` at
`2026-07-27T02:21:22+00:00` and retained all six TOY verdicts. For every claim,
it found the stronger measurements described on the CURRENT page but stated
that their code was not shown in the logbook and that the executed publication
gate did not run them.

The failure was in this audit: it marked `code_visible: true` when a claim page
contained a source link. That does not meet the evaluator-visible evidence
standard. The audit has been replaced with a stricter check that requires:

1. a Python fence inline on every current claim page;
2. byte-for-byte equality between that fence and the claim functions in the
   source actually executed by the gate;
3. the exact stable `CLAIM_RESULT_C*` JSON emitted during execution;
4. the exact full publication-gate source inline on the CURRENT release page;
5. explicit `GATE_STAGE_START` and `GATE_STAGE_PASS` records for the empirical
   measurement and independent-checker stages.

The unchanged toy pages are now nested beneath one **Historical rejected
baseline — archive** node instead of appearing as twelve peers of the current
verifiers. They remain reachable and byte-identical.

## Repeated evaluator-blind review after the live failure

Starting only from `README.md`, `logbook.json`, and the canonical current root,
the reviewer first encounters the six CURRENT claims and CURRENT gate page. On
each claim page it can read the executable claim function and captured result
without following a source link. The CURRENT gate page shows that
`run_publication_gate.py` executes `measure_theorem_signatures.py`, then passes
the generated JSON to `check_theorem_signatures.py`, with `check=True` on both
processes. The historical toy code is one level below the explicit archive
warning.

Reviewer conclusion: the specific visibility defect cited by the live judge is
resolved in the candidate. Scientific verdicts remain unchanged; this is an
evaluator-surface correction, not a claim that the score has increased.

The fresh-clone formal run
`4d4a3555-a313-4b8d-b38a-c191809d01d6` independently repeated that traversal.
It reported `VERBATIM_EXECUTED_SOURCE_INLINE` for C1–C6, zero missing cells,
118 verified candidate hashes, 19 preserved historical assets, and 18 passing
tests. A negative unit test also confirms that a link-only claim page is
rejected as not code-visible.

The first literal Space download then failed closed because the audit resolved
historical hashes only through the repository-internal `.trackio/logbook`
mirror, which is not part of the text upload. The public historical pages were
present and unchanged. The final audit resolves the mirror when available and
otherwise verifies the actual published root path against the same immutable
hash. Its dedicated test exercises both layouts; the post-overlay audit must
pass before upload.

## Second live-judge failure: empirical code was not the proof certificate

The next live evaluation inspected Space revision
`e41343cf30154ab7e49464ce303fc5ed1b56ea05` at
`2026-07-27T04:11:17+00:00` and again retained `6/12`. The evaluator now found
the exact finite sign-pattern code and outputs. Its new, repeated reason for
TOY was that `verify_claim1_proof.py` and `verify_claims2_6_proofs.py` were
only referenced and their SymPy certificates were not embedded.

That exposes a second false-positive in the visibility audit: byte-matching the
finite experiment source did not establish visibility of the distinct
theorem-level route. The replacement audit now requires, on every claim page:

1. the complete applicable symbolic program, not a function excerpt;
2. byte-for-byte equality with the source executed by the fixed gate;
3. the exact `CLAIM1_RESULT` or `CLAIMS2_6_RESULT` line;
4. symbolic-stage start and pass records; and
5. a root-level page containing both complete programs and the C1–C6 mapping.

A negative unit test constructs an empirical-only page and requires the
symbolic visibility check to reject it. The repeated blind review must open the
new root proof page and all six claim pages before release.

## Repeated review with complete proof programs

Run `1680d0f0-1dff-40e4-8b11-615b842b0dfa` at
`1355f08b57162f46805ef86287774fc677c4b73a` performed that repeated traversal.
Starting from the canonical root, it opened all six current claim pages and
`pages/current-proof-certificates/page.md`. For C1 it byte-matched the complete
120-line certificate; for C2–C6 it byte-matched the complete 203-line shared
certificate on every applicable page. It located the exact symbolic output and
stage-pass record for all claims. The audit reported
`FULL_EXECUTED_EMPIRICAL_AND_SYMBOLIC_SOURCE_INLINE`, zero missing cells, 120
verified non-self hashes, 19 preserved historical assets, and a passing secret
scan. All 21 unit tests passed, including the empirical-only rejection.
