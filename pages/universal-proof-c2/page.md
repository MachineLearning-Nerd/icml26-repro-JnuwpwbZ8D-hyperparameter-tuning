# Claim 2 — Theorem 5.1 training-loss bound

---
<!-- trackio-cell
{"type":"markdown","id":"cell_universal_c2","created_at":"2026-07-27T12:00:00+00:00","title":"Claim 2 proof certificate"}
-->

**Verdict: `VERIFIED` · confidence: `HIGH`**

## Exact claim, quantifiers, and assumptions

For every `x,t,α`, let the attained loss be
`ℓ_α(x)=min_{θ∈Θ} f_x(α,θ)`, where `Θ` is the stated `d`-dimensional box and
`f_x` has uniform piecewise-polynomial complexity `(M_f,T_f,Δ_f)`. Then

`Pdim(L)=O(pd log(M_f+T_f+d)+p²d log Δ_f)`.

The universal threshold contract is

`ℓ_α(x)≥t  ↔  ∀θ∈R^d [θ∉Θ ∨ f_x(α,θ)≥t]`.

## Machine-checked proof chain

The formula has one `∀θ` block of dimension `d`. Region location and value
selection use `M_f+T_f` atoms; the box uses `2d`, so the exact atom count is
`M_f+T_f+2d`. Substituting this profile into Theorem 4.1 and applying the
universal witnesses

- `2d-(d+1)=d-1≥0`,
- `2(M_f+T_f+d)-(M_f+T_f+2d)=M_f+T_f≥0`,

gives the stated bound. These identities are symbolic witnesses for all
positive integer dimensions and complexities; they are not checked on a grid.

## Fail-sensitive controls

The verifier rejects replacing `∀` by `∃`, removing the box-domain guard,
omitting the piece-value atoms, and reversing `≥t` to `≤t`.

## Executed evidence

- [Exact raw C2 proof JSON](../../.openresearch/artifacts/universal_proofs/C2.json)
- [Primary verifier source](../../repro/src/verify_universal_theorem_chains.py)
- [Independent auditor](../../repro/src/audit_universal_theorem_chains.py)
- [Independent audit JSON](../../.openresearch/artifacts/universal_proofs/independent_audit.json)

```output
C2={"atom_count_complete":true,"atom_witness_proved":true,"dimension_witness_proved":true,"one_quantifier_block":true,"finite_parameter_sweeps_used_as_proof":0,"mutations_rejected":4,"verdict":"VERIFIED"}
C2_AUDIT={"derivation_edges_complete":true,"exact_checks_fail_closed":true,"four_distinct_fail_sensitive_controls":true,"no_finite_sweep_used_as_proof":true,"quantifier_manifest_complete":true,"source_anchor_complete":true}
```

Limitation: the logical equivalence uses the theorem’s written `min`; an
objective whose infimum is not attained does not satisfy this contract.

