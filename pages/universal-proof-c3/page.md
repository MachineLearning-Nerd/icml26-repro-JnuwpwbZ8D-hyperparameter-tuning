# Claim 3 — Theorem 6.1 bilevel validation bound

---
<!-- trackio-cell
{"type":"markdown","id":"cell_universal_c3","created_at":"2026-07-27T12:00:00+00:00","title":"Claim 3 proof certificate"}
-->

**Verdict: `VERIFIED` · confidence: `HIGH`**

## Exact claim, quantifiers, and assumptions

For every `x,t,α`, assume nonempty lower-level argmin and the stated uniform
piecewise-polynomial complexities for distinct training objective `f_x` and
validation objective `g_x`. For the optimistic bilevel loss, the exact
quantifier order is

`∀θ∈R^d ∃θ'∈R^d`:

`θ∉Θ ∨ g_x(α,θ)≥t ∨ [θ'∈Θ ∧ f_x(α,θ')<f_x(α,θ)]`.

The claim is
`Pdim(L)=O(pd² log M_tot+p²d² log Δ_tot)`.

## Machine-checked proof chain

The two blocks have dimensions `(d,d)`. Validation contributes `M_g+T_g`
atoms; simultaneous location of two training pieces plus their value
comparison contributes `2M_f+T_f²`; the two box tests contribute `4d`.
Theorem 4.1 therefore receives

`M=4d+M_g+T_g+2M_f+T_f²`, `Δ=max(Δ_f,Δ_g)`.

The universal algebraic witnesses are

- `4d²-(d+1)²=(d-1)(3d+1)≥0`;
- after shifting every positive integer variable by one, every coefficient of
  `5M_tot²-(4d+M_g+T_g+2M_f+T_f²)` is nonnegative.

This yields the two stated `d²` terms without using a finite sweep.

## Fail-sensitive controls

The verifier rejects swapping `∀θ∃θ'`, setting validation equal to training,
dropping nonempty argmin, and reversing the strict better-candidate relation.

## Executed evidence

- [Exact raw C3 proof JSON](../../.openresearch/artifacts/universal_proofs/C3.json)
- [Primary verifier](../../repro/src/verify_universal_theorem_chains.py)
- [Independent auditor](../../repro/src/audit_universal_theorem_chains.py)

```output
C3={"atom_count_complete":true,"atom_witness_proved":true,"dimension_witness_proved":true,"two_quantifier_blocks":true,"finite_parameter_sweeps_used_as_proof":0,"mutations_rejected":4,"verdict":"VERIFIED"}
C3_AUDIT={"derivation_edges_complete":true,"exact_checks_fail_closed":true,"four_distinct_fail_sensitive_controls":true,"no_finite_sweep_used_as_proof":true,"quantifier_manifest_complete":true,"source_anchor_complete":true}
```

Limitation: the strictly better witness uses the stated nonempty argmin. An
unattained lower-level infimum is outside this certificate.

