# CURRENT — C3: bilevel validation-loss pseudo-dimension

**Verdict: VERIFIED · confidence: HIGH**

Exact source contract (Theorem 6.1, main lines 481–503): for uniformly
piecewise-polynomial training and validation objectives, the optimistic
bilevel loss has

`Pdim(L)=O(pd² log M_tot+p²d² log Delta_tot)`.

The certificate retains both quantified `d`-blocks in
`forall theta exists theta'`, including the better-candidate comparison. The
appendix's actual atom count is
`4d+M_g+T_g+2M_f+T_f²`; SymPy proves it is at most `5 M_tot²`, so its logarithm
is `O(log M_tot)`, and proves `(d+1)²<=4d²`. The independent route covers 128
tuples. Dropping the existential block is rejected because it cannot recognize
non-minimizers.

The unattained-minimum adversarial candidate makes the argmin empty and the
paper's bounded real-valued loss undefined; it is therefore an assumption-gap
witness, not falsification.

## Concrete bilevel and scaling evidence

The measured class uses
`f(theta)=1/2 ||theta-B alpha||²`, whose exact unique minimizer is `B alpha`,
and a distinct quadratic validation objective `g`. With the same
formula-independent 6,000-vector budget, 12 instances, and seeds
`173,271,419`, the realized patterns are `72/70/33`, `123/331/366`, and
`582/336/565` at `(p,d)=(2,4),(3,6),(4,8)`. The `d=2..32` sweep keeps
`bound/d²` in `[33.66,51.79]`, while the C3/C2 ratio rises from `3.74` to
`37.44`, exposing the claimed `d` to `d²` jump. Replacing `g` by `f` is a
failing control because it collapses the claim to the training-only setting.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_3/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_3/signature_checker.json)

- [Contract](../../.openresearch/artifacts/claim_3/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_3/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_3/raw_output.json)
- [Independent checker](../../.openresearch/artifacts/claim_3/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_3/negative_control_output.json)
- [Falsification route](../../.openresearch/artifacts/claim_3/falsification_route.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Limitations](../../.openresearch/artifacts/claim_3/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old five-point argmin identity is **Historical rejected baseline**.
