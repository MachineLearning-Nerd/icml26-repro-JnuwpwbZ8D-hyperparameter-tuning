# Claim 1 — Theorem 4.1 universal FOL bound

---
<!-- trackio-cell
{"type":"markdown","id":"cell_universal_c1","created_at":"2026-07-27T12:00:00+00:00","title":"Claim 1 proof certificate"}
-->

**Verdict: `VERIFIED` · confidence: `HIGH`**

## Exact claim, quantifiers, and assumptions

For every fixed instance `x` and threshold `t`, uniformly over
`α∈[α_min,α_max]^p`, assume the threshold predicate is a polynomial FOL with a
fixed number `K` of quantified blocks of dimensions `d₁,…,d_K`, at most `M`
atoms, and degree at most `Δ`. Theorem 4.1 bounds the pseudo-dimension by

`O(p A log M + p² B log Δ)`, where
`A=∏(d_k+1)` and `B=∏d_k`.

This is the exact main-source statement at `source/icml2026.tex:390`. The judge
paraphrase replaces `B` by the larger `A` in the second term. Since
`B≤A` for `d_k≥1`, the exact theorem implies that looser paraphrase; this is
not a contradiction.

## Machine-checked proof chain

1. Basu--Pollack--Roy Algorithm 14.8 turns the FOL into an equivalent
   quantifier-free formula.
2. Its atom count satisfies
   `I ≤ M^A Δ^(c p B)` and its degree satisfies `Δ_QE≤Δ^(c'B)`.
3. The quantifier-free Boolean formula is a Goldberg--Jerrum algorithm with
   predicate complexity `I` and degree `Δ_QE`.
4. Bartlett et al. Theorem 3.3 gives
   `Pdim ≤ C p log(I Δ_QE)`.
5. Expanding the log gives
   `pA log M + (c p²B+c'pB)logΔ`.
6. Because `p≥1`, the lower-order `pB logΔ` term is absorbed by the
   `p²B logΔ` term.

The certificate also detects, and does not propagate, the Appendix typo that
uses upper product index `M` instead of `K`.

## Fail-sensitive controls

All four mutations are rejected: replace `K` by `M`; drop uniformity in
`x,t`; drop the `p²` degree term; omit the QE degree from the GJ degree.

## Executed evidence

- [Exact raw C1 proof JSON](../../.openresearch/artifacts/universal_proofs/C1.json)
- [Primary verifier source](../../repro/src/verify_universal_theorem_chains.py)
- [Independent auditor source](../../repro/src/audit_universal_theorem_chains.py)
- [Independent audit JSON](../../.openresearch/artifacts/universal_proofs/independent_audit.json)

```output
UNIVERSAL_PROOF_RESULT={"all_universal_proof_chains_passed": true, "claims": 6, "finite_sweeps_used_as_proof": 0, "mutations_rejected": 24, "verdicts": {"C1": "VERIFIED", "C2": "VERIFIED", "C3": "VERIFIED", "C4": "VERIFIED", "C5": "VERIFIED", "C6": "VERIFIED"}}
C1_AUDIT={"derivation_edges_complete":true,"exact_checks_fail_closed":true,"final_verdict_exact":true,"four_distinct_fail_sensitive_controls":true,"no_finite_sweep_used_as_proof":true,"quantifier_manifest_complete":true,"source_anchor_complete":true}
```

`finite_parameter_sweeps_used_as_proof: 0`. The external QE and GJ theorems
are trusted dependencies stated explicitly, not silently “verified” by
examples.
