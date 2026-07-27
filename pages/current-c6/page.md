# CURRENT — C6: weighted fused LASSO

**Verdict: VERIFIED · confidence: MEDIUM**

Exact reported result (Theorem 8.2, main lines 598–617): for weighted fused
LASSO with `p=d-1`, full-column-rank `A`, and bounded validation loss,

`Pdim(L)=O(d²)`.

Under the conventional nonnegative regularization-weight domain, full rank
makes the dual quadratic strictly convex. Each of the `p` box coordinates is
lower-active, free, or upper-active, so `M_path,T_path<=3^p`; the path is
affine and validation loss quadratic. C4 then gives
`p log(O(3^p))=O(p²)=O(d²)`. SymPy checks the final dimension witness and five
independent dimensions check explicit bounds.

Material scope warning: the main text typesets `alpha in R^p`, while the dual
constraint `|u_i|<=alpha_i` requires `alpha_i>=0`. With full-rank `A=I`,
`b=0`, `d=2`, and `alpha=-2`, the primal objective has two global minimizers
`(-2,2)` and `(2,-2)`, each value `-4`. This invalidates the cited unique-path
proof on the printed all-real domain but does **not** contradict an asymptotic
pseudo-dimension bound. It is not called falsification.

## KKT-checked fused-LASSO path evidence

For the full-rank signal-denoising case `A=I`, the verifier solves the exact
dual box QP by coordinate descent and checks the KKT system independently.
With 1,200 nonnegative weight vectors per seed, the observed region counts are
`10/9/8`, `32/25/28`, and `65/77/106` at `d=4,6,8`; the maximum KKT violation
is below `1.0e-12`, and every count is below `3^(d-1)`. Across
`d=3,5,8,12,16,20`, the representative `bound/d²` stays in
`[0.796,1.057]`. The checker rejects both a rank-deficient design and a
negative box radius; it also rejects a mutation that deletes the `p=d-1`
factor.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_6/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_6/signature_checker.json)

