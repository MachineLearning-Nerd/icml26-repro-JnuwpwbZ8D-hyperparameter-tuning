# Evaluator-blind review — reference-protocol candidate

Scope: only files reachable from `pages/current-verification/page.md` and the
rubric were used. Repository history and OpenResearch run directories were not
used to fill gaps.

Files opened:

1. `README.md`
2. `logbook.json`
3. `pages/current-verification/page.md`
4. `pages/current-c1/page.md` through `pages/current-c6/page.md`
5. `pages/current-release/page.md`
6. `repro/src/measure_theorem_signatures.py`
7. `repro/src/check_theorem_signatures.py`
8. `.openresearch/artifacts/reference_protocols/raw_output.json`
9. `.openresearch/artifacts/reference_protocols/checker_output.json`
10. `pages/historical-rejected-baseline/page.md`

For every claim the reviewer could locate the exact claim, theorem/appendix
anchor, assumptions, quantifiers, implemented protocol, inline source segment,
exact machine output, raw JSON, checker, negative control, fixed command,
seed, CPU allocation, runtime, limitations, and historical supersession.

Special checks:

- C5 documents the erroneous prior extra-d factor and the rejecting mutation.
- C6 documents full-column-rank and nonnegative-weight scope.
- Every numeric theorem bound is compared with log2(pattern count), not the
  raw count.
- Current navigation does not present the rejected symbolic page as current.
- All raw links resolve inside the candidate.

Conclusion: release visibility PASS; zero missing paths and zero missing
visibility-matrix cells. Repeat this review from a fresh downloaded candidate
after the cumulative run and again after upload.
