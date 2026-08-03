# Claims 1 and 4 — exact logarithmic-boundary method

Both claims are audited at the smallest complexity values allowed by their
statements. The shared loss class is
`ell_alpha(x)=<alpha,x>/p` with `alpha in [-1,1]^p` and instances `x_i=e_i`.
At thresholds zero, any labeling `y` is realized by `alpha_i=2y_i-1`, hence
the class pseudo-shatters `p` points for every `p>=1`.

For Claim 1 the threshold predicate is the valid one-atom formula
`(exists theta in R) [<alpha,x>/p-t>=0]`, so `K=1,d_1=1,M=Delta=1`.
For Claim 4 the bounded training objective `||theta-alpha||^2/(4p)` has the
unique one-piece affine path `theta*=alpha`; the tuning objective
`<theta,x>/p` is also one-piece affine, so `M_total=Delta_total=1`.

The primary script emits the algebraic certificate and 510 diagnostic
labelings. The independent checker imports no primary code and recomputes the
source anchors, all complexity arithmetic, all labelings, and the guarded-log
control.
