# Conclusion

---
<!-- trackio-cell
{"type":"markdown","id":"cell_conclusion_20260803","created_at":"2026-08-03T01:00:08+00:00","title":"Conclusion and reproducibility notes"}
-->

Claims 1 and 4 are **falsified as printed** by one shared, exact affine family.
The failure is narrow but decisive: their unguarded logarithms vanish at
allowed unit complexity. The guarded `log_2(1+z)` control survives.

| Claim | Current evidence outcome | Blind-review ceiling |
| --- | --- | ---: |
| C1 | Exact universal falsification as printed | 2/2 |
| C2 | Preserved conditional proof-chain audit | 1/2 |
| C3 | Preserved conditional proof-chain audit | 1/2 |
| C4 | Exact universal falsification as printed | 2/2 |
| C5 | Preserved conditional proof-chain audit | 1/2 |
| C6 | Preserved conditional proof-chain audit; all-real weight domain gap remains | 1/2 |

The four one-point claims are not relabeled as complete: their current route
still treats external QE/Goldberg--Jerrum/mp-QP results as trusted dependencies,
and C6 additionally has the documented `alpha in R^p` versus `alpha>=0` proof
gap. No finite experiment can close those universal dependencies.

Run the exact frozen local command:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

It regenerates the exact witnesses, runs the separately implemented checker,
audits all six source chains, checks the visible release surface, validates the
notebook, and runs the scoped unit tests. Local CPU only; fixed, seed-free
algebraic proof; USD 0.

Repository: [MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning).
The live leaderboard remains 6/12 until the judge evaluates a published SHA.
