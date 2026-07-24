# CURRENT — C5: weighted group LASSO

**Verdict: VERIFIED · confidence: HIGH**

Exact mathematical contract (Theorem 8.1, main lines 566–596): the bounded,
well-defined weighted-group-LASSO bilevel loss class has

`Pdim(L)=O(p³d+p²d²)`.

The proof certificate represents every group norm with
`nu_i²=sum_j theta_ij²` **and** `nu_i>=0`, then uses two quantified blocks of
dimensions `d` and `d+2p`. SymPy verifies
`log(2+4p)<=2p`, the block-dimension bounds, and an explicit coefficient
witness `derived <=16(p³d+p²d²)` for positive integer `p,d`. The independent
route covers 12 widely separated tuples.

The signed-weight audit confirms the nonnegative lift equals the group norm for
`alpha=-7,-1,0,2,11`. The failing control omits `nu>=0`, which admits the wrong
root and changes the objective.

- [Contract](../../.openresearch/artifacts/claim_5/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_5/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_5/raw_output.json)
- [Independent checker](../../.openresearch/artifacts/claim_5/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_5/negative_control_output.json)
- [Falsification route](../../.openresearch/artifacts/claim_5/falsification_route.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Limitations](../../.openresearch/artifacts/claim_5/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old 15 KKT instances are **Historical rejected baseline**.
