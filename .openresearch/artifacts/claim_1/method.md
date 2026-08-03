# C1 method

The decisive audit checks the smallest allowed structural values before using
asymptotic simplifications. For every `p>=1`, let the instances be the
coordinate vectors `e_i`, set all thresholds to zero, and use
`ell_alpha(x)=<alpha,x>/p` on `[-1,1]^p`. Its threshold test is the one-atom
formula `(exists theta in R) [<alpha,x>/p-t >= 0]`; the quantified variable may
be vacuous under Definition 3.1. Thus `K=1`, `d_1=1`, `M=Delta=1`.

For each label vector `y`, `alpha_i=2y_i-1` realizes exactly `y`, proving
`Pdim>=p` algebraically. The independent checker recomputes all 510 diagnostic
labelings for `p=1,...,8`, the complexity arithmetic, and a guarded-log control.

The earlier derivation audit below is retained for provenance but does not
survive this boundary test.

The verifier treats the two explicitly cited foundational results as premises,
then checks the complete algebraic implication to Theorem 4.1. SymPy checks the
expanded symbolic expression and coefficient witness. A separately written
integer checker evaluates 384 combinations of `p`, `K`, dimensions, and
positive lemma constants without importing the symbolic checker.

Three historical mutations are also rejected: removing the quadratic-in-`p` degree term,
using `M` rather than `K` as a product index, and claiming the source's second
product is `prod(d_k+1)`. The first mutation is refuted by an unbounded
coefficient ratio as `p` grows; the latter two fail exact source anchors.

Command (inherited unchanged by every node):

`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`
