from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "repro" / "src"))

from check_theorem_signatures import check  # noqa: E402
from measure_theorem_signatures import build_payload, _fused_dual  # noqa: E402


class TheoremSignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        output = ROOT / "outputs" / "theorem_signatures.json"
        if output.is_file():
            cls.payload = json.loads(output.read_text())
        else:
            cls.payload = build_payload()

    def test_independent_checker_passes(self) -> None:
        self.assertEqual(check(self.payload)["verdict"], "SIGNATURE_CHECK_PASS")

    def test_circular_budget_mutation_fails(self) -> None:
        mutated = copy.deepcopy(self.payload)
        mutated["budget_policy"] = "selected from displayed bound"
        result = check(mutated)
        self.assertIn("circular budget", result["failures"])

    def test_fused_solver_kkt(self) -> None:
        _, violation = _fused_dual(
            (0.4, -1.2, 0.7, 1.1),
            (0.2, 0.5, 0.3),
        )
        self.assertLess(violation, 1e-8)

    def test_missing_p_signature_mutation_fails(self) -> None:
        mutated = copy.deepcopy(self.payload)
        for row in mutated["claims"]["C6"]["d2_signature"]:
            row["bound_over_d2"] /= row["d"] - 1
        result = check(mutated)
        self.assertIn("C6 d2 normalization outside calibrated range", result["failures"])


if __name__ == "__main__":
    unittest.main()
