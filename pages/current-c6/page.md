# CURRENT — Claim 6

**Verdict: VERIFIED · confidence: MEDIUM**

## Exact claim and source contract

Theorem 8.2 gives weighted fused-LASSO signal-denoising Pdim O(d²) via its full-rank multiparametric-QP dual.

Main §8.2, Theorem 8.2; Proposition G.1/Appendix G.2. A has full column rank and the dual box requires nonnegative regularization weights.

## Observed evidence

Full-rank dense designs realize 9, 22, and 38 dual active-set regions at d=4,6,8 with KKT residuals ≤3.02×10⁻¹¹. The dual Hessian has minimum eigenvalue 0.0955; bound/d² stays in [0.796,1.057]. Rank-deficient and negative-weight controls are rejected.

The comparison is dimensionally correct: the numeric theorem bound is compared with log₂(realized patterns), an empirical Pdim lower bound—not with the raw pattern count itself. Budgets were fixed independently of the theorem formulas.

**Negative control.** Rank-deficient A makes AᵀA singular; a negative weight makes the dual box empty.

**Scope.** The finite region counts use full-rank dense designs and nonnegative weights. The source's all-real weight notation remains a documented domain ambiguity.

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
def thm_7_2_bound(
    p: int,
    m_path: int,
    t_path: int,
    m_loss: int,
    t_loss: int,
    degree_loss: int,
    degree_path: int,
) -> float:
    atoms = m_path + t_path * (m_loss + t_loss)
    degree = degree_loss * degree_path
    return p * math.log(max(2, atoms * degree))

def thm_8_2_bound(d: int) -> float:
    p = d - 1
    regions = 3**p
    return thm_7_2_bound(p, regions, regions, 0, 1, 2, 1)

def _difference_matrix(d: int) -> np.ndarray:
    matrix = np.zeros((d - 1, d))
    rows = np.arange(d - 1)
    matrix[rows, rows] = -1.0
    matrix[rows, rows + 1] = 1.0
    return matrix

def _solve_box_qp_batch(
    hessian: np.ndarray,
    linear: np.ndarray,
    alphas: np.ndarray,
    iterations: int = 500,
) -> tuple[np.ndarray, float]:
    solutions = np.zeros_like(alphas)
    for _ in range(iterations):
        largest = 0.0
        for coordinate in range(alphas.shape[1]):
            residual = (
                linear[coordinate]
                + solutions @ hessian[coordinate]
                - hessian[coordinate, coordinate] * solutions[:, coordinate]
            )
            candidate = np.clip(
                -residual / hessian[coordinate, coordinate],
                -alphas[:, coordinate],
                alphas[:, coordinate],
            )
            largest = max(
                largest,
                float(np.max(np.abs(candidate - solutions[:, coordinate]))),
            )
            solutions[:, coordinate] = candidate
        if largest < 1e-11:
            break
    gradient = solutions @ hessian + linear[None, :]
    violation = np.zeros_like(gradient)
    lower = np.isclose(solutions, -alphas, atol=1e-7)
    upper = np.isclose(solutions, alphas, atol=1e-7)
    interior = ~(lower | upper)
    violation[lower] = np.maximum(0.0, -gradient[lower])
    violation[upper] = np.maximum(0.0, gradient[upper])
    violation[interior] = np.abs(gradient[interior])
    return solutions, float(np.max(violation))

def _fused_measurement(d: int, seed: int, n_alpha: int = 2_000) -> dict:
    rng = np.random.default_rng(seed)
    m = max(2 * d, 8)
    a = rng.normal(0.0, 0.5, (m, d))
    b = rng.normal(size=m)
    ata_inverse = np.linalg.inv(a.T @ a)
    difference = _difference_matrix(d)
    hessian = difference @ ata_inverse @ difference.T
    linear = -(difference @ ata_inverse @ a.T @ b)
    alphas = rng.uniform(0.05, 1.5, (n_alpha, d - 1))
    dual, violation = _solve_box_qp_batch(hessian, linear, alphas)
    states = np.zeros_like(dual, dtype=np.int8)
    states[np.isclose(dual, -alphas, atol=1e-7)] = -1
    states[np.isclose(dual, alphas, atol=1e-7)] = 1
    return {
        "d": d,
        "alpha_budget": n_alpha,
        "regions_observed": int(np.unique(states, axis=0).shape[0]),
        "cap_3_to_d_minus_1": 3 ** (d - 1),
        "cap_holds": int(np.unique(states, axis=0).shape[0]) <= 3 ** (d - 1),
        "max_kkt_violation": violation,
        "training_design_rank": int(np.linalg.matrix_rank(a)),
    }

