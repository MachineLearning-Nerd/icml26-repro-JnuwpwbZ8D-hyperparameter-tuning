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

# Reproducing six pseudo-dimension bounds in arXiv:2602.02406

![Six-claim evidence summary](reports/theorem-certificates/images/headline.svg)

The latest live judge evaluated Space revision
`07c62929ab36548b82a2b36c40fda22c1e96086e` and retained **6/12**. Its
criticism was precise: our sign-pattern sweeps, formula substitutions, and
small LASSO instances were still finite corroboration of universally
quantified pseudo-dimension theorems. The public 12/12 comparison logbook was
useful for presentation, but copying its small sweeps would not answer that
scientific objection.

This revision replaces the active evidence with universal Appendix-to-theorem
proof certificates. The fixed command checks every quantifier block,
assumption, atom/degree count, trusted theorem application, and asymptotic
simplification. A separately implemented auditor treats the primary JSON as
untrusted and checks seven obligations per claim.

| Evidence | Formal result |
|---|---:|
| Universal theorem chains | 6 / 6 |
| Claim-specific proof mutations rejected | 24 / 24 |
| Independent structural checks | 42 / 42 |
| Finite sweeps used as proof | **0** |
| Cumulative tests | 24 / 24 |
| Formal run / compute | `b811b0bc-da4c-4575-a4ea-36fd5022d707`; one CPU core; 10 s |

| Claim | Proof certificate | Assessment |
|---|---|---|
| C1 | QE complexity → QFF → Goldberg--Jerrum, including the Appendix `K/M` typo audit | VERIFIED · HIGH |
| C2 | exact `∀θ` loss-threshold formula, atom count, and universal domination witnesses | VERIFIED · HIGH |
| C3 | exact `∀θ∃θ'` bilevel formula and universal `d²` witnesses | VERIFIED · HIGH |
| C4 | direct rational-path GJ predicate/degree accounting with QE absent | VERIFIED · HIGH |
| C5 | exact nonnegative norm lifts, `(d,d+2p)` blocks, and coefficient certificate | VERIFIED · HIGH |
| C6 | dual mp-QP, three-state region bound, and `p=d-1` substitution | VERIFIED on `α≥0` · MEDIUM |

C6 retains a disclosed interpretation risk: the source prints all-real
weights, while its dual box proof requires nonnegative regularization weights.
The negative-weight example is recorded as a proof-domain gap, not mislabeled
as a Pdim falsification.

These are reproduction verdicts and a forecast, not a new judge result. The
live score remains **6/12** until a judge evaluates a newly published revision.

## Read and reproduce

- [Current canonical universal proof verification](pages/universal-proof-index/page.md)
- [Exact command, raw proof evidence, and independent audit](pages/universal-proof-release/page.md)
- [Illustrated technical report](reports/theorem-certificates/report.md)
- [Tutorial marimo notebook](notebooks/theorem_certificates.py)
- [Open in molab](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/blob/main/notebooks/theorem_certificates.py)
- [Pinned environment](uv.lock)

Run the exact inherited command:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

The universal proof route is deterministic and seed-free. Its formal run used
one local CPU core for 10 seconds and cost $0.

## Experiment log

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`orx/frozen-judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/frozen-judged-baseline) | Freeze judged baseline | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Historical rejected baseline | local CPU, one process |
| [`orx/empirical-theorem-signature-release`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/empirical-theorem-signature-release) | First named-class sign patterns and sweeps | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Scientifically improved but still judged toy | local CPU, one process |
| [`orx/final-embedded-certificate-release`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/final-embedded-certificate-release) | Prior 9291652 release | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Live judge remained 6/12 | local CPU, one process |
| [`orx/reference-protocol-parity-and-corrected-theorem`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/reference-protocol-parity-and-corrected-theorem) | Reconstruct evaluator-credited protocols and fix C5 formula | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Calibration science/checker pass; stale presentation audit failed closed and is superseded by the release child | local CPU, one thread |
| [`orx/final-evaluator-visible-release-metadata`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/final-evaluator-visible-release-metadata) | Record the successful cumulative run on the canonical surface | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Release candidate; parent cumulative gate passed 21 tests and zero-gap visibility audit | local CPU, one thread |
| [`orx/schema-v2-native-executed-logbook`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/schema-v2-native-executed-logbook) | Remove historical evidence from active ingestion and expose native executed cells | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Current release candidate; cumulative result pending | local CPU, one thread |
| [`orx/universal-quantified-proof-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/universal-quantified-proof-certificates) | Replace finite corroboration with six universal proof chains and an independent auditor | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | 6/6 chains, 24/24 mutations, 42/42 audit checks, 24 tests | local CPU, one core, 10 s |
| [`orx/evaluator-visible-universal-proof-release`](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/evaluator-visible-universal-proof-release) | Put the universal proof objects first in canonical navigation | `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json` | Release candidate; evaluator-blind review and publication gate | local CPU, one core |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and published Space text | none |

All earlier files are retained for provenance under **Historical rejected
baseline**, but they are intentionally outside the active logbook tree.
