# CURRENT — C2: training-loss pseudo-dimension

**Verdict: VERIFIED · confidence: HIGH**

Exact source contract (Theorem 5.1, main lines 423–428): uniformly
`(M_f,T_f,Delta_f)` piecewise-polynomial training objectives on the stated box
domains induce

`Pdim(L)=O(pd log(M_f+T_f+d)+p²d log Delta_f)`.

The checker constructs the one-universal-block threshold formula, counts
exactly `M_f+T_f+2d` atoms, and specializes C1 with `d_1=d`. SymPy proves
`d+1<=2d` and `M_f+T_f+2d<=2(M_f+T_f+d)` for positive integer dimensions.
The independent route covers 64 structural tuples. No sample count is chosen
from the claimed formula.

The adversarial route constructs a discontinuous piecewise-polynomial function
on `[0,1]` whose infimum is unattained. It is not a counterexample because the
source writes a real-valued `min` loss; it exposes that attainment is implicit.

- [Contract](../../.openresearch/artifacts/claim_2/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_2/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_2/raw_output.json)
- [Independent checker output](../../.openresearch/artifacts/claim_2/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_2/negative_control_output.json)
- [Falsification route](../../.openresearch/artifacts/claim_2/falsification_route.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Limitations](../../.openresearch/artifacts/claim_2/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old nine-point min/forall identity is **Historical rejected baseline**.