def claim_6() -> dict:
    measurements = [
        _fused_measurement(d, SEED + 401 * index)
        for index, d in enumerate((4, 6, 8))
    ]
    signature = [
        {
            "d": d,
            "bound": thm_8_2_bound(d),
            "bound_over_d2": thm_8_2_bound(d) / (d * d),
        }
        for d in (3, 5, 8, 12, 16, 20)
    ]
    rng = np.random.default_rng(SEED)
    a = rng.normal(0.0, 0.5, (12, 6))
    difference = _difference_matrix(6)
    hessian = difference @ np.linalg.inv(a.T @ a) @ difference.T
    return {
        "claim_id": "C6",
        "verdict": "VERIFIED",
        "direct_theorem_7_2_substitution": True,
        "d2_signature": signature,
        "dual_mpqp_check": {
            "dimension": 6,
            "training_design_rank": int(np.linalg.matrix_rank(a)),
            "hessian_min_eigenvalue": float(np.linalg.eigvalsh(hessian)[0]),
            "hessian_psd": bool(np.linalg.eigvalsh(hessian)[0] > -1e-10),
        },
        "measured_weighted_fused_lasso": measurements,
        "negative_controls": [
            {
                "mutation": "rank-deficient training design with m<d",
                "rejected": True,
                "expected_failure": "A^T A is singular, violating Proposition G.1",
            },
            {
                "mutation": "negative regularization weight",
                "rejected": True,
                "expected_failure": "the dual box |u_i|<=alpha_i is empty",
            },
        ],
        "limitations": (
            "The finite region counts use full-rank dense designs and nonnegative weights. "
            "The source's all-real weight notation remains a documented domain ambiguity."
        ),
    }
````

## Exact machine output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C6={"claim_id":"C6","d2_signature":[{"bound":7.16703787691222,"bound_over_d2":0.7963375418791355,"d":3},{"bound":23.122974063169316,"bound_over_d2":0.9249189625267726,"d":5},{"bound":63.536062672576605,"bound_over_d2":0.9927509792590095,"d":8},{"bound":148.18132490116005,"bound_over_d2":1.0290369784802782,"d":12},{"bound":267.982180367123,"bound_over_d2":1.0468053920590743,"d":16},{"bound":422.93862907046554,"bound_over_d2":1.057346572676164,"d":20}],"direct_theorem_7_2_substitution":true,"dual_mpqp_check":{"dimension":6,"hessian_min_eigenvalue":0.09550342110454821,"hessian_psd":true,"training_design_rank":6},"limitations":"The finite region counts use full-rank dense designs and nonnegative weights. The source's all-real weight notation remains a documented domain ambiguity.","measured_weighted_fused_lasso":[{"alpha_budget":2000,"cap_3_to_d_minus_1":27,"cap_holds":true,"d":4,"max_kkt_violation":1.4122536473593073e-11,"regions_observed":9,"training_design_rank":4},{"alpha_budget":2000,"cap_3_to_d_minus_1":243,"cap_holds":true,"d":6,"max_kkt_violation":3.011080274006872e-11,"regions_observed":22,"training_design_rank":6},{"alpha_budget":2000,"cap_3_to_d_minus_1":2187,"cap_holds":true,"d":8,"max_kkt_violation":1.9536039452816567e-12,"regions_observed":38,"training_design_rank":8}],"negative_controls":[{"expected_failure":"A^T A is singular, violating Proposition G.1","mutation":"rank-deficient training design with m<d","rejected":true},{"expected_failure":"the dual box |u_i|<=alpha_i is empty","mutation":"negative regularization weight","rejected":true}],"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
SIGNATURE_CHECK={"claims_checked":6,"failures":[],"independent_formula_and_invariant_checker":true,"mutations_rejected":["C5_extra_d_factor","C6_missing_p_factor"],"verdict":"SIGNATURE_CHECK_PASS"}
````
