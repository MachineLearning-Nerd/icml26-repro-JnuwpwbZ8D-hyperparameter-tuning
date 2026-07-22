# Tests and gate


---
<!-- trackio-cell
{"type": "code", "id": "cell_4f712e58a345", "created_at": "2026-07-22T12:06:24+00:00", "title": "Unit tests", "command": [".venv/bin/python", "-m", "unittest", "discover", "-s", "repro/tests", "-v"], "exit_code": 0, "duration_s": 0.083}
-->
````bash
$ .venv/bin/python -m unittest discover -s repro/tests -v
````

exit 0 · 0.1s


````output
test_all_six_independent_checks (test_hyperparameters.HyperparameterTuningTests.test_all_six_independent_checks) ... ok
test_negative_controls_are_rejected (test_hyperparameters.HyperparameterTuningTests.test_negative_controls_are_rejected) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_fa1ae58c21cb", "created_at": "2026-07-22T12:06:25+00:00", "title": "Fail-closed publication gate", "command": [".venv/bin/python", "repro/src/run_publication_gate.py", "--output", "outputs/publication_gate.json"], "exit_code": 0, "duration_s": 0.188}
-->
````bash
$ .venv/bin/python repro/src/run_publication_gate.py --output outputs/publication_gate.json
````

exit 0 · 0.2s


````python title=run_publication_gate.py
#!/usr/bin/env python3
"""Fail-closed publication gate for the deterministic theorem verifier."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "publication_gate.json")
    args = parser.parse_args()
    verifier_output = ROOT / "outputs" / "verification.json"
    subprocess.run([sys.executable, "repro/src/verify_hyperparameters.py", "--output", str(verifier_output)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
    verification = json.loads(verifier_output.read_text())
    passed = verification["all_claims_passed"] and len(verification["claims"]) == 6
    payload = {
        "paper": "JnuwpwbZ8D",
        "tests_passed": True,
        "claims_passed": len(verification["claims"]),
        "publication_gate_passed": passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

````


````json title=publication_gate.json
{
  "claims_passed": 6,
  "paper": "JnuwpwbZ8D",
  "publication_gate_passed": true,
  "tests_passed": true
}

````


````output
{"all_claims_passed": true, "claims": 6, "paper": "JnuwpwbZ8D"}
test_all_six_independent_checks (test_hyperparameters.HyperparameterTuningTests.test_all_six_independent_checks) ... ok
test_negative_controls_are_rejected (test_hyperparameters.HyperparameterTuningTests.test_negative_controls_are_rejected) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
{"claims_passed": 6, "paper": "JnuwpwbZ8D", "publication_gate_passed": true, "tests_passed": true}

````
