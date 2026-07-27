# CURRENT — Reproduction command and independent checker

The fixed command is unchanged across the experiment tree:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

The candidate protocol was calibrated in formal OpenResearch run
`f69eb97c-98f5-4224-93d6-1128fcbe198c` from commit `8aef1f4`.
Estimate: one CPU core and 1–2 minutes. Selection: local CPU because the
single-thread job was confidently below five minutes. Actual six-protocol
runtime: 7.200243542 seconds; the whole failed calibration run stopped after
the deliberately stale presentation audit.

The current executable routes are:

- [six-claim protocol source](../../repro/src/measure_theorem_signatures.py)
- [independent fail-closed checker](../../repro/src/check_theorem_signatures.py)
- [raw machine-readable run output](../../.openresearch/artifacts/reference_protocols/raw_output.json)
- [checker output](../../.openresearch/artifacts/reference_protocols/checker_output.json)

The checker exits nonzero if any calibrated control, substitution, scaling
signature, lower-bound comparison, rank/KKT condition, or mutation test fails.
Its exact result is:

```output
{"claims_checked":6,"failures":[],"independent_formula_and_invariant_checker":true,"mutations_rejected":["C5_extra_d_factor","C6_missing_p_factor"],"verdict":"SIGNATURE_CHECK_PASS"}
```

Historical formula and symbolic-certificate routes are retained for audit but
are no longer presented as the current theorem verifier.
