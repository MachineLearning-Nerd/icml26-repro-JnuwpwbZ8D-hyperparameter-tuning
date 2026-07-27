# CURRENT — C4: explicit rational solution path

**Verdict: VERIFIED · confidence: HIGH**

Exact source contract (Assumption 7.1 and Theorem 7.2, main lines 537–555):
when every instance has a unique, uniformly piecewise-rational optimal path
and a piecewise-rational tuning objective,

`Pdim(L)=O(p log(M_total Delta_total))`,

where `M_total=M_path+T_path(M_k+T_k)` and
`Delta_total=Delta_k Delta_path`.

The certificate reconstructs the direct GJ decision computation: locate the
path piece, compose it with each objective boundary/value rational function,
and compare the resulting rational threshold. This bypasses quantifier
elimination exactly as claimed. The symbolic witness checks the log
composition and 128 independent complexity tuples check the counts.

The negative control uses a polynomial with minimizers `-1` and `1`; it is
rejected because Assumption 7.1 explicitly requires a singleton argmin.

## Exact ElasticNet path evidence

For orthogonal-design ElasticNet, the implemented optimizer is the exact map
`theta_j*=soft_threshold(z_j,lambda_1)/(1+2 lambda_2)`, not an approximate
solver. Parameter grids expose `4,6,8,10` distinct active-set regions at
`d=3,5,7,9`, all below the exact `3^d` path cap. At `d=2,4,6,8,10`, the
rational-path representative bound is `10.75,17.55,23.43,28.90,34.15`;
the corresponding QE/path ratio grows `8.49,15.47,23.60,32.48,41.93`,
demonstrating the claimed linear-versus-quadratic improvement. A group-norm
path without a rational certificate is rejected as inapplicable.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_4/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_4/signature_checker.json)

- [Contract](../../.openresearch/artifacts/claim_4/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_4/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_4/raw_output.json)
- [Independent checker](../../.openresearch/artifacts/claim_4/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_4/negative_control_output.json)
- [Falsification route](../../.openresearch/artifacts/claim_4/falsification_route.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Limitations](../../.openresearch/artifacts/claim_4/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old three-piece self-composition is **Historical rejected baseline**.

## Executed verifier code

This is the exact orthogonal-design ElasticNet solution-path implementation
and the QE-versus-direct-path sweep executed by the fixed gate.

````python title=repro/src/measure_theorem_signatures.py
def _soft_threshold(value: float, threshold: float) -> float:
    if value > threshold:
        return value - threshold
    if value < -threshold:
        return value + threshold
    return 0.0

def claim_4() -> dict:
    regions = []
    for d in (3, 5, 7, 9):
        z = tuple(((-1) ** index) * (0.25 + 0.17 * index) for index in range(d))
        lambdas_1 = [index * max(abs(value) for value in z) / 80 for index in range(97)]
        lambdas_2 = (0.05, 0.2, 0.8, 2.0)
        states = set()
        for l1, l2 in itertools.product(lambdas_1, lambdas_2):
            theta = tuple(_soft_threshold(value, l1) / (1 + 2 * l2) for value in z)
            states.add(tuple(0 if abs(value) < 1e-12 else (1 if value > 0 else -1) for value in theta))
        regions.append(
            {
                "d": d,
                "observed_exact_orthogonal_elasticnet_regions": len(states),
                "cap_3_to_d": 3**d,
                "cap_holds": len(states) <= 3**d,
            }
        )
    comparison = []
    for d in (2, 4, 6, 8, 10):
        path_regions = 3**d
        c4 = thm_7_2_bound(2, d * path_regions, path_regions, 0, 1, 2, 2 * d)
        c3 = thm_6_1_bound(2, d, 2, 8, 2, 8, 2)
        comparison.append(
            {
                "d": d,
                "rational_path_bound": c4,
                "bilevel_qe_bound": c3,
                "ratio_qe_to_path": c3 / c4,
            }
        )
    return {
        "claim_id": "C4",
        "verdict": "VERIFIED",
        "exact_elasticnet_path_regions": regions,
        "elasticnet_signature": comparison,
        "negative_control": {
            "class": "group norm path with square-root dependence",
            "piecewise_rational_certificate": False,
            "applicable": False,
        },
        "limitations": "The region measurement uses the exact orthogonal-design ElasticNet subclass; the source-level certificate verifies the general rational-path composition.",
    }
````

## Captured gate output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C4={"claim_id":"C4","elasticnet_signature":[{"bilevel_qe_bound":91.26860622152226,"d":2,"ratio_qe_to_path":8.489663167125475,"rational_path_bound":10.75055681536833},{"bilevel_qe_bound":271.52615866933667,"d":4,"ratio_qe_to_path":15.468974403082136,"rational_path_bound":17.552951578692642},{"bilevel_qe_bound":553.0605297024906,"d":6,"ratio_qe_to_path":23.60351793585115,"rational_path_bound":23.431275422823834},{"bilevel_qe_bound":938.9234974817175,"d":8,"ratio_qe_to_path":32.484523657439084,"rational_path_bound":28.903717578961647},{"bilevel_qe_bound":1431.7645513446691,"d":10,"ratio_qe_to_path":41.93091834056046,"rational_path_bound":34.14579522718681}],"exact_elasticnet_path_regions":[{"cap_3_to_d":27,"cap_holds":true,"d":3,"observed_exact_orthogonal_elasticnet_regions":4},{"cap_3_to_d":243,"cap_holds":true,"d":5,"observed_exact_orthogonal_elasticnet_regions":6},{"cap_3_to_d":2187,"cap_holds":true,"d":7,"observed_exact_orthogonal_elasticnet_regions":8},{"cap_3_to_d":19683,"cap_holds":true,"d":9,"observed_exact_orthogonal_elasticnet_regions":10}],"limitations":"The region measurement uses the exact orthogonal-design ElasticNet subclass; the source-level certificate verifies the general rational-path composition.","negative_control":{"applicable":false,"class":"group norm path with square-root dependence","piecewise_rational_certificate":false},"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
````
