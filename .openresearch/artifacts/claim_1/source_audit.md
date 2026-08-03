# C1 source audit

- Retrieved URL: `https://ar5iv.labs.arxiv.org/html/2602.02406`
- Retrieval UTC: `2026-07-24T14:49:15Z`
- HTML SHA-256: `f31ac76c07c173dc777ea16d5bc718cadc116824479ee801b3a3f55499f900a0`
- Primary repository source: `source/icml2026.tex`, SHA-256 `5c7260856bcaf8554196716d0dc1ebfc69ebab1684893207b938e93d601754ef`
- Theorem anchor: main source lines 390–400.
- Quantifier-elimination anchor: main source lines 299–313.
- GJ anchor: appendix lines 6–30.
- Proof anchor: appendix lines 35–65.

The exact source theorem universally quantifies over function classes whose
threshold predicates have a uniform polynomial-FOL representation. It assumes
fixed quantifier-block count `K`, quantified dimensions `d_k`, at most `M`
atomic polynomials, maximum degree `Delta`, and `p` real free parameters. The
second displayed product is `prod d_k`, not `prod(d_k+1)`.

Neither the theorem nor its proof supplies a positive guard for `log(M)` or
`log(Delta)`. Definition 3.1 does not require each quantified variable to occur
in an atomic polynomial, so a one-block vacuous quantifier is within scope.

The appendix proof also contains two local notation errors: its products use `M` as
the upper index instead of `K`, and one occurrence says `Delta_f` instead of
`Delta`. The certificate rejects those transcriptions and follows the main
theorem plus the preceding quantifier-elimination theorem. Those transcription
errors are separate from the decisive missing-log-guard falsification.
