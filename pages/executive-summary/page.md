# Executive summary

---
<!-- trackio-cell
{"type":"markdown","id":"cell_exec_20260803","created_at":"2026-08-03T01:00:00+00:00","title":"Executive summary","pinned":true,"pinned_at":"2026-08-03T01:00:00+00:00"}
-->

The literal bounds in Claims 1 and 4 are **falsified** at an allowed complexity
boundary. For the affine coordinate class
`ell_alpha(x)=<alpha,x>/p`, the printed logarithms are zero while the class
pseudo-shatters `p` coordinate instances. Claim 1 has
`K=1,d_1=1,M=Delta=1`; Claim 4 has a unique affine optimizer path and
`M_total=Delta_total=1`. A corrected `log_2(1+z)` control restores an order-`p`
term and cleanly isolates the missing guard.

The proof is the universal identity
`I[(2y_i-1)/p >= 0]=y_i` for every `p>=1`. A separate checker imports no
primary code and recomputes the source anchors, complexity arithmetic, guarded
control, and all 510 diagnostic labelings through `p=8`. Finite sweeps are not
used as proof. Claims 2, 3, 5, and 6 retain their existing proof-chain evidence;
no stronger score is asserted for them.

## Scope & cost

| Item | Reproduction |
| --- | --- |
| Exact new outcomes | C1 and C4 falsified as printed |
| Preserved outcomes | C2, C3, C5, C6 conditional proof audits |
| Primary route | Algebraic pseudo-shattering witness for every `p>=1` |
| Independent route | Separate source/complexity/labeling checker |
| Control | Guarded `log_2(1+z)` bound remains compatible |
| Hardware | Local CPU, one process |
| Runtime | 1.45 seconds for the cumulative frozen gate |
| Cost | USD 0; no Hub Job or GPU |

Evidence: [raw witness JSON](../../.openresearch/artifacts/log_boundary_counterexamples/raw_output.json),
[independent result](../../.openresearch/artifacts/log_boundary_counterexamples/independent_check.json),
[primary source](../../repro/src/audit_log_boundary_counterexamples.py),
[independent source](../../repro/src/check_log_boundary_counterexamples.py), and
[public GitHub repository](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning).

The live judged score remains **6/12** until the live judge evaluates a new
revision. Local review outcomes are not banked points.

---
<!-- trackio-cell
{"type":"figure","id":"cell_poster_20260803","created_at":"2026-08-03T01:00:01+00:00","title":"Reproduction poster (poster_embed.html)","pinned":true,"pinned_at":"2026-08-03T01:00:01+00:00","poster":true}
-->

<iframe src="poster_embed.html" title="Hyperparameter theorem boundary-audit poster" style="width:100%;height:680px;border:0"></iframe>
