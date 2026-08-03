---
title: "Repro - Provably Data-driven Multiple Hyper-parameter Tuning"
emoji: 📐
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-JnuwpwbZ8D
---

# Exact boundary audit of arXiv:2602.02406

Claims 1 and 4 are **falsified as printed**. Their unguarded logarithms vanish
at allowed unit complexity, yet one affine coordinate family pseudo-shatters
`p` points for every `p>=1`.

| Claim | Exact complexity | Printed factor | Exact lower bound | Outcome |
| --- | --- | ---: | ---: | --- |
| C1 | `K=1,d_1=1,M=Delta=1` | 0 | `Pdim>=p` | FALSIFIED AS PRINTED |
| C4 | `M_total=Delta_total=1`, unique affine path | 0 | `Pdim>=p` | FALSIFIED AS PRINTED |

For `x_i=e_i`, `t_i=0`, and `ell_alpha(x)=<alpha,x>/p`, every labeling
`y in {0,1}^p` is realized by `alpha_i=2y_i-1`. A separately implemented
checker recomputes every source anchor, complexity identity, corrected control,
and 510 diagnostic labelings. The finite enumeration is not the proof; the
coordinate-wise identity is universal.

The corrected control `log_2(1+z)` restores an order-`p` term, so the result
does not refute an intended guarded theorem. Claims 2, 3, 5, and 6 retain their
existing source-exact proof audits. C6 retains its disclosed all-real versus
nonnegative-weight proof-domain gap.

## Read and reproduce

- [Logbook index](pages/universal-proof-index/page.md)
- [Claim 1 exact falsification](pages/universal-proof-c1/page.md)
- [Claim 4 exact falsification](pages/universal-proof-c4/page.md)
- [Raw witness JSON](.openresearch/artifacts/log_boundary_counterexamples/raw_output.json)
- [Independent checker JSON](.openresearch/artifacts/log_boundary_counterexamples/independent_check.json)
- [Conclusion and limitations](pages/universal-proof-release/page.md)
- [Public GitHub repository](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning)

Run:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

Local CPU only, deterministic and seed-free, 1.45 seconds, USD 0. The live
judge score remains **6/12** until a newly published revision is evaluated.
Every historical judged path and prior evidence artifact remains retained.
