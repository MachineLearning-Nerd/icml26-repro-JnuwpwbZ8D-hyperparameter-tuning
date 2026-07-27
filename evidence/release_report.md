Previous live judged score: `6/12`

Conservative projected score range after the proposed change: **8–12/12**

Best-supported possible new score: **12/12 forecast, not a judge result**

# Reference-protocol parity release report

The evaluator judged Space SHA
`929165205a02428c2cc7207ddb0f2e187cf913d9` on
2026-07-27 at 05:20:08 UTC and retained 6/12. All six claims were TOY because
the symbolic programs checked only loose algebraic envelopes and the concrete
classes were simplified. The public comparison Space
`tomyimkc/...@59b1a8d8f0645f0c830d433804c8fbfba70231b3` received 12/12 for six
specific routes: theorem substitutions, scaling signatures, named-class
patterns or path regions, and applicability controls.

This release reconstructs those routes independently, fixes an actual C5
formula bug, and makes the raw output and checker directly visible.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| C1 | 1 | 2 | HIGH | VERIFIED | 31/32 and 475/512 halfspace patterns; block ratios 1.885/1.993; sine control |
| C2 | 1 | 2 | HIGH | VERIFIED | one-block substitution; 163/579/1,232 patterns; p/d sweeps |
| C3 | 1 | 2 | HIGH | VERIFIED | f differs from g; 255/1,329/2,652 patterns; d-squared separation |
| C4 | 1 | 2 | HIGH | VERIFIED | 4/6/8 ElasticNet regions; linear path bound versus quadratic QE route |
| C5 | 1 | 2 | HIGH | VERIFIED | corrected G.1 substitution; dense-design 51/100/174 patterns; old formula rejected |
| C6 | 1 | 2 | MEDIUM | VERIFIED | full-rank mp-QP; PSD Hessian; 9/22/38 regions; weight-domain ambiguity remains |

Current total score: **6/12**. Conservative projected total: **8–12/12**.
Best-supported possible total: **12/12**, forecast only. Every claim changed
scientifically from revision 9291652. No claim is marked BLOCKED, but C6
retains a material interpretation risk.

## Experiment tree and fixed command

Parent `orx/final-embedded-certificate-release` is frozen at `c9f159e`.
Child experiment `e86ce5c8-9e75-4e7c-a215-70d02cf7b0e4`,
branch `orx/reference-protocol-parity-and-corrected-theorem`, contains the
clean-room protocols. Calibration run
`f69eb97c-98f5-4224-93d6-1128fcbe198c` emitted all new evidence and an
independent checker pass, then failed closed at the intentionally stale page
audit. Cumulative run `c43d6308-5846-404a-b75e-c4846409effb` then passed the
unchanged command at commit `859f229a2b477b163662c2f77ff7961b8619b240`:
all six claims, 21 tests, the independent checker, 122 manifest hashes, and
zero visibility gaps. The final metadata-only child is
`8d091b9a-bdf8-4167-b735-7b0d2c9acf8e`.

Every node uses:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

The calibration estimated one core and 1–2 minutes. It selected local CPU,
enforced a one-thread BLAS/OpenMP cap, and measured 7.200243542 seconds for the
committed calibration evidence. The successful cumulative rerun measured
4.693270541 seconds for the same stage. Hugging Face cpu-upgrade was not
required. Cost: $0.

## Evidence and visibility

- canonical page: `pages/current-verification/page.md`
- claim pages: `pages/current-c1/page.md` through `current-c6/page.md`
- executable source: `repro/src/measure_theorem_signatures.py`
- independent checker: `repro/src/check_theorem_signatures.py`
- raw JSON: `.openresearch/artifacts/reference_protocols/raw_output.json`
- checker output: `.openresearch/artifacts/reference_protocols/checker_output.json`

The important correction is C5. The previous numeric implementation added an
extra factor d. The new Appendix G.1 substitution uses one block of dimension
d+2p, M=2(1+2p), and degree 2; the checker rejects the old mutation.

The historical judged file set remains reachable. The final allowlist contains
123 text paths and its non-self manifest contains 122 hashes. A fresh candidate
download is traversed only from the canonical entrypoint before upload, and
the process is repeated after publication.

## Exact publication action

After every cumulative gate passes, upload only the exact text allowlist to
the existing Space `DineshAI/JnuwpwbZ8D` using the text-only Hugging Face API.
Then download the exact revision, verify every hash, repeat the evaluator-blind
traversal, mirror the published text to GitHub main, confirm with
`git ls-remote`, and await the live judge. No score increase is claimed before
that judgment.
