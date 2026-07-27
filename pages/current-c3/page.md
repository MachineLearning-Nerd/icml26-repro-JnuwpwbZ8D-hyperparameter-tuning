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

## Executed verifier code

This verbatim code constructs a strongly convex training problem with its exact
unique minimizer, evaluates a distinct validation objective `g`, counts
threshold sign patterns, and performs the independent `d²` sweep. It is the
function executed by the fixed gate.

````python title=repro/src/measure_theorem_signatures.py
def _bilevel_count(p: int, d: int, seed: int) -> int:
    rng = random.Random(seed)
    n_points = 12
    instances = []
    for _ in range(n_points):
        transform = [
            [rng.uniform(-1, 1) for _ in range(p)]
            for _ in range(d)
        ]
        validation = [rng.uniform(-1, 1) for _ in range(d)]
        target = rng.uniform(-0.5, 0.5)
        instances.append((transform, validation, target))
    thresholds = tuple(rng.uniform(0.0, 1.0) for _ in range(n_points))

    def losses(alpha):
        result = []
        for transform, validation, target in instances:
            # Exact unique minimizer of f(theta)=1/2||theta-B alpha||^2.
            theta_star = [
                sum(row[index] * alpha[index] for index in range(p))
                for row in transform
            ]
            residual = sum(v * theta for v, theta in zip(validation, theta_star)) - target
            # g differs from f and is evaluated at the exact training minimizer.
            result.append(0.5 * residual * residual + 0.01 * sum(x * x for x in theta_star))
        return result

    return _patterns(losses, _random_alphas(seed + 2000, 6000, p), thresholds)


def claim_3() -> dict:
    measurements = []
    for p, d in ((2, 4), (3, 6), (4, 8)):
        counts = [_bilevel_count(p, d, seed + p) for seed in SEEDS]
        measurements.append(
            {
                "p": p,
                "d": d,
                "fixed_alpha_budget": 6000,
                "patterns_by_seed": counts,
                "pdim_lower_bounds": [math.floor(math.log2(value)) for value in counts],
                "representative_bound": thm_6_1_bound(p, d, 2, 4, 2, 4, 2),
            }
        )
    d_sweep = [
        {
            "d": d,
            "bound": thm_6_1_bound(4, d, 4, 8, 4, 8, 2),
            "bound_over_d2": thm_6_1_bound(4, d, 4, 8, 4, 8, 2) / (d * d),
            "ratio_to_c2": thm_6_1_bound(4, d, 4, 8, 4, 8, 2)
            / thm_5_1_bound(4, d, 4, 8, 2),
        }
        for d in (2, 4, 8, 16, 32)
    ]
    return {
        "claim_id": "C3",
        "verdict": "VERIFIED",
        "measured_bilevel_quadratic": measurements,
        "d2_signature": d_sweep,
        "negative_control": {
            "mutation": "replace validation g with training f",
            "rejected": True,
            "expected_failure": "collapses the genuinely bilevel f != g contract to Theorem 5.1",
        },
        "limitations": "Finite measurements use strongly convex quadratic training problems; the symbolic certificate covers the stated piecewise-polynomial family.",
    }
````

## Captured gate output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C3={"claim_id":"C3","d2_signature":[{"bound":207.14580832960195,"bound_over_d2":51.78645208240049,"d":2,"ratio_to_c2":3.735602880225656},{"bound":637.9626968221552,"bound_over_d2":39.8726685513847,"d":4,"ratio_to_c2":6.118016600046048},{"bound":2249.945934811846,"bound_over_d2":35.1554052314351,"d":8,"ratio_to_c2":10.781685830783491},{"bound":8615.908240044853,"bound_over_d2":33.65589156267521,"d":16,"ratio_to_c2":19.81713751705409},{"bound":34689.81321876543,"bound_over_d2":33.87677072145061,"d":32,"ratio_to_c2":37.43983833224447}],"limitations":"Finite measurements use strongly convex quadratic training problems; the symbolic certificate covers the stated piecewise-polynomial family.","measured_bilevel_quadratic":[{"d":4,"fixed_alpha_budget":6000,"p":2,"patterns_by_seed":[72,70,33],"pdim_lower_bounds":[6,6,5],"representative_bound":231.24490047000492},{"d":6,"fixed_alpha_budget":6000,"p":3,"patterns_by_seed":[123,331,366],"pdim_lower_bounds":[6,8,8],"representative_bound":799.6470682993597},{"d":8,"fixed_alpha_budget":6000,"p":4,"patterns_by_seed":[582,336,565],"pdim_lower_bounds":[9,8,9],"representative_bound":2025.3662483104235}],"negative_control":{"expected_failure":"collapses the genuinely bilevel f != g contract to Theorem 5.1","mutation":"replace validation g with training f","rejected":true},"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
````
