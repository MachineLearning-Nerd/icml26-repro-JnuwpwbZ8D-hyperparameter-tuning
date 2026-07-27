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

## Exact weighted group-LASSO evidence

The concrete solver uses the exact orthogonal-block solution
`theta_g*=(1-alpha_g/||z_g||)_+ z_g`. With 5,000 weight vectors for each of
three seeds, it realizes every binary group-active pattern: `4/4`, `8/8`, and
`16/16` at `(p,d)=(2,4),(3,6),(4,8)`. Independent `p` and `d` sweeps reproduce
the `p³d+p²d²` signature. This evidence is paired with the symbolic norm-lift
certificate above; finite active patterns alone are not treated as a proof.
The non-semi-algebraic `sin(||theta_g||)` control is rejected as inapplicable.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_5/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_5/signature_checker.json)

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
