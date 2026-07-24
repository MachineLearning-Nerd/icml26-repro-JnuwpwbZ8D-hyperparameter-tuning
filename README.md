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

# Proof-certificate reproduction of arXiv:2602.02406

![Six-claim evidence summary](reports/theorem-certificates/images/headline.svg)

This CPU-only reproduction replaces the previously judged toy checks with
source-anchored proof certificates for all six pseudo-dimension claims in
*Provably Data-driven Multiple Hyper-parameter Tuning with Structured Loss
Function*. The cumulative gate passes. Claims C1–C5 are assessed **VERIFIED /
HIGH confidence**. Claim C6 is **VERIFIED / MEDIUM confidence** under the
standard nonnegative interpretation of regularization weights; the paper's
printed all-real notation is broader than its box-QP proof, and that gap is
shown rather than hidden.

These are reproduction verdicts, not judge results. The live judged score
remains **6/12** until the evaluator reviews a new Space revision.

| Claim | Paper result | Observed evidence | Assessment |
|---|---|---|---|
| C1 | Theorem 4.1 FOL bound | Symbolic QE-to-GJ derivation; 384 independent coefficient cases; 3 mutations rejected | VERIFIED · HIGH |
| C2 | Theorem 5.1 training-loss bound | One-block FOL certificate; symbolic atom/dimension witnesses; 64 independent cases | VERIFIED · HIGH |
| C3 | Theorem 6.1 bilevel bound | Two-block FOL certificate including the `T_f²` atom term; 128 independent cases | VERIFIED · HIGH |
| C4 | Theorem 7.2 rational-path bound | Direct GJ composition certificate; 128 complexity tuples; uniqueness control | VERIFIED · HIGH |
| C5 | Theorem 8.1 group-LASSO bound | Nonnegative norm-lift certificate and explicit asymptotic witness; 12 coefficient cases | VERIFIED · HIGH |
| C6 | Theorem 8.2 fused-LASSO bound | Active-state certificate for nonnegative weights; negative-weight proof-gap witness | VERIFIED · MEDIUM |

The paper reports asymptotic theorems rather than experimental scalar targets,
so “paper number versus observed number” means the claimed bound versus the
independently reconstructed bound. No training, dataset, GPU, author code, or
formula-derived sampling budget is used. Formal runs used local CPU because
each was single-process and completed in 5–15 seconds.

## Read and reproduce

- [Current canonical verification](pages/current-verification/page.md)
- [Illustrated technical report](reports/theorem-certificates/report.md)
- [Tutorial marimo notebook](notebooks/theorem_certificates.py)
- [Open in molab](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/blob/main/notebooks/theorem_certificates.py)
- [Pinned environment](uv.lock)

Run the exact inherited command:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

## Experiment log

All formal nodes inherit that exact command; hyperparameters are not smuggled
through command-line changes.

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`orx/frozen-judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/frozen-judged-baseline) | Freeze judged toy baseline | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Historical rejected baseline; pass, 5s | local CPU, one process |
| [`orx/c1-symbolic-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/c1-symbolic-proof-certificate) | C1 symbolic certificate | same exact command above | pass, 15s | local CPU, one process |
| [`orx/c2-c6-specialization-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/c2-c6-specialization-certificates) | C2–C6 theorem reductions | same exact command above | corrected fixture then pass, 10s | local CPU, one process |
| [`orx/c2-c6-counterexample-audits`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/c2-c6-counterexample-audits) | Assumption-aware adversarial audit | same exact command above | pass; C6 proof-domain gap found, 10s | local CPU, one process |
| [`orx/symbolic-asymptotic-witnesses`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/symbolic-asymptotic-witnesses) | Winning cumulative proof route | same exact command above | 11 tests pass, 10s | local CPU, one process |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and exact published text | none |

## Historical evidence

The old 621 finite-grid/KKT checks are preserved for provenance but are labeled
**Historical rejected baseline**. They are regression tests, not the current
verification and not evidence for the universal pseudo-dimension bounds.
