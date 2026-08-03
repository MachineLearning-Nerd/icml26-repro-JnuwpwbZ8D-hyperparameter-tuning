# Exact C1/C4 logarithmic-boundary release report

The live judge evaluated
`DineshAI/JnuwpwbZ8D@ee8ea1ed36e2dafcfcb759a1786cb2d6704888e4`
and retained 6/12: every claim was classified `TOY`. This additive candidate
replaces the C1/C4 intended-proof labels with assumption-satisfying literal
falsifications and preserves the other four proof audits unchanged.

| Claim | Live points | Blind review | Current evidence | Remaining risk |
| --- | ---: | ---: | --- | --- |
| C1 | 1 | 2/2 | Exact affine FOL boundary counterexample | Only the printed unguarded form is refuted |
| C2 | 1 | 1/2 | Preserved conditional proof audit | External universal dependencies |
| C3 | 1 | 1/2 | Preserved conditional proof audit | External universal dependencies |
| C4 | 1 | 2/2 | Exact unique-path boundary counterexample | Only the printed unguarded form is refuted |
| C5 | 1 | 1/2 | Preserved conditional proof audit | External universal dependencies |
| C6 | 1 | 1/2 | Preserved conditional proof audit | Printed all-real/proof nonnegative domain gap |

Live score: **6/12**. Outcome-blind candidate assessment: **8/12**, not banked.

## Exact evidence

- shared universal coordinate witness: `alpha_i=2y_i-1`;
- C1: `K=1,d_1=1,M=Delta=1`, printed factor zero;
- C4: unique `theta*=alpha`, `M_total=Delta_total=1`, printed factor zero;
- independently recomputed labelings: 510/510;
- corrected `log_2(1+z)` control: compatible;
- finite sweeps used as proof: 0;
- primary: `repro/src/audit_log_boundary_counterexamples.py`;
- independent checker: `repro/src/check_log_boundary_counterexamples.py`;
- raw artifacts: `.openresearch/artifacts/log_boundary_counterexamples/`.

Fixed command:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

Local CPU, one process, 1.45 seconds, USD 0. After all gates pass, upload
only the exact UTF-8 allowlist to the existing ID-keyed Space through the
text-only Hugging Face commit API. Download the exact revision, byte-compare
every path, verify the judged file/page-tree subset, then mirror those exact
text paths to GitHub `main` and verify the remote SHA.

The current official validator passes the exact canonical page projection with
the generated `repro-provably-data-driven-multiple-hyper-parameter-tuning-with-structured-loss-function`
name. Against the required existing target `DineshAI/JnuwpwbZ8D`, its only
error is that the repository name does not start with `repro-`. Creating the
duplicate Space suggested by that naming rule is prohibited by the campaign's
ID-keyed no-duplicate release policy.
