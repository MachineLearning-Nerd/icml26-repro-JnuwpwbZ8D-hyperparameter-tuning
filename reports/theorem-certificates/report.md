# From toy checks to proof certificates: reproducing six pseudo-dimension bounds

![Headline evidence](images/headline.svg)

The paper asks whether several hyperparameters can be selected from data even
when the tuned loss is defined by an optimization problem. Its six headline
claims are asymptotic pseudo-dimension bounds. That matters for reproduction:
running LASSO on a few points cannot verify a theorem quantified over whole
function classes. The useful unit of evidence is instead a source-anchored,
machine-checkable derivation with adversarial controls.

## What changed

The judged artifact earned 6/12 because every claim had only toy evidence:
formula substitution, finite-grid logical identities, or small KKT checks.
Those files remain intact for provenance. The new code path reconstructs the
paper's logical reductions, checks their atom counts and degrees, mechanically
proves the asymptotic absorptions, and separately searches for
assumption-satisfying counterexamples.

![Proof pipeline](images/proof-pipeline.svg)

The core implementation is deliberately small:

```python
specializations = symbolic_witnesses()
assert specializations["all_symbolic_witnesses_passed"]
assert all(not row["falsification_succeeded"] for row in audits.values())
```

The fixed command runs this path, every negative control, and the old suite:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

## Evidence by claim

![Independent checker cases](images/checker-cases.svg)

| Claim | Paper claim | Reconstructed evidence | Assessment |
|---|---|---|---|
| C1 | `O(p D+ log M + p² D log Delta)` | QE-to-GJ symbolic expansion; 384 independent cases | VERIFIED · HIGH |
| C2 | `O(pd log M_f+... +p²d log Delta_f)` | exact one-block atom count and coefficient proof | VERIFIED · HIGH |
| C3 | `O(pd² log M_tot+p²d² log Delta_tot)` | exact two-block formula; `T_f²` handled inside log | VERIFIED · HIGH |
| C4 | `O(p log(M_total Delta_total))` | direct rational-path GJ decision computation | VERIFIED · HIGH |
| C5 | `O(p³d+p²d²)` | nonnegative norm lift and two-block symbolic reduction | VERIFIED · HIGH |
| C6 | `O(d²)` | `3^(d-1)` active-state path for nonnegative weights | VERIFIED · MEDIUM |

The case counts are not used to infer the theorem. They are independent
regression checks around proof-level symbolic certificates.

## Adversarial audit

![Adversarial controls](images/adversarial-audit.svg)

Four different failure modes were tested. An unattained compact-domain
infimum makes C2/C3's written `min` loss undefined, so it exposes an implicit
attainment premise but is not falsification. A two-minimizer path violates
C4's explicit uniqueness assumption. Signed group weights do not break C5's
norm lift because `nu>=0` selects the correct square root.

C6 is the important exception. The paper writes `alpha in R^p`, yet derives a
dual box `|u_i|<=alpha_i`. For a negative coordinate that box is empty. In the
full-rank primal example `A=I, b=0, d=2, alpha=-2`, two global minimizers occur
at `(-2,2)` and `(2,-2)`, value `-4`. This defeats the claimed proof route on
the literal all-real domain. It does not establish that the `O(d²)` bound is
false, so the result remains MEDIUM confidence under the intended
nonnegative-weight interpretation.

## Experiment lineage and cost

![Experiment tree](images/experiment-tree.svg)

The tree froze the judged baseline, branched a positive-certificate route and
an adversarial route, merged both only on a new child, then strengthened the
winner with symbolic coefficient witnesses. Eight formal local CPU runs used
80 seconds total, including one 10-second fixture mismatch that failed closed.
Every workload was single-process and confidently below five minutes, so the
authorized Hugging Face `cpu-upgrade` threshold was never crossed. Total cost:
$0 local and $0 Hugging Face.

## Assessment

Claims C1–C5 are VERIFIED with HIGH confidence. C6 is VERIFIED with MEDIUM
confidence under the standard nonnegative meaning of regularization weights;
its source-domain gap is evaluator-visible. The conservative post-change
forecast is 10–12/12, and 12/12 is only the best-supported possible forecast.
The live score remains 6/12 until a judge records a new Space revision.

Important branches: [frozen baseline](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/frozen-judged-baseline),
[certificate route](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/c2-c6-specialization-certificates),
[adversarial route](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/c2-c6-counterexample-audits), and
[winning symbolic route](https://github.com/MachineLearning-Nerd/icml26-repro-JnuwpwbZ8D-hyperparameter-tuning/tree/orx/symbolic-asymptotic-witnesses).
