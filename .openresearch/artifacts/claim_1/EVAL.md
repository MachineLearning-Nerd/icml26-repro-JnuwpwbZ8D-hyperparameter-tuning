# C1 — Theorem 4.1 boundary audit

Verdict: **FALSIFIED AS PRINTED**

The prior symbolic derivation omitted the allowed boundary `M=Delta=1`, where
both printed logarithms vanish. The affine coordinate class has a one-atom,
degree-one FOL representation and pseudo-shatters `p` instances, so its
pseudo-dimension is at least `p` while the printed expression is zero.

- Exact joint C1/C4 evidence: [`../log_boundary_counterexamples/raw_output.json`](../log_boundary_counterexamples/raw_output.json)
- Independent checker: [`../log_boundary_counterexamples/independent_check.json`](../log_boundary_counterexamples/independent_check.json)

- Raw result: [`raw_output.json`](raw_output.json)
- Contract: [`claim_contract.json`](claim_contract.json)
- Certificate: [`proof_certificate.json`](proof_certificate.json)
- Source audit: [`source_audit.md`](source_audit.md)
- Method: [`method.md`](method.md)
- Limitations: [`limitations.md`](limitations.md)
- Falsification route: [`falsification_route.json`](falsification_route.json)

The older proof certificate is retained as a derivation audit but its
`VERIFIED` conclusion is superseded by the assumption-satisfying counterexample.
