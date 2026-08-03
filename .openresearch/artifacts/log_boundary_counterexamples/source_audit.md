# Source audit

- Paper: arXiv:2602.02406.
- Theorem 4.1: `source/icml2026.tex:390-400`.
- First-order formula definition: `source/icml2026.tex:259-280`.
- Explicit-path assumption: `source/icml2026.tex:536-546`.
- Theorem 7.2: `source/icml2026.tex:553-555`.
- Direct Goldberg--Jerrum proof: `source/icml_appendix.tex:28-30` and the
  Appendix F construction.

The source contains unguarded `log M`, `log Delta`, and
`log(M_total Delta_total)`. It does not state lower bounds excluding one atom,
degree one, or a one-piece affine path/objective.
