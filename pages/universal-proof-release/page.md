# Fixed run, independent audit, and release visibility

---
<!-- trackio-cell
{"type":"code","id":"cell_universal_run","created_at":"2026-07-27T12:00:00+00:00","title":"Run: fixed cumulative publication gate (exit 0)","command":["uv","run","--frozen","--python","3.12","repro/src/run_publication_gate.py","--output","outputs/publication_gate.json"],"exit_code":0,"duration_s":10.0}
-->

```bash
$ uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

exit 0 · 10.0s

Formal OpenResearch run:
`b811b0bc-da4c-4575-a4ea-36fd5022d707`, commit
`67466cf191c493f0ebb67928866fa40e3a674668`, local CPU, one allocated core,
$0. The pre-run estimate was one core and under one minute.

## Exact gate output

```output
UNIVERSAL_PROOF_RESULT={"all_universal_proof_chains_passed": true, "claims": 6, "finite_sweeps_used_as_proof": 0, "mutations_rejected": 24, "verdicts": {"C1": "VERIFIED", "C2": "VERIFIED", "C3": "VERIFIED", "C4": "VERIFIED", "C5": "VERIFIED", "C6": "VERIFIED"}}
UNIVERSAL_PROOF_AUDIT={"claims": 6, "finite_sweeps_used_as_proof": 0, "independent_audit_passed": true, "independent_checks": 42}
Ran 24 tests in 0.169s
OK
{"claims_passed": 6, "current_exact_claims": {"C1": "VERIFIED", "C2": "VERIFIED", "C3": "VERIFIED", "C4": "VERIFIED", "C5": "VERIFIED", "C6": "VERIFIED"}, "publication_gate_passed": true, "tests_passed": true, "universal_theorem_proofs": {"audit_passed": true, "claims": 6, "finite_sweeps_used_as_proof": 0, "independent_checks": 42, "mutations_rejected": 24}}
```

## Independent implementation

The [independent auditor](../../repro/src/audit_universal_theorem_chains.py)
does not import the [primary verifier](../../repro/src/verify_universal_theorem_chains.py).
It treats the primary JSON as an untrusted proof object, reconstructs expected
source-anchor tokens, quantifier manifests, derivation edges, and
claim-specific mutation classes, and requires every exact check to be the
Boolean value `true`.

[Download the exact audit JSON](../../.openresearch/artifacts/universal_proofs/independent_audit.json).

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| C1 | universal-proof-c1 | yes | yes | yes | 7/7 | 4 mutations | yes | VERIFIED |
| C2 | universal-proof-c2 | yes | yes | yes | 7/7 | 4 mutations | yes | VERIFIED |
| C3 | universal-proof-c3 | yes | yes | yes | 7/7 | 4 mutations | yes | VERIFIED |
| C4 | universal-proof-c4 | yes | yes | yes | 7/7 | 4 mutations | yes | VERIFIED |
| C5 | universal-proof-c5 | yes | yes | yes | 7/7 | 4 mutations | yes | VERIFIED |
| C6 | universal-proof-c6 | yes | yes | yes | 7/7 | 4 mutations | yes, `α≥0` domain explicit | VERIFIED / MEDIUM |

Historical files remain byte-preserved and reachable, but none is the current
verifier. The proof pages above supersede the finite-grid and empirical
signature pages.

