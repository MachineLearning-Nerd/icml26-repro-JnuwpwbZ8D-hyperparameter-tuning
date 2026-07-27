# CURRENT — Release evidence and visibility

## Reproduction contract

- Python: 3.12.11, selected by `.python-version`
- Manager: `uv`; lockfile: `uv.lock`
- Exact fixed command:
  `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`
- Seeds: proof checks are deterministic; empirical checks use `173,271,419`
- Winning scientific SHA: `177668a1312bde3215e9778b2cc43f51dabd8a21`
- Winning run: `480450c8-f8f1-4f6f-ad74-21b4dc490ab0`
- Empirical stage runtime: 2.953 seconds, local CPU, one Python process on a host exposing 8 logical CPUs
- Hugging Face `cpu-upgrade`: not used; every formal task was confidently under five minutes and single-core
- Recorded formal CPU runtime through the measurement preflight: 90 seconds across nine runs, including two fail-closed fixture/manifest checks
- Compute cost: $0 local; $0 Hugging Face

## Fail-closed behavior

The current gate runs the historical regression suite, C1 symbolic certificate,
C1 falsification audit, C2–C6 symbolic/specialization certificates, the
C2–C6 adversarial audit, six concrete theorem-signature experiments, an
independent signature checker, and 16 unit tests. It exits nonzero on any mismatch.
The negative controls reject a missing `p²` term, source-index mutations,
finite-grid proxy evidence, missing bilevel existential structure, nonunique
paths, a signed norm lift, an invalid negative-radius dual box, a circular
sample budget, and a missing `p=d-1` factor.

## Historical safety and red team

The immutable judged revision is
`a928c531f0d7b6784a4bfa3e7944bf0e20a49b26`. Its 23-file SHA-256 manifest is
[here](../../evidence/judged-space-a928c531.sha256). The candidate changes no
historical claim page or asset; the old file set is a subset of the candidate
tree. Navigation labels every old page **Historical rejected baseline** and
places current verification first.

The evaluator-blind audit starts only at `README.md`, `logbook.json`, and this
index. It records every opened page and treats unlinked evidence as missing.
Its report and exact upload allowlist are linked below:

- [Blind traversal record](../../evidence/evaluator_blind_review.md)
- [Final release report](../../evidence/release_report.md)
- [Text upload allowlist](../../evidence/hf_upload_allowlist.txt)
- [Candidate SHA-256 manifest](../../evidence/candidate_text_manifest.sha256)
- [Run metadata](../../evidence/run_metadata.json)
- [Empirical raw output](../../.openresearch/artifacts/theorem_signatures/raw_output.json)
- [Independent empirical checker](../../.openresearch/artifacts/theorem_signatures/checker_output.json)

## Remaining limitation

C6's box-constrained dual proof requires `alpha_i >= 0`. The main text calls
the coordinates regularization weights but also typesets `alpha in R^p`.
For `A=I`, `b=0`, `d=2`, and `alpha=-2`, the primal problem has two global
minimizers `(-2,2)` and `(2,-2)`, both with value `-4`. This defeats the cited
unique-path route but is not an asymptotic pseudo-dimension counterexample.
