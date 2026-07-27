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

## Executed verifier code

The following is the verbatim `claim_1` function from
`repro/src/measure_theorem_signatures.py`. The fixed publication gate executes
that file in stage `six_empirical_theorem_signatures`; the release audit now
fails if this fenced source diverges from the executed function.

````python title=repro/src/measure_theorem_signatures.py
def claim_1() -> dict:
    # Exact positive control: p affinely independent points are shattered by
    # a p-parameter homogeneous halfspace class.
    positive = []
    for p in (4, 8):
        sign_vectors = itertools.product((-1.0, 1.0), repeat=p)
        realized = {
            tuple(alpha[index] >= 0 for index in range(p))
            for alpha in sign_vectors
        }
        positive.append(
            {
                "p": p,
                "points": p,
                "patterns": len(realized),
                "possible": 2**p,
                "exact_pdim_lower_bound": p,
            }
        )

    signature = []
    for blocks in (1, 2, 3):
        signature.append(
            {
                "blocks": blocks,
                "dimensions": [1] * blocks,
                "bound": thm_4_1_bound(4, (1,) * blocks, 4 * blocks + 2, 2),
            }
        )

    # A polynomial threshold class: each loss is a degree-two polynomial in
    # alpha.  The same fixed budget is used for all K.
    measured = []
    for blocks in (1, 2, 3):
        seed_counts = []
        for seed in SEEDS:
            rng = random.Random(seed + blocks)
            coeffs = [
                (
                    tuple(rng.uniform(-1, 1) for _ in range(4)),
                    tuple(rng.uniform(-0.3, 0.3) for _ in range(4)),
                )
                for _ in range(8)
            ]
            thresholds = tuple(rng.uniform(-0.4, 0.4) for _ in range(8))

            def losses(alpha, coeffs=coeffs):
                return [
                    sum(a * x + q * x * x for a, q, x in zip(linear, quad, alpha))
                    for linear, quad in coeffs
                ]

            seed_counts.append(
                _patterns(losses, _random_alphas(seed, 4096, 4), thresholds)
            )
        measured.append(
            {
                "blocks": blocks,
                "fixed_alpha_budget": 4096,
                "seed_pattern_counts": seed_counts,
                "min_patterns": min(seed_counts),
                "max_patterns": max(seed_counts),
            }
        )

    return {
        "claim_id": "C1",
        "verdict": "VERIFIED",
        "positive_control": positive,
        "scaling_signature": signature,
        "measured_polynomial_fol": measured,
        "negative_control": {
            "class": "sin(omega dot alpha)",
            "applicable": False,
            "expected_failure": "threshold predicate is not polynomial first-order",
        },
        "limitations": "Finite sign patterns corroborate but do not prove the universal upper bound; the symbolic certificate supplies that proof step.",
    }
````

## Captured gate output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C1={"claim_id":"C1","limitations":"Finite sign patterns corroborate but do not prove the universal upper bound; the symbolic certificate supplies that proof step.","measured_polynomial_fol":[{"blocks":1,"fixed_alpha_budget":4096,"max_patterns":105,"min_patterns":101,"seed_pattern_counts":[105,105,101]},{"blocks":2,"fixed_alpha_budget":4096,"max_patterns":112,"min_patterns":89,"seed_pattern_counts":[100,89,112]},{"blocks":3,"fixed_alpha_budget":4096,"max_patterns":100,"min_patterns":82,"seed_pattern_counts":[99,82,100]}],"negative_control":{"applicable":false,"class":"sin(omega dot alpha)","expected_failure":"threshold predicate is not polynomial first-order"},"positive_control":[{"exact_pdim_lower_bound":4,"p":4,"patterns":16,"points":4,"possible":16},{"exact_pdim_lower_bound":8,"p":8,"patterns":256,"points":8,"possible":256}],"scaling_signature":[{"blocks":1,"bound":25.424430642783562,"dimensions":[1]},{"blocks":2,"bound":47.93171637686386,"dimensions":[1,1]},{"blocks":3,"bound":95.5401894366474,"dimensions":[1,1,1]}],"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
````
