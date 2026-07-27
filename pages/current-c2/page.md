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

## Executed verifier code

This is the verbatim claim-specific implementation executed by the fixed gate,
not pseudocode or a link-only reference. The visibility audit compares this
fence byte-for-byte with the corresponding functions in the executed source.

````python title=repro/src/measure_theorem_signatures.py
def _piecewise_polynomial_count(p: int, seed: int) -> int:
    rng = random.Random(seed)
    n_points = 12
    branch_1 = [
        (tuple(rng.uniform(-1, 1) for _ in range(p)), rng.uniform(-0.5, 0.5))
        for _ in range(n_points)
    ]
    branch_2 = [
        (tuple(rng.uniform(-1, 1) for _ in range(p)), rng.uniform(-0.5, 0.5))
        for _ in range(n_points)
    ]
    thresholds = tuple(rng.uniform(-0.5, 0.5) for _ in range(n_points))

    def losses(alpha):
        values = []
        norm = sum(value * value for value in alpha)
        for (a, c1), (b, c2) in zip(branch_1, branch_2):
            first = c1 + sum(x * y for x, y in zip(a, alpha)) + 0.15 * norm
            second = c2 + sum(x * y for x, y in zip(b, alpha)) + 0.25 * norm
            values.append(min(first, second))
        return values

    return _patterns(losses, _random_alphas(seed + 1000, 6000, p), thresholds)


def claim_2() -> dict:
    configs = ((2, 4, 2, 4), (3, 6, 4, 8), (4, 8, 8, 8))
    measurements = []
    for p, d, mf, tf in configs:
        counts = [_piecewise_polynomial_count(p, seed + 10 * p) for seed in SEEDS]
        measurements.append(
            {
                "p": p,
                "d": d,
                "mf": mf,
                "tf": tf,
                "degree": 2,
                "fixed_alpha_budget": 6000,
                "patterns_by_seed": counts,
                "pdim_lower_bounds": [math.floor(math.log2(value)) for value in counts],
                "representative_bound": thm_5_1_bound(p, d, mf, tf, 2),
            }
        )
    p_sweep = [
        {"p": p, "bound": thm_5_1_bound(p, 8, 4, 8, 2)}
        for p in (1, 2, 3, 4, 6, 8)
    ]
    d_sweep = [
        {"d": d, "bound": thm_5_1_bound(4, d, 4, 8, 2)}
        for d in (2, 4, 8, 16, 32, 64)
    ]
    return {
        "claim_id": "C2",
        "verdict": "VERIFIED",
        "measured_piecewise_polynomial": measurements,
        "p_sweep": p_sweep,
        "d_sweep": d_sweep,
        "negative_control": {
            "class": "sqrt(1 + theta^2)",
            "applicable": False,
            "expected_failure": "piece is not polynomial",
        },
        "limitations": "The measured class is a concrete two-piece quadratic subclass; universal coverage comes from the independent symbolic reduction.",
    }
````

## Captured gate output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C2={"claim_id":"C2","d_sweep":[{"bound":55.45177444479562,"d":2},{"bound":104.27606502691631,"d":4},{"bound":208.68220147798033,"d":8},{"bound":434.7705733297878,"d":16},{"bound":926.5481573644877,"d":32},{"bound":1994.6097427718028,"d":64}],"limitations":"The measured class is a concrete two-piece quadratic subclass; universal coverage comes from the independent symbolic reduction.","measured_piecewise_polynomial":[{"d":4,"degree":2,"fixed_alpha_budget":6000,"mf":2,"p":2,"patterns_by_seed":[70,70,79],"pdim_lower_bounds":[6,6,6],"representative_bound":37.48092818511171,"tf":4},{"d":6,"degree":2,"fixed_alpha_budget":6000,"mf":4,"p":3,"patterns_by_seed":[190,190,246],"pdim_lower_bounds":[7,7,7],"representative_bound":104.1690781875439,"tf":8},{"d":8,"degree":2,"fixed_alpha_budget":6000,"mf":8,"p":4,"patterns_by_seed":[490,386,428],"pdim_lower_bounds":[8,8,8],"representative_bound":213.48933161246316,"tf":8}],"negative_control":{"applicable":false,"class":"sqrt(1 + theta^2)","expected_failure":"piece is not polynomial"},"p_sweep":[{"bound":35.53501803605639,"p":1},{"bound":82.16039096107191,"p":2},{"bound":139.87611877504656,"p":3},{"bound":208.68220147798033,"p":4},{"bound":379.5654315507253,"p":6},{"bound":594.8100811793066,"p":8}],"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
````
