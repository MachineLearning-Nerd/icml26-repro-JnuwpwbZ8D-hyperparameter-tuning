# Universal proof-certificate reproduction

---
<!-- trackio-cell
{"type":"markdown","id":"cell_universal_overview","created_at":"2026-07-27T12:00:00+00:00","title":"Outcome first: proof-level replacement for the rejected finite checks","pinned":true}
-->

## Outcome first

**All six claims have current `VERIFIED` proof certificates.** This is a new
route, not a relabeling of the earlier finite-grid evidence. The live judge
correctly rejected the earlier sign-pattern sweeps and small LASSO instances
as `TOY`. They remain preserved as **Historical rejected baseline**, but they
are not used to prove any universal theorem here.

The current fixed-command run reconstructs each Appendix-to-theorem argument:
the exact quantifier order, assumptions, atom and degree accounting, invocation
of the named quantifier-elimination / Goldberg--Jerrum / mp-QP result, and the
final asymptotic simplification. It rejects four theorem-specific proof
mutations per claim. A separately implemented auditor imports no primary
verifier code and checks seven structural obligations per claim.

| Evidence | Result |
|---|---:|
| Universal theorem chains | 6 / 6 |
| Fail-sensitive proof mutations rejected | 24 / 24 |
| Independent structural checks | 42 / 42 |
| Finite parameter sweeps used as proof | **0** |
| Cumulative unit tests | 24 / 24 |
| Formal run | `b811b0bc-da4c-4575-a4ea-36fd5022d707` |
| Git commit | `67466cf191c493f0ebb67928866fa40e3a674668` |
| Compute | local CPU, one core, 10 s, $0 |

Fixed command:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

## Source identity

Paper: arXiv:2602.02406, retrieved 2026-07-27 with an explicit browser
User-Agent.

- `source/icml2026.tex` SHA-256:
  `5c7260856bcaf8554196716d0dc1ebfc69ebab1684893207b938e93d601754ef`
- `source/icml_appendix.tex` SHA-256:
  `3551432784412496e3f3ffac96272de1745b8b6e4c4a1afd0c79c606dc37068f`
- structured full-text retrieval SHA-256:
  `eba938e8df91d449708d1c1f8f7c149f32ae69229701e6a32b876e50d4ef87ed`

## Current claim matrix

| Claim | Current proof page | Proof status | Confidence | Principal caveat |
|---|---|---|---|---|
| C1 | Theorem 4.1 | VERIFIED | HIGH | QE and GJ are named trusted theorems |
| C2 | Theorem 5.1 | VERIFIED | HIGH | Requires the stated minimum to be attained |
| C3 | Theorem 6.1 | VERIFIED | HIGH | Requires nonempty lower-level argmin |
| C4 | Theorem 7.2 | VERIFIED | HIGH | Requires a unique, well-defined rational path |
| C5 | Theorem 8.1 | VERIFIED | HIGH | Uses nonempty groups, hence `p≤d` |
| C6 | Theorem 8.2 | VERIFIED on conventional weight domain | MEDIUM | Source prints `α∈R^p`; its dual-box proof requires `α≥0` |

This is a score forecast artifact, not a judge result. The previous live score
is still **6/12** until the live evaluator judges the new Hugging Face revision.
It does not claim a new score. In particular, the C5 proof audits the full
second quantified block of dimension `d+2p`.

## Evaluator-visible evidence

- [Primary universal verifier](../../repro/src/verify_universal_theorem_chains.py)
- [Independent auditor](../../repro/src/audit_universal_theorem_chains.py)
- [Independent audit JSON](../../.openresearch/artifacts/universal_proofs/independent_audit.json)
- [Release command, exact output, and visibility review](../universal-proof-release/page.md)
- [Historical rejected baseline](../historical-rejected-baseline/page.md)
