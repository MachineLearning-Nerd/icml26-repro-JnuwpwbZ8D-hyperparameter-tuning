# C6 source audit

Theorem 8.2 is at main lines 598–617 and explicitly assumes full-column-rank
`A`. Appendix lines 405–470 derive the box-constrained dual and the at-most
`3^(d-1)` active-state count. The text writes `alpha in R^p`, while the dual
route requires the conventional nonnegative regularization-weight domain; this
assumption is made explicit in the contract rather than hidden.
