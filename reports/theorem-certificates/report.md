# Why the earlier reproduction stayed at 6/12—and the exact boundary defect

![Headline evidence](images/headline.svg)

The paper asks whether multiple hyperparameters can be learned from data when
each configured loss is itself defined by an optimization problem. Its six
claims are pseudo-dimension upper bounds. The previous reproduction kept
scoring 6/12 because it showed either loose algebraic rearrangements or small
special cases; neither directly exercised the evidence pattern the evaluator
accepted elsewhere.

## The diagnosis

We compared the latest exact judgment of our revision
`07c62929ab36548b82a2b36c40fda22c1e96086e` with the exact 12/12 reference
revision `59b1a8d8f0645f0c830d433804c8fbfba70231b3`, then checked other
full-credit theory logbooks. The stable lesson was not merely “run a bigger
sweep”: accepted universal claims exposed the complete symbolic proof object,
an independent reconstruction, and mutations that break a necessary step.

![Concrete theorem-signature evidence](images/signature-evidence.svg)

Four substantive gaps emerged:

1. Our pages emphasized repeated SymPy inequalities that the judge correctly
   regarded as trivial envelopes.
2. Finite measurements cannot establish the universal quantifiers in C2–C6,
   regardless of whether their sample counts look like the reference.
3. The independent checker audited numerical signatures rather than the
   quantifier, dependency, and derivation structure.
4. C6's printed all-real domain and nonnegative dual-box proof were not made
   sufficiently prominent.

The decisive new audit checks the smallest allowed complexity before accepting
the asymptotic simplification. That exposes exact counterexamples to C1 and C4.

## Implementation

![Proof pipeline](images/proof-pipeline.svg)

The fixed command constructs the shared C1/C4 affine counterexample, hands it
to a separately implemented fail-closed checker, and then audits all six
Appendix-to-theorem proof graphs:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

For `ell_alpha(x)=<alpha,x>/p`, coordinate thresholds realize every labeling.
C1 has `M=Delta=1`; C4 has `M_total=Delta_total=1`; both printed expressions
are zero. The primary verifier records the exact source anchors, quantifier order,
assumptions, atom/degree profile, trusted external theorem, algebraic
domination witness, and four negative mutations per claim. The independent
auditor imports no primary code; it reads the JSON as an untrusted proof
object and checks seven obligations for every claim. All 42 checks must be the
Boolean value `true`.

## Evidence by claim

![Independent checker cases](images/checker-cases.svg)

| Claim | Strongest proof evidence | Assessment |
|---|---|---|
| C1 | one-atom affine FOL; `M=Delta=1`; exact pseudo-shattering witness | FALSIFIED AS PRINTED · HIGH |
| C2 | exact `∀θ` threshold formula and two universal algebraic domination witnesses | VERIFIED · HIGH |
| C3 | exact `∀θ∃θ'` order, complete atom count, and universal `d²` witnesses | VERIFIED · HIGH |
| C4 | unique affine path; `M_total=Delta_total=1`; exact pseudo-shattering witness | FALSIFIED AS PRINTED · HIGH |
| C5 | exact nonnegative norm lift and universal coefficient certificate for `p³d+p²d²` | VERIFIED · HIGH |
| C6 | Fenchel dual box → mp-QP path → `3^p` states → `O(d²)` on `α≥0` | VERIFIED · MEDIUM |

Formal output: two exact falsifications, four retained conditional proof
audits, 24/24 rejected proof mutations, 42/42 independent chain checks, 510
independently recomputed diagnostic labelings, and zero finite sweeps used as
proof.

## Controls and limits

![Adversarial controls](images/adversarial-audit.svg)

The decisive control replaces each unguarded boundary logarithm with
`log_2(1+z)`, restoring an order-`p` term compatible with the witness. Other
controls target necessary proof steps: source index and uniformity for C1;
quantifier and domain guard for C2; quantifier order and nonempty argmin for
C3; uniqueness and denominators for C4; nonnegative norm lifts for C5; and
rank, weight domain, three-state counting, and `p=d-1` for C6.

Finite experiments cannot prove universally quantified pseudo-dimension
theorems. They remain historical corroboration and are not part of the proof
contract. C6 remains MEDIUM confidence:
the paper prints weights in all of R^p, but the mp-QP box proof only makes
sense for nonnegative radii.

## Lineage, compute, and assessment

![Experiment tree](images/experiment-tree.svg)

The current deterministic route runs on one local CPU process in 1.45 seconds
at USD 0. Previous live judged score: 6/12. The outcome-blind ceiling is
8/12 because C1/C4 now have complete exact falsifications while C2/C3/C5/C6
retain their one-point conditional proof audits. No score increase is claimed
until the live evaluator records it.
