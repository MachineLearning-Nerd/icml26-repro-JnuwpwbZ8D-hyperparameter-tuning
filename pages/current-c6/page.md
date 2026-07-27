# CURRENT — C6: weighted fused LASSO

**Verdict: VERIFIED · confidence: MEDIUM**

Exact reported result (Theorem 8.2, main lines 598–617): for weighted fused
LASSO with `p=d-1`, full-column-rank `A`, and bounded validation loss,

`Pdim(L)=O(d²)`.

Under the conventional nonnegative regularization-weight domain, full rank
makes the dual quadratic strictly convex. Each of the `p` box coordinates is
lower-active, free, or upper-active, so `M_path,T_path<=3^p`; the path is
affine and validation loss quadratic. C4 then gives
`p log(O(3^p))=O(p²)=O(d²)`. SymPy checks the final dimension witness and five
independent dimensions check explicit bounds.

Material scope warning: the main text typesets `alpha in R^p`, while the dual
constraint `|u_i|<=alpha_i` requires `alpha_i>=0`. With full-rank `A=I`,
`b=0`, `d=2`, and `alpha=-2`, the primal objective has two global minimizers
`(-2,2)` and `(2,-2)`, each value `-4`. This invalidates the cited unique-path
proof on the printed all-real domain but does **not** contradict an asymptotic
pseudo-dimension bound. It is not called falsification.

## KKT-checked fused-LASSO path evidence

For the full-rank signal-denoising case `A=I`, the verifier solves the exact
dual box QP by coordinate descent and checks the KKT system independently.
With 1,200 nonnegative weight vectors per seed, the observed region counts are
`10/9/8`, `32/25/28`, and `65/77/106` at `d=4,6,8`; the maximum KKT violation
is below `1.0e-12`, and every count is below `3^(d-1)`. Across
`d=3,5,8,12,16,20`, the representative `bound/d²` stays in
`[0.796,1.057]`. The checker rejects both a rank-deficient design and a
negative box radius; it also rejects a mutation that deletes the `p=d-1`
factor.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_6/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_6/signature_checker.json)

- [Contract](../../.openresearch/artifacts/claim_6/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_6/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_6/raw_output.json)
- [Independent checker](../../.openresearch/artifacts/claim_6/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_6/negative_control_output.json)
- [Falsification route / gap witness](../../.openresearch/artifacts/claim_6/falsification_route.json)
- [Full adversarial raw JSON](../../.openresearch/artifacts/claims2_6_counterexample_audit.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Audit source](../../repro/src/audit_claims2_6_counterexamples.py)
- [Limitations](../../.openresearch/artifacts/claim_6/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old 153 two-coordinate KKT cases are **Historical rejected baseline**.
