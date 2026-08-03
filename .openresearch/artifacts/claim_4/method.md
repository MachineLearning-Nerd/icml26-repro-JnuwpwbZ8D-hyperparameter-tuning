# C4 method

The exact witness uses `alpha,theta in [-1,1]^p`, training objective
`||theta-alpha||^2/(4p)`, and tuning objective `<theta,x>/p`. The training
objective has the unique path `theta*=alpha`. Both the path and objective have
one affine piece, giving `M_total=Delta_total=1` exactly. Coordinate instances
at threshold zero are pseudo-shattered by `alpha_i=2y_i-1`.

An independently implemented checker recomputes all complexity values and the
same 510 diagnostic labelings without importing the primary verifier.

The retained earlier checker follows the decision computation away from the
boundary: locate the rational path piece, locate the objective piece after
composition, then test the rational threshold. It verifies 128 independent
complexity tuples and rejects removal of uniqueness.
