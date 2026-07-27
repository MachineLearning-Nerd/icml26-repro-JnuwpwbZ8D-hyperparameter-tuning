Previous live judged score: `6/12`

Conservative projected score range after the proposed change: **11–12/12**

Best-supported possible new score: **12/12 forecast, not a judge result**

# Final release report

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
only on a new child. The corrective child is
`orx/empirical-theorem-signature-release`. Its first run
`a982ff28-c284-492e-9ff8-aeb54b178592` completed all new scientific checks,
then failed closed because the prior release manifest did not list the new
files. The cumulative successor run
`480450c8-f8f1-4f6f-ad74-21b4dc490ab0` at
`177668a1312bde3215e9778b2cc43f51dabd8a21` passed the full gate in 10 seconds:
six VERIFIED claims, `SIGNATURE_CHECK_PASS`, 16 tests, 118 text paths, and 117
validated hashes.

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

Ten formal local CPU runs consumed approximately 100 seconds total, including
two expected fail-closed release/fixture checks. Each was estimated at one
core, used one Python process, and was confidently under five minutes. Hugging Face
`cpu-upgrade` was therefore not used. Local and Hugging Face compute cost: $0.

All 23 judged paths remain in the candidate tree; 19 historical pages/assets
available in the repository mirror are byte-for-byte hash verified. The old
README/logbook navigation is superseded, while every historical evidence page
is unchanged and reachable under the exact label **Historical rejected
baseline**.

## Publication action

After the final gate passes, upload exactly the paths in
`evidence/hf_upload_allowlist.txt` through the text-only Hugging Face API to
the existing Space `DineshAI/JnuwpwbZ8D`; do not create a Space. Then download
that exact revision, verify `evidence/candidate_text_manifest.sha256`, repeat
the blind traversal, fast-forward GitHub `main` to the identical release
commit, and confirm it with `git ls-remote`. Mark the paper awaiting judge and
do not claim a score increase.
