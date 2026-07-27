# Method

The primary verifier reconstructs each theorem as a proof graph:

1. exact domain and quantifier manifest;
2. source assumptions;
3. logical threshold reduction;
4. predicate, dimension, and degree profile;
5. invocation of a named trusted theorem;
6. algebraic asymptotic simplification;
7. four fail-sensitive mutations.

The independent auditor does not import the primary module. It treats the
primary JSON as untrusted and checks source anchors, quantifiers, derivation
edges, mutation classes, Boolean exact checks, absence of finite sweeps as
proof, and the final verdict.

Fixed command:

`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`
