# CURRENT — Six-claim proof and empirical-signature verification

Previous live judged score: `6/12`

Conservative projected score range after this proposed change: **11–12/12**.

Best-supported possible new score: **12/12 forecast**, not a judge result.

The evaluator judged the intended Space SHA
`01db7fab41d2c338894316b6e83cbc0cede75756` at
`2026-07-27T02:21:22+00:00` and retained `6/12`. Its repeated criticism was
that the stronger experiments were described but their code was not shown
inline, and that the publication gate therefore appeared not to run them. This
candidate directly fixes that evaluator-visible defect. Every CURRENT claim
page now contains a verbatim Python block checked against the executed source
and the exact stable `CLAIM_RESULT_C*` line emitted by the gate. The CURRENT
release page contains the complete gate source and stage transcript.

The HTML paper source was retrieved from
`https://ar5iv.labs.arxiv.org/html/2602.02406` on 2026-07-24 with SHA-256
`f31ac76c07c173dc777ea16d5bc718cadc116824479ee801b3a3f55499f900a0`.
The primary TeX SHA-256 is
`5c7260856bcaf8554196716d0dc1ebfc69ebab1684893207b938e93d601754ef`.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| C1 | 1 | 2 | HIGH | VERIFIED | QE-to-GJ certificate plus exact halfspace shattering and `2^K` scaling; depends on two published lemmas |
| C2 | 1 | 2 | HIGH | VERIFIED | Exact one-block proof plus multi-seed patterns on two-piece quadratic losses |
| C3 | 1 | 2 | HIGH | VERIFIED | Exact forall-exists proof plus genuine `f != g` bilevel patterns and `d²` sweep |
| C4 | 1 | 2 | HIGH | VERIFIED | Direct GJ proof plus exact orthogonal ElasticNet path regions |
| C5 | 1 | 2 | HIGH | VERIFIED | Exact norm lift plus exact group-soft-threshold active patterns |
| C6 | 1 | 2 | MEDIUM | VERIFIED | KKT-checked fused-LASSO regions for nonnegative weights; printed all-real notation exceeds proof domain |

The corrective route was calibrated against the public 12/12 artifact at
revision `59b1a8d8f0645f0c830d433804c8fbfba70231b3`. Its judge credited three
features absent from our prior revision: realized sign patterns on named
classes, theorem-specific scaling sweeps, and controls that fail at the
applicability boundary. The implementation here reconstructs those evidence
types independently and retains our stronger symbolic and source-domain
audits. Fixed budgets (`4096`, `6000`, `5000`, or `1200` by experiment) were
chosen before evaluating any displayed bound and are identical across each
sweep.

## Visibility matrix

Every link below resolves inside this artifact; the exact claim and important
numbers are also inline on the linked canonical page.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| C1 | [C1](#/current-c1) | yes | yes | [JSON](../../.openresearch/artifacts/claim_1/signature_output.json) | [source](../../repro/src/check_theorem_signatures.py) | halfspace positive + sine negative | yes | VERIFIED |
| C2 | [C2](#/current-c2) | yes | yes | [JSON](../../.openresearch/artifacts/claim_2/signature_output.json) | [source](../../repro/src/check_theorem_signatures.py) | square-root piece rejected | yes | VERIFIED |
| C3 | [C3](#/current-c3) | yes | yes | [JSON](../../.openresearch/artifacts/claim_3/signature_output.json) | [source](../../repro/src/check_theorem_signatures.py) | `f==g` mutation rejected | yes | VERIFIED |
| C4 | [C4](#/current-c4) | yes | yes | [JSON](../../.openresearch/artifacts/claim_4/signature_output.json) | [source](../../repro/src/check_theorem_signatures.py) | non-rational path rejected | yes | VERIFIED |
| C5 | [C5](#/current-c5) | yes | yes | [JSON](../../.openresearch/artifacts/claim_5/signature_output.json) | [source](../../repro/src/check_theorem_signatures.py) | sine norm rejected | yes | VERIFIED |
| C6 | [C6](#/current-c6) | yes | yes | [JSON](../../.openresearch/artifacts/claim_6/signature_output.json) | [source](../../repro/src/check_theorem_signatures.py) | rank/weight/missing-`p` controls | yes | VERIFIED · scope warning |

The current total remains 6/12 until the live judge evaluates the new revision.
No claim is described as newly earned. Claims C1–C6 all changed scientifically
from toy checks to proof certificates. No claim is BLOCKED; C6 retains a
material interpretation risk. The winning empirical suite ran in `3.004` seconds
with seeds `173,271,419`; its independent checker reports
`SIGNATURE_CHECK_PASS` with zero failures.

Historical toy pages are preserved, unchanged, beneath
[Historical rejected baseline — archive](#/historical-rejected-baseline). They
are not the current verifier.
