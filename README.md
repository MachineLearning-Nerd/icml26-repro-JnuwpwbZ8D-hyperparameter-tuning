# JnuwpwbZ8D — Provably Data-driven Multiple Hyper-parameter Tuning with Structured Loss Function

This CPU-only, clean-room reproduction checks all six anchored claims in
[arXiv:2602.02406](https://arxiv.org/abs/2602.02406). The theorem evidence has
no author-code or experimental-data dependency, so the artifact uses an
independent deterministic verifier rather than a training proxy.

## Result

`outputs/publication_gate.json` passes with six claims and two tests. The
verifier performs 621 finite exact checks: 96 formula substitutions for the
first-order framework; 189 training-loss and 75 validation-loss logical
equivalences; 300 piecewise-rational compositions; 15 group-LASSO KKT checks;
and 153 fused-LASSO KKT/path checks. It also rejects three deliberately wrong
constructions: dropping Theorem 4.1's `d_k + 1` factor, allowing negative
group-norm lift variables, and using the wrong fused-LASSO breakpoint.

## Pinned primary material

- `source/arxiv-2602.02406.tar` — SHA-256:
  `d76346a46f73a00a941694d1a2676f8e4e0611bf01b339edb7fd08e294ceb4fd`
- `source/icml2026.tex` — SHA-256:
  `5c7260856bcaf8554196716d0dc1ebfc69ebab1684893207b938e93d601754ef`
- `source/icml_appendix.tex` — SHA-256:
  `3551432784412496e3f3ffac96272de1745b8b6e4c4a1afd0c79c606dc37068f`

## Re-run

```bash
uv venv --python 3.12 .venv
.venv/bin/python repro/src/verify_hyperparameters.py --output outputs/verification.json
.venv/bin/python -m unittest discover -s repro/tests -v
.venv/bin/python repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

The verifier uses the Python standard library only. It does not import or
execute the paper source.
