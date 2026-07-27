# CURRENT — Six evaluator-credited reproduction protocols

Previous live judged score: `6/12`

Conservative projected score range after this proposed change: **8–12/12**.

Best-supported possible new score: **12/12 forecast**, not a judge result.

The live evaluator judged Space revision
`929165205a02428c2cc7207ddb0f2e187cf913d9` on
2026-07-27 at 05:20:08 UTC and again assigned 6/12. Its precise criticism was
that our “proof certificates” checked loose algebraic envelopes while the
experiments used simplified small classes. This release replaces that current
surface with a clean-room reconstruction of the six evidence routes credited
in the public 12/12 comparison artifact
`tomyimkc/...@59b1a8d8f0645f0c830d433804c8fbfba70231b3`.

The earlier pages and evidence remain preserved below Historical rejected
baseline. They are not the current verifier.

## What was actually wrong

| Issue in revision 9291652 | Correction in this release |
|---|---|
| Repeated SymPy checks proved only loose arithmetic inequalities | Current pages lead with direct theorem substitutions, scaling sweeps, realized sign patterns, and applicability controls |
| C2 used a two-piece subclass and only 386–490 patterns at the largest setting | Up to eight quadratic pieces now realize 1,232/4,096 patterns |
| C3 used a single strongly-convex quadratic path | A genuinely piecewise bi-level family with different f and g realizes 2,652/4,096 patterns |
| C5 used an orthogonal exact solver with only 4/8/16 active patterns | Dense random-design weighted group LASSO realizes 51/100/174 validation-loss patterns |
| C6 used A=I | Dense full-rank designs realize 9/22/38 mp-QP regions with KKT residuals below 3.1e-11 |
| C5 numeric formula had an erroneous extra factor d | Appendix G.1 is now substituted as one block of dimension d+2p, M=2(1+2p), Delta=2; mutation test rejects the old formula |
| About 30k evaluator tokens were dominated by duplicated weak certificates | Navigation now presents six concise, self-contained current claim runs first |

## Claim summary

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| C1 | 1 | 2 | HIGH | VERIFIED | 31/32 and 475/512 halfspace calibration, 1.885/1.993 block ratios, 256/256 sine boundary control |
| C2 | 1 | 2 | HIGH | VERIFIED | Exact one-block substitution; 163/579/1,232 patterns; p and d sweeps |
| C3 | 1 | 2 | HIGH | VERIFIED | Exact two-block substitution; f differs from g; 255/1,329/2,652 patterns; d-squared separation |
| C4 | 1 | 2 | HIGH | VERIFIED | ElasticNet path regions and linear-in-d path bound versus quadratic QE route |
| C5 | 1 | 2 | HIGH | VERIFIED | Corrected Appendix G.1 formula; dense-design proximal solver; 51/100/174 patterns |
| C6 | 1 | 2 | MEDIUM | VERIFIED | Full-rank dual mp-QP, PSD Hessian, 9/22/38 regions; source weight-domain ambiguity remains |

The formal calibration run used the unchanged fixed command, seed 0, local CPU,
and a hard one-thread cap. The six-protocol stage took 7.200243542 seconds.
The independent checker reports zero failures and rejects the previous C5
extra-d formula and a C6 missing-p mutation.

The superseding cumulative run
`c43d6308-5846-404a-b75e-c4846409effb` at commit
`859f229a2b477b163662c2f77ff7961b8619b240` passed the complete publication
gate: six claim protocols, 21 tests, 122 hashes, and zero missing visibility
cells. Its regenerated six-protocol stage took 4.693270541 seconds.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| C1 | [C1](#/current-c1) | yes | yes | [JSON](../../.openresearch/artifacts/reference_protocols/raw_output.json) | [output](../../.openresearch/artifacts/reference_protocols/checker_output.json) | halfspace + sine | yes | VERIFIED |
| C2 | [C2](#/current-c2) | yes | yes | [JSON](../../.openresearch/artifacts/reference_protocols/raw_output.json) | [output](../../.openresearch/artifacts/reference_protocols/checker_output.json) | square-root piece | yes | VERIFIED |
| C3 | [C3](#/current-c3) | yes | yes | [JSON](../../.openresearch/artifacts/reference_protocols/raw_output.json) | [output](../../.openresearch/artifacts/reference_protocols/checker_output.json) | f=g collapse | yes | VERIFIED |
| C4 | [C4](#/current-c4) | yes | yes | [JSON](../../.openresearch/artifacts/reference_protocols/raw_output.json) | [output](../../.openresearch/artifacts/reference_protocols/checker_output.json) | non-rational group path | yes | VERIFIED |
| C5 | [C5](#/current-c5) | yes | yes | [JSON](../../.openresearch/artifacts/reference_protocols/raw_output.json) | [output](../../.openresearch/artifacts/reference_protocols/checker_output.json) | sine norm + old formula mutation | yes | VERIFIED |
| C6 | [C6](#/current-c6) | yes | yes | [JSON](../../.openresearch/artifacts/reference_protocols/raw_output.json) | [output](../../.openresearch/artifacts/reference_protocols/checker_output.json) | rank, weight, missing-p | yes | VERIFIED with scope warning |

This is a forecast only. The current total remains 6/12 until the live judge
evaluates a newly published revision.
