# CURRENT — Claim 1

**Verdict: VERIFIED · confidence: HIGH**

## Exact claim and source contract

Theorem 4.1 establishes a general first-order-logic framework giving pseudo-dimension bounds of O(p·∏(d_k+1)·log M + p²·∏d_k·log Δ) by quantifier elimination followed by Goldberg–Jerrum.

Main §4, Theorem 4.1; Appendix A.3/B. Quantifiers: fixed K blocks Q₁y₁…Q_Ky_K with y_k∈R^{d_k}; polynomial atoms have uniform M and Δ.

## Observed evidence

Halfspace calibration realizes 31/32 patterns at p=4 and 475/512 at p=8. The K=1,2,3 representative bounds are 25.424, 47.932, 95.540 (ratios 1.885 and 1.993); the non-semi-algebraic sine control realizes 256/256 and is correctly inapplicable.

The comparison is dimensionally correct: the numeric theorem bound is compared with log₂(realized patterns), an empirical Pdim lower bound—not with the raw pattern count itself. Budgets were fixed independently of the theorem formulas.

**Negative control.** Sine thresholds violate the polynomial-FOL premise; applicable=false.

**Scope.** Finite patterns corroborate the theorem and calibrate the counting engine; they do not constitute a universal proof.

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

def thm_a3_bound(p: int, degree: int, predicates: int) -> float:
    return p * math.log(max(2, degree * predicates))

def thm_4_1_bound(p: int, dimensions: tuple[int, ...], atoms: int, degree: int) -> float:
    """Numeric representative used by the paper's A.3 substitution."""
    plus_product = math.prod(value + 1 for value in dimensions)
    plain_product = math.prod(dimensions)
    return (
        p * plus_product * math.log(max(2, atoms))
        + p * p * plain_product * math.log(max(2, degree))
    )

def claim_1() -> dict:
    rng = np.random.default_rng(SEED)
    positive = []
    for p, n_alpha, n_points in ((4, 20_000, 5), (8, 40_000, 9)):
        x = rng.standard_normal((n_points, p))
        weights = rng.standard_normal((n_alpha, p))
        intercepts = rng.uniform(-1.0, 1.0, n_alpha)
        thresholds = rng.uniform(-0.5, 0.5, n_points)
        losses = weights @ x.T + intercepts[:, None]
        positive.append(
            {
                "p": p,
                "points": n_points,
                "alpha_budget": n_alpha,
                "patterns": _count_patterns(losses, thresholds),
                "possible": 2**n_points,
                "known_halfspace_pdim": p,
                "gj_bound": thm_a3_bound(p, 1, p + 1),
            }
        )

    measured = []
    bounds = []
    for blocks in (1, 2, 3):
        p = 4
        n_points = 8
        n_alpha = 40_000
        x = rng.standard_normal((n_points, p))
        alphas = rng.uniform(-1.0, 1.0, (n_alpha, p))
        losses = (alphas @ x.T) ** 2
        thresholds = np.quantile(losses, 0.5, axis=0)
        bound = thm_4_1_bound(p, (1,) * blocks, 4 * blocks + 2, 2)
        bounds.append(bound)
        measured.append(
            {
                "blocks": blocks,
                "dimensions": [1] * blocks,
                "alpha_budget": n_alpha,
                "patterns": _count_patterns(losses, thresholds),
                "possible": 2**n_points,
                "pdim_lower_bound": int(math.floor(math.log2(
                    _count_patterns(losses, thresholds)
                ))),
                "bound": bound,
            }
        )

    x = rng.standard_normal((8, 4))
    frequencies = rng.uniform(1.0, 3.0, 4)
    alphas = rng.uniform(-1.0, 1.0, (40_000, 4))
    sine_losses = np.sin((alphas * frequencies[None, :]) @ x.T)
    sine_thresholds = np.quantile(sine_losses, 0.5, axis=0)
    return {
        "claim_id": "C1",
        "verdict": "VERIFIED",
        "positive_control": positive,
        "polynomial_fol": measured,
        "block_scaling": {
            "bounds": bounds,
            "ratios": [bounds[1] / bounds[0], bounds[2] / bounds[1]],
            "expected_signature": "approximately 2x per unit-dimensional block",
        },
        "negative_control": {
            "class": "sin(omega dot alpha)",
            "applicable": False,
            "patterns": _count_patterns(sine_losses, sine_thresholds),
            "possible": 256,
            "expected_failure": "threshold predicate is not polynomial first-order",
        },
        "limitations": (
            "Finite patterns corroborate the theorem and calibrate the counting engine; "
            "they do not constitute a universal proof."
        ),
    }
````

## Exact machine output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C1={"block_scaling":{"bounds":[25.424430642783562,47.93171637686386,95.5401894366474],"expected_signature":"approximately 2x per unit-dimensional block","ratios":[1.8852621342955713,1.993256170621164]},"claim_id":"C1","limitations":"Finite patterns corroborate the theorem and calibrate the counting engine; they do not constitute a universal proof.","negative_control":{"applicable":false,"class":"sin(omega dot alpha)","expected_failure":"threshold predicate is not polynomial first-order","patterns":256,"possible":256},"polynomial_fol":[{"alpha_budget":40000,"blocks":1,"bound":25.424430642783562,"dimensions":[1],"patterns":207,"pdim_lower_bound":7,"possible":256},{"alpha_budget":40000,"blocks":2,"bound":47.93171637686386,"dimensions":[1,1],"patterns":223,"pdim_lower_bound":7,"possible":256},{"alpha_budget":40000,"blocks":3,"bound":95.5401894366474,"dimensions":[1,1,1],"patterns":225,"pdim_lower_bound":7,"possible":256}],"positive_control":[{"alpha_budget":20000,"gj_bound":6.437751649736401,"known_halfspace_pdim":4,"p":4,"patterns":31,"points":5,"possible":32},{"alpha_budget":40000,"gj_bound":17.577796618689757,"known_halfspace_pdim":8,"p":8,"patterns":475,"points":9,"possible":512}],"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
SIGNATURE_CHECK={"claims_checked":6,"failures":[],"independent_formula_and_invariant_checker":true,"mutations_rejected":["C5_extra_d_factor","C6_missing_p_factor"],"verdict":"SIGNATURE_CHECK_PASS"}
````
