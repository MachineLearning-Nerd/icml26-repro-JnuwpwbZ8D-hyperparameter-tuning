# Outcome-blind review — exact boundary candidate

Review inputs were limited to the exact current challenge prompt and source
anchors, the candidate logbook tree, linked raw artifacts, the two executable
implementations, and the preserved proof objects. Working notes, desired
scores, and publication forecasts were excluded.

Files opened:

1. `README.md`, `logbook.json`, and `workspace.json`
2. `pages/universal-proof-index/page.md`
3. `pages/executive-summary/page.md` and `poster_embed.html`
4. `pages/universal-proof-c1/page.md` through `universal-proof-c6/page.md`
5. `pages/universal-proof-release/page.md`
6. `repro/src/audit_log_boundary_counterexamples.py`
7. `repro/src/check_log_boundary_counterexamples.py`
8. `.openresearch/artifacts/log_boundary_counterexamples/raw_output.json`
9. `.openresearch/artifacts/log_boundary_counterexamples/independent_check.json`
10. the six retained universal proof objects and their independent audit

## Claim scores

| Claim | Score | Evidence-only finding |
| --- | ---: | --- |
| C1 | 2/2 | The one-atom, degree-one FOL satisfies the literal assumptions; the universal coordinate identity proves `Pdim>=p` while both printed logs vanish. Source, raw result, code, independent checker, and guarded control are complete. |
| C2 | 1/2 | The retained proof-chain audit is useful and source-exact, but it treats quantifier elimination and Goldberg--Jerrum as trusted dependencies rather than independently reproducing the complete universal theorem. |
| C3 | 1/2 | The quantified reduction and atom counts are explicit, but the same external universal dependencies prevent a complete independent reproduction. |
| C4 | 2/2 | The bounded quadratic has a unique affine path and the affine tuning objective gives `M_total=Delta_total=1`; the universal shattering identity, checker, and guarded control fully falsify the literal theorem. |
| C5 | 1/2 | The norm lift and asymptotic domination are useful, but the complete universal implication remains conditional on the external theorem chain. |
| C6 | 1/2 | The mp-QP specialization is useful only on `alpha>=0`; the printed all-real domain gap remains and the external path theorem is trusted. |

Total outcome-blind assessment: **8/12**. This is not a live judge score.

## Structural and release gates

- Index, pinned executive summary, scope/cost table, pinned poster, six claim
  pages, and Conclusion are in fixed order.
- The active tree contains no historical child.
- Historical judged paths remain present outside the active tree.
- C1/C4 expose source, raw JSON, primary code, independent code, exact output,
  and a fail-sensitive corrected control.
- `finite_sweeps_used_as_proof` is zero; the 510 enumerated rows are diagnostic.
- The independent implementation imports no primary code.
- Every linked path exists; release visibility PASS with zero missing paths and
  zero missing cells.

This is **not** a perfect blind review. Claims 2, 3, 5, and 6 retain honest
universal proof blockers. Rewriting their prose would not repair those defects.
The exact C1/C4 falsifications are additive and cannot weaken the 6/12 judged
baseline, so the candidate is eligible for publication after exact validation.
