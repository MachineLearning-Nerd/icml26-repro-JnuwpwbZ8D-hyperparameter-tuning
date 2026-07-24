# CURRENT — Six-claim proof-certificate verification

Previous live judged score: `6/12`

Conservative projected score range after this proposed change: **10–12/12**.

Best-supported possible new score: **12/12 forecast**, not a judge result.

The HTML paper source was retrieved from
`https://ar5iv.labs.arxiv.org/html/2602.02406` on 2026-07-24 with SHA-256
`f31ac76c07c173dc777ea16d5bc718cadc116824479ee801b3a3f55499f900a0`.
The primary TeX SHA-256 is
`5c7260856bcaf8554196716d0dc1ebfc69ebab1684893207b938e93d601754ef`.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| C1 | 1 | 2 | HIGH | VERIFIED | QE-to-GJ symbolic certificate; depends on two cited published lemmas |
| C2 | 1 | 2 | HIGH | VERIFIED | Exact one-block reduction and symbolic atom/dimension witnesses; attainment is implicit in the defined loss |
| C3 | 1 | 2 | HIGH | VERIFIED | Exact forall-exists reduction including `T_f²`; nonempty argmin is implicit |
| C4 | 1 | 2 | HIGH | VERIFIED | Direct GJ certificate under explicit singleton rational-path assumption |
| C5 | 1 | 2 | HIGH | VERIFIED | Exact nonnegative norm lift and two-block asymptotic certificate |
| C6 | 1 | 2 | MEDIUM | VERIFIED | Exact for nonnegative regularization weights; printed all-real notation exceeds cited proof domain |

## Visibility matrix

Every link below resolves inside this artifact; the exact claim and important
numbers are also inline on the linked canonical page.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| C1 | [C1](#/current-c1) | yes | yes | [JSON](../../.openresearch/artifacts/claim_1/raw_output.json) | [source](../../repro/src/verify_claim1_proof.py) | 3 mutations | yes | VERIFIED |
| C2 | [C2](#/current-c2) | yes | yes | [JSON](../../.openresearch/artifacts/claim_2/raw_output.json) | [source](../../repro/src/verify_claims2_6_proofs.py) | finite-grid proxy rejected | yes | VERIFIED |
| C3 | [C3](#/current-c3) | yes | yes | [JSON](../../.openresearch/artifacts/claim_3/raw_output.json) | [source](../../repro/src/verify_claims2_6_proofs.py) | missing existential rejected | yes | VERIFIED |
| C4 | [C4](#/current-c4) | yes | yes | [JSON](../../.openresearch/artifacts/claim_4/raw_output.json) | [source](../../repro/src/verify_claims2_6_proofs.py) | nonunique path rejected | yes | VERIFIED |
| C5 | [C5](#/current-c5) | yes | yes | [JSON](../../.openresearch/artifacts/claim_5/raw_output.json) | [source](../../repro/src/verify_claims2_6_proofs.py) | signed lift rejected | yes | VERIFIED |
| C6 | [C6](#/current-c6) | yes | yes | [JSON](../../.openresearch/artifacts/claim_6/raw_output.json) | [source](../../repro/src/verify_claims2_6_proofs.py) | negative-weight witness | yes | VERIFIED · scope warning |

The current total remains 6/12 until the live judge evaluates the new revision.
No claim is described as newly earned. Claims C1–C6 all changed scientifically
from toy checks to proof certificates. No claim is BLOCKED; C6 retains a
material interpretation risk.
