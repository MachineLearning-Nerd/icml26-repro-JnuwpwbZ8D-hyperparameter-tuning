# Claim 5 — Theorem 8.1 weighted group LASSO

---
<!-- trackio-cell
{"type":"markdown","id":"cell_universal_c5","created_at":"2026-07-27T12:00:00+00:00","title":"Claim 5 proof certificate"}
-->

**Verdict: `VERIFIED` · confidence: `HIGH`**

## Exact claim, quantifiers, and assumptions

For every `x,t,α` for which the optimistic loss is well defined, partition
`θ∈R^d` into `p` nonempty groups (`p≤d`). The claimed bound is

`Pdim(L)=O(p³d+p²d²)`.

The certificate uses `∀θ∈R^d` followed by
`∃(z,ν^θ,ν^z)∈R^(d+2p)`.

## Machine-checked proof chain

For every group, the polynomial lift
`ν_i²=Σ_j θ_{ij}² ∧ ν_i≥0` is exactly equivalent to
`ν_i=||θ_i||₂`; the sign guard is essential. Two candidate vectors require
`2p` equalities and `2p` sign guards. Adding training and validation
comparisons gives `M=2+4p`, degree `2`, and block dimensions `d` and `d+2p`.

Theorem 4.1 gives

`p(d+1)(d+2p+1)log(2+4p)+p²d(d+2p)log2`.

For integer `p,d≥1`, `log(2+4p)≤2p` and `log2≤1`; after shifting `p,d` by
one, every coefficient of

`16(p³d+p²d²)-[2p²(d+1)(d+2p+1)+p²d(d+2p)]`

is nonnegative. This is a universal coefficient certificate for the displayed
asymptotic simplification.

## Fail-sensitive controls

Rejected mutations: remove `ν≥0`; omit validation comparison; omit the
candidate-`z` norm variables; drop well-defined argmin.

## Executed evidence

- [Exact raw C5 proof JSON](../../.openresearch/artifacts/universal_proofs/C5.json)
- [Primary verifier](../../repro/src/verify_universal_theorem_chains.py)
- [Independent auditor](../../repro/src/audit_universal_theorem_chains.py)

```output
C5={"atom_count_verified":true,"block_dimensions_verified":true,"coefficient_domination_proved":true,"signed_alpha_does_not_change_norm_lift_identity":true,"finite_parameter_sweeps_used_as_proof":0,"mutations_rejected":4,"verdict":"VERIFIED"}
C5_AUDIT={"derivation_edges_complete":true,"exact_checks_fail_closed":true,"four_distinct_fail_sensitive_controls":true,"no_finite_sweep_used_as_proof":true,"quantifier_manifest_complete":true,"source_anchor_complete":true}
```

The small KKT experiments remain corroboration only and are not used here.

