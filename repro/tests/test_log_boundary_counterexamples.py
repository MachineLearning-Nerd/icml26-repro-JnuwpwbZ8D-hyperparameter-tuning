import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "audit_log_boundary_counterexamples.py"
SPEC = importlib.util.spec_from_file_location("audit_log_boundary_counterexamples", MODULE_PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


class LogBoundaryCounterexampleTests(unittest.TestCase):
    def test_all_labelings_are_realized(self) -> None:
        for p in range(1, 9):
            rows = AUDIT.shattered_labelings(p)
            self.assertEqual(len(rows), 2**p)
            self.assertTrue(all(row["labels"] == row["observed"] for row in rows))

    def test_both_printed_factors_are_zero(self) -> None:
        payload = AUDIT.build_payload(3)
        self.assertEqual(payload["claims"]["C1"]["printed_rhs_factor"], 0)
        self.assertEqual(payload["claims"]["C4"]["printed_rhs_factor"], 0)
        self.assertTrue(payload["corrected_control"]["compatible_with_witness"])

    def test_finite_enumeration_is_not_labeled_as_proof(self) -> None:
        payload = AUDIT.build_payload(2)
        self.assertEqual(payload["finite_sweeps_used_as_proof"], 0)
        self.assertIn("algebraic identity is the proof", payload["enumeration"]["scope"])


if __name__ == "__main__":
    unittest.main()
