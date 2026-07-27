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

## Concrete sign-pattern and scaling evidence

A genuine two-piece quadratic loss family was evaluated on 12 problem
instances with 6,000 parameter vectors per seed, a budget fixed independently
of the theorem formula. At `(p,d)=(2,4),(3,6),(4,8)`, the realized pattern
counts were respectively `70/70/79`, `190/190/246`, and `490/386/428` over
seeds `173,271,419`, giving empirical pseudo-dimension lower bounds `6`, `7`,
and `8`. The representative bounds are `37.481`, `104.169`, and `213.489`.
Independent sweeps over `p=1..8` and `d=2..64` reproduce the quadratic-in-`p`
and near-linear-in-`d` signature. The square-root control is rejected because
it is not piecewise polynomial.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_2/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_2/signature_checker.json)

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
