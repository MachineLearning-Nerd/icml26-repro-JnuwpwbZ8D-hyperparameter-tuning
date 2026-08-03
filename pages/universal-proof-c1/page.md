# Claim 1 — Theorem 4.1

---
<!-- trackio-cell
{"type":"markdown","id":"cell_c1_boundary_20260803","created_at":"2026-08-03T01:00:02+00:00","title":"Exact logarithmic-boundary falsification"}
-->

**Verdict: `FALSIFIED AS PRINTED` · confidence: `HIGH`**

## Literal claim and source

Theorem 4.1 at `source/icml2026.tex:390-400` states

`Pdim(F)=O(p prod(d_k+1) log M + p^2 prod(d_k) log Delta)`.

The generated claim uses the larger `prod(d_k+1)` in its second term, but that
does not affect this witness because both logarithms vanish.

## Assumption-satisfying counterexample

For every `p>=1`, set `A=[-1,1]^p`, let `x_i=e_i`, and define
`ell_alpha(x)=<alpha,x>/p`. For arbitrary `x,t`, its threshold predicate is

`(exists theta in R) [<alpha,x>/p-t >= 0]`.

Definition 3.1 does not require a quantified variable to occur in an atom, so
this is a valid fixed one-block polynomial FOL with
`K=1`, `d_1=1`, `M=1`, and `Delta=1`. The printed RHS is therefore zero.

At thresholds `t_i=0`, every label vector `y in {0,1}^p` is realized by
`alpha_i=2y_i-1`, because

`I[ell_alpha(e_i)>=0] = I[(2y_i-1)/p>=0] = y_i`.

Thus `Pdim(F)>=p>0` for every `p>=1`, contradicting the identically zero
printed bound. This is a family of exact counterexamples, not a finite sweep.

## Fail-sensitive control and rerun evidence

Replacing the boundary term by `log_2(1+M)` yields `p`, which is compatible
with the exact lower bound. This control shows that the missing positive log
guard—and not the affine construction—is decisive.

- [Raw exact evidence](../../.openresearch/artifacts/log_boundary_counterexamples/raw_output.json)
- [Independent checker output](../../.openresearch/artifacts/log_boundary_counterexamples/independent_check.json)
- [Method](../../.openresearch/artifacts/log_boundary_counterexamples/method.md)
- [Source audit](../../.openresearch/artifacts/log_boundary_counterexamples/source_audit.md)
- [Limitations](../../.openresearch/artifacts/log_boundary_counterexamples/limitations.md)
- [Primary verifier](../../repro/src/audit_log_boundary_counterexamples.py)
- [Independent verifier](../../repro/src/check_log_boundary_counterexamples.py)
- [Retained derivation audit](../../.openresearch/artifacts/universal_proofs/C1.json)

```output
LOG_BOUNDARY_COUNTEREXAMPLES={"claims":{"C1":"FALSIFIED_AS_PRINTED","C4":"FALSIFIED_AS_PRINTED"},"finite_sweeps_used_as_proof":0,"labelings_checked":510,"verdict":"LITERAL_FALSIFICATION_AS_PRINTED"}
LOG_BOUNDARY_CHECK={"labelings_recomputed":510,"independent_checker_imports_primary":false,"verdict":"INDEPENDENT_CHECK_PASS"}
```
