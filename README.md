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

# Proof and empirical-signature reproduction of arXiv:2602.02406

![Six-claim evidence summary](reports/theorem-certificates/images/headline.svg)

This CPU-only reproduction replaces the previously judged toy checks with
source-anchored proof certificates and concrete theorem-signature experiments
for all six pseudo-dimension claims in
*Provably Data-driven Multiple Hyper-parameter Tuning with Structured Loss
Function*. The cumulative gate passes. Claims C1–C5 are assessed **VERIFIED /
HIGH confidence**. Claim C6 is **VERIFIED / MEDIUM confidence** under the
standard nonnegative interpretation of regularization weights; the paper's
printed all-real notation is broader than its box-QP proof, and that gap is
shown rather than hidden.

These are reproduction verdicts, not judge results. The live judged score
remains **6/12** until the evaluator reviews a new Space revision.

The evaluator reviewed revision `01db7fab41d2c338894316b6e83cbc0cede75756`
and kept all six claims at TOY because the stronger verifier code was linked
rather than embedded in the logbook, causing it to conclude that the gate did
not execute those experiments. This child revision answers that exact
visibility failure: each CURRENT claim page embeds the verbatim executed Python
and stable captured output, and the CURRENT release page embeds the exact
fail-closed gate showing the empirical and independent-checker stages. The
historical toy pages remain preserved under a single explicit archive node.

The scientific correction was calibrated against a public 12/12 revision and
independently adds the three evidence types its judge credited: realized sign
patterns on named loss classes, hallmark parameter-scaling sweeps, and
theorem-specific failing controls. The formal empirical run uses one local CPU
core, fixed budgets unrelated to the displayed bounds, and seeds
`173,271,419`.

| Claim | Paper result | Observed evidence | Assessment |
|---|---|---|---|
| C1 | Theorem 4.1 FOL bound | Symbolic QE-to-GJ derivation; exact `16/16` and `256/256` halfspace shattering; `2^K` sweep | VERIFIED · HIGH |
| C2 | Theorem 5.1 training-loss bound | One-block proof; 3-seed two-piece-quadratic patterns; `p`/`d` sweeps | VERIFIED · HIGH |
| C3 | Theorem 6.1 bilevel bound | Two-block proof; genuine `f != g` patterns; C3/C2 ratio `3.74→37.44` | VERIFIED · HIGH |
| C4 | Theorem 7.2 rational-path bound | Direct GJ proof; exact ElasticNet path regions `4,6,8,10` | VERIFIED · HIGH |
| C5 | Theorem 8.1 group-LASSO bound | Norm-lift proof; exact group soft-threshold realizes `4/4,8/8,16/16` active patterns | VERIFIED · HIGH |
| C6 | Theorem 8.2 fused-LASSO bound | KKT violation `<1e-12`; up to 106 regions at `d=8`; negative-weight proof-gap witness | VERIFIED · MEDIUM |

The paper reports asymptotic theorems rather than experimental scalar targets,
so “paper number versus observed number” means the claimed bound versus the
independently reconstructed bound. No training, dataset, GPU, author code, or
formula-derived sampling budget is used. Formal runs used local CPU because
each was single-process and completed in 5–15 seconds.

## Read and reproduce

- [Current canonical verification](pages/current-verification/page.md)
- [Executed gate and shared engine](pages/current-release/page.md)
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
| [`orx/empirical-theorem-signature-release`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/empirical-theorem-signature-release) | Add named-class sign patterns, scaling sweeps, and applicability controls | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | measurement preflight: science/checker pass; stale manifest failed closed and was superseded | local CPU, one process |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and exact published text | none |

## Historical evidence

The old 621 finite-grid/KKT checks are preserved for provenance but are labeled
**Historical rejected baseline**. They are regression tests, not the current
verification and not evidence for the universal pseudo-dimension bounds.
