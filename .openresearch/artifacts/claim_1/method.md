# C1 method

The verifier treats the two explicitly cited foundational results as premises,
then checks the complete algebraic implication to Theorem 4.1. SymPy checks the
expanded symbolic expression and coefficient witness. A separately written
integer checker evaluates 384 combinations of `p`, `K`, dimensions, and
positive lemma constants without importing the symbolic checker.

Three mutations must be rejected: removing the quadratic-in-`p` degree term,
using `M` rather than `K` as a product index, and claiming the source's second
product is `prod(d_k+1)`. The first mutation is refuted by an unbounded
coefficient ratio as `p` grows; the latter two fail exact source anchors.

Command (inherited unchanged by every node):

`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`
