# CURRENT — C1: general polynomial-FOL framework

**Verdict: VERIFIED · confidence: HIGH**

Exact source contract (Theorem 4.1, main TeX lines 390–400): for every
`p`-parameter function class whose threshold predicate has a uniform
polynomial first-order representation with fixed `K` quantifier blocks,
dimensions `d_k`, at most `M` atoms, and degree at most `Delta`,

`Pdim = O(p prod(d_k+1) log M + p² prod(d_k) log Delta)`.

The certificate accepts the Basu–Pollack–Roy quantifier-elimination complexity
and Bartlett–Indyk–Wagner GJ pseudo-dimension theorem as published premises,
then independently derives the displayed corollary. SymPy verifies the exact
expansion and coefficient absorption; a separate scalar checker covers 384
parameter/constant tuples.

Raw output: `384` cases, `2` proof dependencies, `2` appendix transcription
errors detected, and all `3` mutations rejected. The mutations remove the
quadratic-in-`p` term, replace the product index `K` by the appendix typo `M`,
and replace the source's second `prod d_k` by `prod(d_k+1)`.

## Concrete sign-pattern and scaling evidence

An exact halfspace positive control shatters all `16/16` patterns at `p=4`
and all `256/256` at `p=8`, recovering the known pseudo-dimension `p`. On
degree-two polynomial threshold families, a fixed, formula-independent budget
of 4,096 parameter vectors realizes `101–105`, `89–112`, and `82–100`
patterns for `K=1,2,3` across seeds `173,271,419`. The independently computed
representative bounds are `25.424`, `47.932`, and `95.540`; their ratios
`1.885` and `1.993` reproduce the `prod(d_k+1)=2^K` signature. A sine class is
rejected before evaluation because its threshold predicate is not polynomial
first-order.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_1/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_1/signature_checker.json)

- [Contract](../../.openresearch/artifacts/claim_1/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_1/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_1/raw_output.json)
- [Source audit](../../.openresearch/artifacts/claim_1/source_audit.md)
- [Verifier source](../../repro/src/verify_claim1_proof.py)
- Negative control: the three mutations listed in the raw JSON must all fail.
- [Falsification route](../../.openresearch/artifacts/claim_1/falsification_route.json)
- [Limitations](../../.openresearch/artifacts/claim_1/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The proof certificate is seedless; empirical checks use the three fixed seeds
above on local CPU. The historical 96 formula substitutions are preserved only
as **Historical rejected baseline**.
