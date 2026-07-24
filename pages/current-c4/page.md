# CURRENT — C4: explicit rational solution path

**Verdict: VERIFIED · confidence: HIGH**

Exact source contract (Assumption 7.1 and Theorem 7.2, main lines 537–555):
when every instance has a unique, uniformly piecewise-rational optimal path
and a piecewise-rational tuning objective,

`Pdim(L)=O(p log(M_total Delta_total))`,

where `M_total=M_path+T_path(M_k+T_k)` and
`Delta_total=Delta_k Delta_path`.

The certificate reconstructs the direct GJ decision computation: locate the
path piece, compose it with each objective boundary/value rational function,
and compare the resulting rational threshold. This bypasses quantifier
elimination exactly as claimed. The symbolic witness checks the log
composition and 128 independent complexity tuples check the counts.

The negative control uses a polynomial with minimizers `-1` and `1`; it is
rejected because Assumption 7.1 explicitly requires a singleton argmin.

- [Contract](../../.openresearch/artifacts/claim_4/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_4/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_4/raw_output.json)
- [Independent checker](../../.openresearch/artifacts/claim_4/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_4/negative_control_output.json)
- [Falsification route](../../.openresearch/artifacts/claim_4/falsification_route.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Limitations](../../.openresearch/artifacts/claim_4/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old three-piece self-composition is **Historical rejected baseline**.