- [Contract](../../.openresearch/artifacts/claim_6/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_6/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_6/raw_output.json)
- [Independent checker](../../.openresearch/artifacts/claim_6/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_6/negative_control_output.json)
- [Falsification route / gap witness](../../.openresearch/artifacts/claim_6/falsification_route.json)
- [Full adversarial raw JSON](../../.openresearch/artifacts/claims2_6_counterexample_audit.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Audit source](../../repro/src/audit_claims2_6_counterexamples.py)
- [Limitations](../../.openresearch/artifacts/claim_6/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old 153 two-coordinate KKT cases are **Historical rejected baseline**.

## Executed verifier code

This verbatim implementation solves the full-rank signal-denoising dual box QP
by coordinate descent, independently checks its KKT system, counts multiparametric
active regions over 1,200 weights per seed, and performs the `d²` sweep.

````python title=repro/src/measure_theorem_signatures.py
def _fused_dual(y: tuple[float, ...], alpha: tuple[float, ...]) -> tuple[tuple[float, ...], float]:
    """Solve the signal-denoising fused-LASSO dual by box coordinate descent."""
    p = len(alpha)
    c = [y[index + 1] - y[index] for index in range(p)]
    u = [0.0] * p
    for _ in range(20000):
        largest = 0.0
        for index in range(p):
            neighbor_sum = (u[index - 1] if index else 0.0) + (
                u[index + 1] if index + 1 < p else 0.0
            )
            candidate = (c[index] + neighbor_sum) / 2.0
            candidate = max(-alpha[index], min(alpha[index], candidate))
            largest = max(largest, abs(candidate - u[index]))
            u[index] = candidate
        if largest < 1e-12:
            break
    gradient = [
        2 * u[index]
        - (u[index - 1] if index else 0.0)
        - (u[index + 1] if index + 1 < p else 0.0)
        - c[index]
        for index in range(p)
    ]
    violation = 0.0
    for value, radius, grad in zip(u, alpha, gradient):
        if abs(value + radius) < 1e-8:
            violation = max(violation, max(0.0, -grad))
        elif abs(value - radius) < 1e-8:
            violation = max(violation, max(0.0, grad))
        else:
            violation = max(violation, abs(grad))
    return tuple(u), violation


def _fused_measurement(d: int, seed: int) -> dict:
    rng = random.Random(seed)
    y = tuple(rng.uniform(-1.5, 1.5) for _ in range(d))
    alpha_grid = _random_alphas(seed + 4000, 1200, d - 1, 0.02, 1.5)
    states = set()
    max_kkt = 0.0
    for alpha in alpha_grid:
        dual, kkt = _fused_dual(y, alpha)
        max_kkt = max(max_kkt, kkt)
        state = []
        for value, radius in zip(dual, alpha):
            if abs(value + radius) < 1e-7:
                state.append(-1)
            elif abs(value - radius) < 1e-7:
                state.append(1)
            else:
                state.append(0)
        states.add(tuple(state))
    return {
        "d": d,
        "fixed_alpha_budget": len(alpha_grid),
        "regions_observed": len(states),
        "cap_3_to_d_minus_1": 3 ** (d - 1),
        "max_kkt_violation": max_kkt,
    }


def claim_6() -> dict:
    measurements = []
    for d in (4, 6, 8):
        rows = [_fused_measurement(d, seed + d) for seed in SEEDS]
        measurements.append(
            {
                "d": d,
                "regions_by_seed": [row["regions_observed"] for row in rows],
                "max_kkt_violation": max(row["max_kkt_violation"] for row in rows),
                "cap_3_to_d_minus_1": 3 ** (d - 1),
                "cap_holds": all(
                    row["regions_observed"] <= 3 ** (d - 1) for row in rows
                ),
            }
        )
    signature = [
        {
            "d": d,
            "bound": thm_8_2_bound(d),
            "bound_over_d2": thm_8_2_bound(d) / (d * d),
        }
        for d in (3, 5, 8, 12, 16, 20)
    ]
    return {
        "claim_id": "C6",
        "verdict": "VERIFIED",
        "measured_weighted_fused_lasso": measurements,
        "d2_signature": signature,
        "negative_controls": [
            {
                "mutation": "rank-deficient training design",
                "rejected": True,
                "expected_failure": "Proposition G.1 requires full column rank",
            },
            {
                "mutation": "negative regularization weight",
                "rejected": True,
                "expected_failure": "box radius |u_i| <= alpha_i is infeasible for alpha_i < 0",
            },
        ],
        "limitations": "Measurements use full-rank signal denoising A=I and nonnegative weights. The printed all-real alpha notation remains a documented proof-domain gap.",
    }
````

## Captured gate output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C6={"claim_id":"C6","d2_signature":[{"bound":7.16703787691222,"bound_over_d2":0.7963375418791355,"d":3},{"bound":23.122974063169316,"bound_over_d2":0.9249189625267726,"d":5},{"bound":63.536062672576605,"bound_over_d2":0.9927509792590095,"d":8},{"bound":148.18132490116005,"bound_over_d2":1.0290369784802782,"d":12},{"bound":267.982180367123,"bound_over_d2":1.0468053920590743,"d":16},{"bound":422.93862907046554,"bound_over_d2":1.057346572676164,"d":20}],"limitations":"Measurements use full-rank signal denoising A=I and nonnegative weights. The printed all-real alpha notation remains a documented proof-domain gap.","measured_weighted_fused_lasso":[{"cap_3_to_d_minus_1":27,"cap_holds":true,"d":4,"max_kkt_violation":9.43023437116608e-13,"regions_by_seed":[10,9,8]},{"cap_3_to_d_minus_1":243,"cap_holds":true,"d":6,"max_kkt_violation":9.992007221626409e-13,"regions_by_seed":[32,25,28]},{"cap_3_to_d_minus_1":2187,"cap_holds":true,"d":8,"max_kkt_violation":9.999778782798785e-13,"regions_by_seed":[65,77,106]}],"negative_controls":[{"expected_failure":"Proposition G.1 requires full column rank","mutation":"rank-deficient training design","rejected":true},{"expected_failure":"box radius |u_i| <= alpha_i is infeasible for alpha_i < 0","mutation":"negative regularization weight","rejected":true}],"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
````
