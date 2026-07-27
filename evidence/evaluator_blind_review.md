# Evaluator-blind review — schema-v2 current-only candidate

Scope: only the schema-v2 active tree beginning at
`pages/current-verification/page.md` and the evaluator rubric were used.
Repository history, OpenResearch run directories, and historical logbook pages
were not used to fill evidence gaps.

Files opened:

1. `README.md`
2. `logbook.json`
3. `workspace.json`
4. `pages/current-verification/page.md`
5. `pages/current-c1/page.md` through `pages/current-c6/page.md`
6. `pages/current-release/page.md`
7. `repro/src/measure_theorem_signatures.py`
8. `repro/src/check_theorem_signatures.py`
9. `.openresearch/artifacts/reference_protocols/raw_output.json`
10. `.openresearch/artifacts/reference_protocols/checker_output.json`

Navigation audit:

- `schema_version` is 2 and the paper is identified by `arxiv_id`.
- The active tree contains no historical child and no rejected verifier.
- It contains exactly six claim pages and one reproducibility page.
- Historical files remain preserved and are reachable from the release page,
  but are outside automatic active-tree ingestion.

For every claim the reviewer could locate the exact official claim, theorem or
appendix anchor, assumptions, quantifiers, implemented protocol, native
executed-cell metadata, exact fixed command, exit code, duration, inline
executed source, machine output, measured-value table, raw JSON, independent
checker, negative control, seed, CPU allocation, limitations, and assessment.

Special checks:

- C5 documents the corrected `d+2p` substitution and rejecting extra-`d`
  mutation.
- C6 documents full-column-rank and nonnegative-weight proof scope.
- Every numeric theorem bound is compared with `log2(pattern count)`, not the
  raw count.
- No legacy 96-, 189-, 75-, 153-, or 300-case verifier appears in active
  navigation.

Conclusion: release visibility PASS; zero missing paths and zero missing
visibility-matrix cells. Repeat this review from a fresh downloaded additive
candidate and from the exact published revision.
