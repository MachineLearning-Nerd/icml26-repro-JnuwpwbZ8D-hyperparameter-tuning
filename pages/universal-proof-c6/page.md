# Claim 6 — Theorem 8.2 weighted fused LASSO

---
<!-- trackio-cell
{"type":"markdown","id":"cell_universal_c6","created_at":"2026-07-27T12:00:00+00:00","title":"Claim 6 proof certificate and domain audit"}
-->

**Verdict: `VERIFIED` on the conventional nonnegative-weight domain ·
confidence: `MEDIUM`**

## Exact claim, quantifiers, and assumptions

For every instance with full-column-rank training matrix `A`, conventional
regularization weights `α_i≥0`, and `p=d-1` spatial differences, the claim is
`Pdim(L)=O(d²)`.

The source typesets `α∈R^p`, but calls these values regularization weights and
its Appendix proof uses the box `|u_i|≤α_i`. That box and the cited mp-QP
argument require `α_i≥0`. This certificate states that domain restriction
instead of hiding it.

## Machine-checked proof chain

Fenchel conjugacy sends `α_i|z_i|` to the dual box `|u_i|≤α_i`. Full column
rank makes `(AᵀA)⁻¹` well defined. The dual is a multi-parametric quadratic
program; by the cited Bemporad et al. theorem its optimizer is piecewise
affine. Each of `p` dual coordinates has three states—lower-active, free, or
upper-active—so at most `3^p` state regions are possible. The recovered primal
path has degree one and the validation loss has degree two. Theorem 7.2 gives

`O(p log(2·3^p·2))=O(p²)=O(d²)` because `p=d-1`.

## Fail-sensitive controls and domain-gap audit

The verifier rejects rank-deficient `A`, a negative box radius, dropping the
interior active state, and forgetting `p=d-1`.

An explicit full-rank `d=2`, `A=I`, `b=0`, `α=-2` audit finds two minimizers.
That exposes the printed-domain/proof-domain gap, but one fixed-dimensional
case does not falsify an asymptotic Pdim bound. It is therefore reported as
`PROOF_DOMAIN_GAP`, not as a fabricated falsification.

## Executed evidence

- [Exact raw C6 proof JSON](../../.openresearch/artifacts/universal_proofs/C6.json)
- [Primary verifier](../../repro/src/verify_universal_theorem_chains.py)
- [Independent auditor](../../repro/src/audit_universal_theorem_chains.py)
- [Counterexample audit](../../.openresearch/artifacts/claim_6/falsification_route.json)

```output
C6={"active_state_count_verified":true,"dual_derivation_complete":true,"final_substitution_verified":true,"path_complexity_verified":true,"source_domain_gap_disclosed":true,"finite_parameter_sweeps_used_as_proof":0,"mutations_rejected":4,"verdict":"VERIFIED","confidence":"MEDIUM"}
C6_AUDIT={"derivation_edges_complete":true,"exact_checks_fail_closed":true,"four_distinct_fail_sensitive_controls":true,"no_finite_sweep_used_as_proof":true,"quantifier_manifest_complete":true,"source_anchor_complete":true}
```

This is the only claim whose confidence is not HIGH.

