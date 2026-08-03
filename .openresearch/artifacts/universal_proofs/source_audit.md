# Source audit

Retrieved 2026-07-27 for arXiv:2602.02406 with an explicit browser
User-Agent.

- `source/icml2026.tex`:
  `5c7260856bcaf8554196716d0dc1ebfc69ebab1684893207b938e93d601754ef`
- `source/icml_appendix.tex`:
  `3551432784412496e3f3ffac96272de1745b8b6e4c4a1afd0c79c606dc37068f`
- structured full-text retrieval:
  `eba938e8df91d449708d1c1f8f7c149f32ae69229701e6a32b876e50d4ef87ed`

Anchors: main Theorems 4.1, 5.1, 6.1, Assumption 7.1 and Theorem
7.2, Theorems 8.1 and 8.2; Appendix Theorem A.3 and Sections B, C, E,
F, G.1, G.2.

Audited source issues:

1. The C1 and C4 displayed bounds omit a positive guard around logarithmic
   complexity. Allowed unit-complexity affine classes therefore make their
   right-hand sides zero despite pseudo-dimension at least `p`.
2. The Appendix B product upper index `M` is inconsistent with the main
   quantifier-elimination theorem's `K`; the certificate uses `K`.
3. The exact Theorem 4.1 degree term uses `prod(d_k)`, while the imported judge
   paraphrase uses the larger `prod(d_k+1)`.
4. Theorem 8.2 prints `alpha in R^p`, while its dual-box proof needs
   nonnegative regularization weights.
