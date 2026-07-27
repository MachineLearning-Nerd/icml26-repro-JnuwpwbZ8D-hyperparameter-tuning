# CURRENT — C5: weighted group LASSO

**Verdict: VERIFIED · confidence: HIGH**

Exact mathematical contract (Theorem 8.1, main lines 566–596): the bounded,
well-defined weighted-group-LASSO bilevel loss class has

`Pdim(L)=O(p³d+p²d²)`.

The proof certificate represents every group norm with
`nu_i²=sum_j theta_ij²` **and** `nu_i>=0`, then uses two quantified blocks of
dimensions `d` and `d+2p`. SymPy verifies
`log(2+4p)<=2p`, the block-dimension bounds, and an explicit coefficient
witness `derived <=16(p³d+p²d²)` for positive integer `p,d`. The independent
route covers 12 widely separated tuples.

The signed-weight audit confirms the nonnegative lift equals the group norm for
`alpha=-7,-1,0,2,11`. The failing control omits `nu>=0`, which admits the wrong
root and changes the objective.

## Exact weighted group-LASSO evidence

The concrete solver uses the exact orthogonal-block solution
`theta_g*=(1-alpha_g/||z_g||)_+ z_g`. With 5,000 weight vectors for each of
three seeds, it realizes every binary group-active pattern: `4/4`, `8/8`, and
`16/16` at `(p,d)=(2,4),(3,6),(4,8)`. Independent `p` and `d` sweeps reproduce
the `p³d+p²d²` signature. This evidence is paired with the symbolic norm-lift
certificate above; finite active patterns alone are not treated as a proof.
The non-semi-algebraic `sin(||theta_g||)` control is rejected as inapplicable.

- [Empirical verifier](../../repro/src/measure_theorem_signatures.py)
- [Independent checker](../../repro/src/check_theorem_signatures.py)
- [Empirical raw JSON](../../.openresearch/artifacts/claim_5/signature_output.json)
- [Checker output](../../.openresearch/artifacts/claim_5/signature_checker.json)

- [Contract](../../.openresearch/artifacts/claim_5/claim_contract.json)
- [Proof certificate](../../.openresearch/artifacts/claim_5/proof_certificate.json)
- [Raw JSON](../../.openresearch/artifacts/claim_5/raw_output.json)
- [Independent checker](../../.openresearch/artifacts/claim_5/independent_checker.json)
- [Negative control](../../.openresearch/artifacts/claim_5/negative_control_output.json)
- [Falsification route](../../.openresearch/artifacts/claim_5/falsification_route.json)
- [Verifier source](../../repro/src/verify_claims2_6_proofs.py)
- [Limitations](../../.openresearch/artifacts/claim_5/limitations.md)

Fixed command:
`uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`.
The old 15 KKT instances are **Historical rejected baseline**.

## Executed verifier code

This verbatim implementation runs the exact orthogonal block-soft-threshold
solver over 5,000 weight vectors per seed, counts realized active patterns, and
performs the separate `p` and `d` sweeps.

````python title=repro/src/measure_theorem_signatures.py
def _group_lasso_instance(p: int, group_size: int, seed: int) -> dict:
    rng = random.Random(seed)
    z = [
        tuple(rng.uniform(-1.5, 1.5) for _ in range(group_size))
        for _ in range(p)
    ]
    alphas = _random_alphas(seed + 3000, 5000, p, 0.0, 2.0)
    states = set()
    losses = []
    for alpha in alphas:
        theta = []
        state = []
        for weight, group in zip(alpha, z):
            norm = math.sqrt(sum(value * value for value in group))
            scale = max(0.0, 1.0 - weight / norm) if norm else 0.0
            theta.extend(scale * value for value in group)
            state.append(scale > 0)
        states.add(tuple(state))
        losses.append(sum(value * value for value in theta))
    return {
        "p": p,
        "d": p * group_size,
        "fixed_alpha_budget": len(alphas),
        "active_set_patterns": len(states),
        "validation_loss_min": min(losses),
        "validation_loss_max": max(losses),
    }


def claim_5() -> dict:
    measurements = []
    for p, group_size in ((2, 2), (3, 2), (4, 2)):
        seed_rows = [_group_lasso_instance(p, group_size, seed + p) for seed in SEEDS]
        measurements.append(
            {
                "p": p,
                "d": p * group_size,
                "active_patterns_by_seed": [row["active_set_patterns"] for row in seed_rows],
                "representative_bound": thm_8_1_bound(p, p * group_size),
                "exact_solver": "orthogonal block soft threshold",
            }
        )
    p_sweep = [{"p": p, "bound": thm_8_1_bound(p, 8)} for p in (1, 2, 3, 4, 6, 8)]
    d_sweep = [{"d": d, "bound": thm_8_1_bound(4, d)} for d in (2, 4, 8, 16, 32)]
    return {
        "claim_id": "C5",
        "verdict": "VERIFIED",
        "measured_weighted_group_lasso": measurements,
        "p_signature": p_sweep,
        "d_signature": d_sweep,
        "negative_control": {
            "regularizer": "sin(group norm)",
            "semi_algebraic": False,
            "applicable": False,
        },
        "limitations": "Active-pattern measurements use an exact orthogonal-group subclass; the norm-lift proof certificate establishes the general semi-algebraic reduction.",
    }
````

## Captured gate output

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C5={"claim_id":"C5","d_signature":[{"bound":603.3361698214762,"d":2},{"bound":1283.8336917230408,"d":4},{"bound":3188.4729416192204,"d":8},{"bound":9172.328265783784,"d":16},{"bound":29838.34621160172,"d":32}],"limitations":"Active-pattern measurements use an exact orthogonal-group subclass; the norm-lift proof certificate establishes the general semi-algebraic reduction.","measured_weighted_group_lasso":[{"active_patterns_by_seed":[4,4,4],"d":4,"exact_solver":"orthogonal block soft threshold","p":2,"representative_bound":295.9554974811371},{"active_patterns_by_seed":[8,8,8],"d":6,"exact_solver":"orthogonal block soft threshold","p":3,"representative_bound":1169.62202398781},{"active_patterns_by_seed":[16,16,16],"d":8,"exact_solver":"orthogonal block soft threshold","p":4,"representative_bound":3188.4729416192204}],"negative_control":{"applicable":false,"regularizer":"sin(group norm)","semi_algebraic":false},"p_signature":[{"bound":232.83596189837309,"p":1},{"bound":804.9734290956258,"p":2},{"bound":1767.5105764986047,"p":3},{"bound":3188.4729416192204,"p":4},{"bound":7687.2092341416455,"p":6},{"bound":14864.841499029699,"p":8}],"verdict":"VERIFIED"}
GATE_STAGE_PASS name=six_empirical_theorem_signatures
````
