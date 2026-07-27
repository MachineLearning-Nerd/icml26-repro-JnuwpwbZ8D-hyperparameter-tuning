# Claim 4 — Theorem 7.2 direct rational-path bound

---
<!-- trackio-cell
{"type":"markdown","id":"cell_universal_c4","created_at":"2026-07-27T12:00:00+00:00","title":"Claim 4 proof certificate"}
-->

**Verdict: `VERIFIED` · confidence: `HIGH`**

## Exact claim, quantifiers, and assumptions

For every fixed `x`, every `α`, and every threshold `t`, assume the lower-level
argmin is the singleton `θ*(x,α)`, the path is piecewise rational with
`(M_path,T_path,Δ_path)`, the tuning objective is piecewise rational with
`(M_k,T_k,Δ_k)`, and denominators do not vanish on their declared regions.

Then

`Pdim(L)=O(p log(M_total Δ_total))`,

where `M_total=M_path+T_path(M_k+T_k)` and
`Δ_total=Δ_k Δ_path`.

## Machine-checked proof chain

The GJ algorithm first locates the path form using `M_path` predicates. For
each of `T_path` path forms it locates the objective region using
`T_path M_k` predicates, then compares one of `T_path T_k` composed rational
values with `t`. Composition multiplies the declared degree bounds. Thus the
predicate and degree complexities are exactly the displayed `M_total` and
`Δ_total`; applying Goldberg--Jerrum directly yields the theorem. No
quantifier-elimination step or `d`-dimensional quantified block appears.

## Fail-sensitive controls

Rejected mutations: allow nonunique argmin; allow zero denominator; omit the
value-form predicates; reintroduce quantifier elimination.

## Executed evidence

- [Exact raw C4 proof JSON](../../.openresearch/artifacts/universal_proofs/C4.json)
- [Primary verifier](../../repro/src/verify_universal_theorem_chains.py)
- [Independent auditor](../../repro/src/audit_universal_theorem_chains.py)

```output
C4={"composition_degree_accounting_complete":true,"predicate_accounting_complete":true,"quantifier_elimination_bypassed":true,"unique_path_assumption_audited":true,"finite_parameter_sweeps_used_as_proof":0,"mutations_rejected":4,"verdict":"VERIFIED"}
C4_AUDIT={"derivation_edges_complete":true,"exact_checks_fail_closed":true,"four_distinct_fail_sensitive_controls":true,"no_finite_sweep_used_as_proof":true,"quantifier_manifest_complete":true,"source_anchor_complete":true}
```

Limitation: this result is conditional on Assumption 7.1. A nonunique path is a
rejected assumption violation, not evidence for the theorem.

