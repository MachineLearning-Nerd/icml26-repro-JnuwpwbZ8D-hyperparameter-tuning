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
No seeds; deterministic local CPU. The historical 96 formula substitutions are
preserved only as **Historical rejected baseline**.
