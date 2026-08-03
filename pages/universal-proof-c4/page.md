# Claim 4 — Theorem 7.2

---
<!-- trackio-cell
{"type":"markdown","id":"cell_c4_boundary_20260803","created_at":"2026-08-03T01:00:04+00:00","title":"Exact unique-path logarithmic-boundary falsification"}
-->

**Verdict: `FALSIFIED AS PRINTED` · confidence: `HIGH`**

## Literal claim and source

Theorem 7.2 at `source/icml2026.tex:553-555` states

`Pdim(L)=O(p log(M_total Delta_total))`,

where `M_total=M_path+T_path(M_k+T_k)` and
`Delta_total=Delta_k Delta_path`.

## Assumption-satisfying counterexample

Use `alpha,theta in [-1,1]^p`, coordinate instances `x_i=e_i`, and

- training objective `f_x(alpha,theta)=||theta-alpha||_2^2/(4p)`;
- tuning objective `k_x(alpha,theta)=<theta,x>/p`.

The bounded training objective has the unique minimizer `theta*=alpha` for
every `alpha`, exactly satisfying Assumption 7.1. The optimizer path has one
affine piece: `M_path=0,T_path=1,Delta_path=1`. The tuning objective also has
one affine piece: `M_k=0,T_k=1,Delta_k=1`. Hence

`M_total=0+1*(0+1)=1` and `Delta_total=1*1=1`.

The printed RHS is zero. Yet the induced loss is
`ell_alpha(x)=<alpha,x>/p`, and the same universal choice
`alpha_i=2y_i-1` pseudo-shatters all `p` coordinate instances at threshold
zero. Thus `Pdim(L)>=p>0`, contradicting the printed theorem for every `p>=1`.

## Fail-sensitive control and rerun evidence

The guarded control `p log_2(1+M_total Delta_total)=p` is compatible with the
witness. The older nonunique-path candidate is not used; this witness has a
unique affine path and no denominator.

`finite_sweeps_used_as_proof: 0`.

- [Raw exact evidence](../../.openresearch/artifacts/log_boundary_counterexamples/raw_output.json)
- [Independent checker output](../../.openresearch/artifacts/log_boundary_counterexamples/independent_check.json)
- [Method](../../.openresearch/artifacts/log_boundary_counterexamples/method.md)
- [Source audit](../../.openresearch/artifacts/log_boundary_counterexamples/source_audit.md)
- [Limitations](../../.openresearch/artifacts/log_boundary_counterexamples/limitations.md)
- [Primary verifier](../../repro/src/audit_log_boundary_counterexamples.py)
- [Independent verifier](../../repro/src/check_log_boundary_counterexamples.py)
- [Retained path-accounting audit](../../.openresearch/artifacts/universal_proofs/C4.json)

```output
C4_COMPLEXITY={"M_path":0,"T_path":1,"Delta_path":1,"M_k":0,"T_k":1,"Delta_k":1,"M_total":1,"Delta_total":1,"printed_rhs_factor":0,"pdim_lower_bound":"p"}
LOG_BOUNDARY_CHECK={"c4_total_complexities_recomputed":true,"c4_total_degree_recomputed":true,"labelings_recomputed":510,"verdict":"INDEPENDENT_CHECK_PASS"}
```
