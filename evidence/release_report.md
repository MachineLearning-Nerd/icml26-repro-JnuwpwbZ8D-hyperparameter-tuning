Previous live judged score: `6/12`

Conservative projected score range after the proposed change: **11–12/12**

Best-supported possible new score: **12/12 forecast, not a judge result**

# Final release report

The live evaluator judged Space revision
`e41343cf30154ab7e49464ce303fc5ed1b56ea05` at
`2026-07-27T04:11:17+00:00` and retained `6/12`. It found the inline finite
experiments but said the distinct SymPy theorem certificates were referenced
rather than embedded. The prior audit had therefore proved visibility of the
corroborating experiment, not visibility of the theorem-level route.
Experiment `dbf76dd4-46a2-498f-a15f-9a3d2da9cbcf`
(`orx/embed-symbolic-theorem-certificates`) answers that exact failure: every
current claim page now embeds the complete applicable proof program and stable
proof output in addition to its finite experiment. A root-level current page
also exposes both complete certificate programs and the C1–C6 mapping.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| C1 | 1 | 2 | HIGH | VERIFIED | QE-to-GJ proof plus exact halfspace shattering and `2^K` sweep |
| C2 | 1 | 2 | HIGH | VERIFIED | One-block proof plus three-seed two-piece-quadratic patterns |
| C3 | 1 | 2 | HIGH | VERIFIED | Two-block proof plus genuine `f != g` patterns and `d²` separation |
| C4 | 1 | 2 | HIGH | VERIFIED | Direct GJ proof plus exact orthogonal ElasticNet path regions |
| C5 | 1 | 2 | HIGH | VERIFIED | Norm-lift proof plus exact block soft-threshold active patterns |
| C6 | 1 | 2 | MEDIUM | VERIFIED | KKT-checked nonnegative-weight paths; printed all-real notation remains broader |

Current total score: **6/12**. Conservative projected total: **11–12/12**.
Best-supported possible total: **12/12**, forecast only. All six claims changed
from TOY evidence to proof-certificate evidence. No claim is BLOCKED. C6 is the
only MEDIUM-confidence claim and retains the explicit negative-weight
proof-domain risk.

## Experiment tree and winner

The frozen baseline is `orx/frozen-judged-baseline`. Round 1 promoted the C1
symbolic certificate and falsification audit. Round 2 compared C2–C6 positive
certificates with assumption-aware counterexample audits, then merged them
only on a new child. The scientific corrective child was
`orx/empirical-theorem-signature-release`. Its first run
`a982ff28-c284-492e-9ff8-aeb54b178592` completed all new scientific checks,
then failed closed because the prior release manifest did not list the new
files. The cumulative successor run
`480450c8-f8f1-4f6f-ad74-21b4dc490ab0` at
`177668a1312bde3215e9778b2cc43f51dabd8a21` passed the full gate in 10 seconds:
six VERIFIED claims, `SIGNATURE_CHECK_PASS`, 16 tests, 118 text paths, and 117
validated hashes. The later release at `01db7fab...` was scientifically
unchanged but did not make its executable source visible in the form consumed
by the evaluator. The judge-directed visibility correction first failed closed
on a byte-different blank line in five embedded code blocks, then passed after
that presentation defect was corrected. Run
`4d4a3555-a313-4b8d-b38a-c191809d01d6` passed the complete gate in 10 seconds:
six VERIFIED claims, `SIGNATURE_CHECK_PASS`, zero visibility-matrix omissions,
118 validated candidate hashes, the secret scan, the notebook check, and 18
unit tests.

## Commands

The exact fixed reproduction command on every formal node was:

```bash
uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json
```

Formal orchestration commands used were `orx create-experiment ... --parent
<id>`, `orx exp run <id> --backend local`, `orx exp wait <id> --timeout 480`,
`orx runs d69602ab-4834-46c6-b762-c17b9a2685bc`, and `orx logs <run-id>`.
Startup/source commands included `orx projects --json`, `orx project view`,
`orx paper 2602.02406 --full`, `orx skill` and the four mandatory native skill
reads, `git status --short`, `git branch -a`, `git ls-remote`, `df -h`, and a
User-Agent-bearing HTTP retrieval of the ar5iv HTML. Release checks used
`marimo check notebooks/theorem_certificates.py`, JSON parsing, SVG XML
validation, SHA-256 verification, a fresh Git clone, and a root-only Markdown
link traversal.

## Evidence, compute, and preservation

Evaluator-visible pages are under `pages/current-*`; code is under `repro/`;
machine-readable evidence is under `.openresearch/artifacts/`; the illustrated
report and notebook are under `reports/theorem-certificates/` and `notebooks/`.
The immutable judged manifest is
`evidence/judged-space-a928c531.sha256`.

Thirteen formal local CPU runs consumed 130 seconds total, including three
fail-closed release/fixture/visibility checks. Each was estimated at one
core, used one Python process, and was confidently under five minutes. Hugging Face
`cpu-upgrade` was therefore not used. Local and Hugging Face compute cost: $0.

All 23 judged paths remain in the candidate tree; 19 historical pages/assets
available in the repository mirror are byte-for-byte hash verified. The old
README/logbook navigation is superseded, while every historical evidence page
is unchanged and reachable beneath the exact label **Historical rejected
baseline — archive**. The corrected upload allowlist contains 119 text paths;
its non-self manifest contains 118 hashes.

## Publication action

After the final gate passes, upload exactly the paths in
`evidence/hf_upload_allowlist.txt` through the text-only Hugging Face API to
the existing Space `DineshAI/JnuwpwbZ8D`; do not create a Space. Then download
that exact revision, verify `evidence/candidate_text_manifest.sha256`, repeat
the blind traversal, fast-forward GitHub `main` to the identical release
commit, and confirm it with `git ls-remote`. Mark the paper awaiting judge and
do not claim a score increase.
