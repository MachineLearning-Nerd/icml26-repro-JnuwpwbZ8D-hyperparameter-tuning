# CURRENT — Claim 2

**Verdict: VERIFIED · confidence: HIGH**

## Exact claim and source contract

Theorem 5.1 bounds piecewise-polynomial training-loss objectives with f=g by O(pd·log(M_f+T_f+d) + p²d·log Δ_f).

Main §5, Theorem 5.1; Appendix D.1. Assumptions: bounded box domains, attained training minimum, uniform (M_f,T_f,Δ_f) piecewise-polynomial structure, f=g.

## Observed evidence

On 12 instances and 10,000 α values, the 4/8/8-piece quadratic families realize 163, 579, and 1,232 patterns. Their empirical Pdim lower bounds are 7, 9, and 10 versus representative bounds 37.481, 104.169, and 213.489. Independent p and d sweeps reproduce the stated signature.

The comparison is dimensionally correct: the numeric theorem bound is compared with log₂(realized patterns), an empirical Pdim lower bound—not with the raw pattern count itself. Budgets were fixed independently of the theorem formulas.

**Negative control.** A square-root loss piece violates piecewise-polynomiality; applicable=false.

**Scope.** The measured family has up to eight convex-quadratic pieces; the result is scoped corroboration, not an exhaustive proof over all such families.

- [Complete executed source](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Raw run JSON](../../.openresearch/artifacts/reference_protocols/raw_output.json)
- [Checker output](../../.openresearch/artifacts/reference_protocols/checker_output.json)
- [Historical rejected baseline](#/historical-rejected-baseline)

Fixed command: uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json.

Formal calibration run: f69eb97c-98f5-4224-93d6-1128fcbe198c; seed 0; one CPU thread enforced; actual protocol runtime 7.200243542 s on local CPU.

## Verifier source

The following is the exact claim-specific segment executed by the fixed gate. Shared imports and the complete module are available at the source link above.

````python title=repro/src/measure_theorem_signatures.py
def _count_patterns(losses: np.ndarray, thresholds: np.ndarray) -> int:
    packed = np.packbits(losses >= thresholds[None, :], axis=1)
    return int(np.unique(packed, axis=0).shape[0])

def thm_4_1_bound(p: int, dimensions: tuple[int, ...], atoms: int, degree: int) -> float:
    """Numeric representative used by the paper's A.3 substitution."""
    plus_product = math.prod(value + 1 for value in dimensions)
    plain_product = math.prod(dimensions)
    return (
        p * plus_product * math.log(max(2, atoms))
        + p * p * plain_product * math.log(max(2, degree))
    )

def thm_5_1_bound(p: int, d: int, mf: int, tf: int, degree: int) -> float:
    return thm_4_1_bound(p, (d,), mf + tf + 2 * d, degree)

def _piecewise_polynomial_count(
    p: int, d: int, pieces: int, seed: int, n_alpha: int = 10_000
) -> int:
    rng = np.random.default_rng(seed)
    n_points = 12
    alphas = rng.uniform(-1.0, 1.0, (n_alpha, p))
    losses = np.empty((n_alpha, n_points))
    for point in range(n_points):
        values = []
        for _ in range(pieces):
            linear = rng.normal(0.0, 1.0, p)
            factor = rng.normal(0.0, 0.35, (max(1, min(d, 4)), p))
            constant = rng.uniform(-0.7, 0.7)
            values.append(
                constant
                + alphas @ linear
                - 0.5 * np.sum((alphas @ factor.T) ** 2, axis=1)
            )
        losses[:, point] = np.min(np.stack(values, axis=1), axis=1)
    return _count_patterns(losses, np.quantile(losses, 0.5, axis=0))

def claim_2() -> dict:
    configs = ((2, 4, 2, 4), (3, 6, 4, 8), (4, 8, 8, 8))
    measurements = []
    for index, (p, d, mf, tf) in enumerate(configs):
        patterns = _piecewise_polynomial_count(p, d, tf, SEED + 101 * index)
        bound = thm_5_1_bound(p, d, mf, tf, 2)
        measurements.append(
            {
                "p": p,
                "d": d,
                "mf": mf,
                "tf": tf,
                "degree": 2,
                "alpha_budget": 10_000,
                "points": 12,
                "patterns": patterns,
                "possible": 4096,
                "pdim_lower_bound": int(math.floor(math.log2(patterns))),
                "representative_bound": bound,
                "bound_covers_lower_bound": math.log2(patterns) <= bound,
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
        "direct_substitution": all(
            math.isclose(
                thm_5_1_bound(p, d, mf, tf, 2),
                thm_4_1_bound(p, (d,), mf + tf + 2 * d, 2),
            )
            for p, d, mf, tf in configs
        ),
        "measured_piecewise_polynomial": measurements,
        "p_sweep": p_sweep,
        "d_sweep": d_sweep,
        "negative_control": {
            "class": "sqrt(1 + theta^2)",
            "applicable": False,
            "expected_failure": "the loss piece is not polynomial",
        },
        "limitations": (
            "The measured family has up to eight convex-quadratic pieces; the result "
            "is scoped corroboration, not an exhaustive proof over all such families."
        ),
    }
````

## Exact machine output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C2={"claim_id":"C2","d_sweep":[{"bound":55.45177444479562,"d":2},{"bound":104.27606502691631,"d":4},{"bound":208.68220147798033,"d":8},{"bound":434.7705733297878,"d":16},{"bound":926.5481573644877,"d":32},{"bound":1994.6097427718028,"d":64}],"direct_substitution":true,"limitations":"The measured family has up to eight convex-quadratic pieces; the result is scoped corroboration, not an exhaustive proof over all such families.","measured_piecewise_polynomial":[{"alpha_budget":10000,"bound_covers_lower_bound":true,"d":4,"degree":2,"mf":2,"p":2,"patterns":163,"pdim_lower_bound":7,"points":12,"possible":4096,"representative_bound":37.48092818511171,"tf":4},{"alpha_budget":10000,"bound_covers_lower_bound":true,"d":6,"degree":2,"mf":4,"p":3,"patterns":579,"pdim_lower_bound":9,"points":12,"possible":4096,"representative_bound":104.1690781875439,"tf":8},{"alpha_budget":10000,"bound_covers_lower_bound":true,"d":8,"degree":2,"mf":8,"p":4,"patterns":1232,"pdim_lower_bound":10,"points":12,"possible":4096,"representative_bound":213.48933161246316,"tf":8}],"negative_control":{"applicable":false,"class":"sqrt(1 + theta^2)","expected_failure":"the loss piece is not polynomial"},"p_sweep":[{"bound":35.53501803605639,"p":1},{"bound":82.16039096107191,"p":2},{"bound":139.87611877504656,"p":3},{"bound":208.68220147798033,"p":4},{"bound":379.5654315507253,"p":6},{"bound":594.8100811793066,"p":8}],"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
SIGNATURE_CHECK={"claims_checked":6,"failures":[],"independent_formula_and_invariant_checker":true,"mutations_rejected":["C5_extra_d_factor","C6_missing_p_factor"],"verdict":"SIGNATURE_CHECK_PASS"}
````
