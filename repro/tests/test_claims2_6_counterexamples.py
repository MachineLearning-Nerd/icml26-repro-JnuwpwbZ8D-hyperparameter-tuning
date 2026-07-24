import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "audit_claims2_6_counterexamples.py"
SPEC = importlib.util.spec_from_file_location("audit_claims2_6_counterexamples", MODULE_PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


class CounterexampleAuditTests(unittest.TestCase):
    def test_unattained_candidate_is_not_a_defined_loss(self) -> None:
        result = AUDIT.discontinuous_compact_infimum()
        self.assertFalse(result["minimum_attained"])
        self.assertEqual(result["classification"], "ASSUMPTION_GAP_NOT_COUNTEREXAMPLE")

    def test_nonunique_candidate_violates_explicit_assumption(self) -> None:
        result = AUDIT.nonunique_path_candidate()
        self.assertEqual(len(result["minimizers"]), 2)

    def test_signed_group_lift_is_exact(self) -> None:
        result = AUDIT.signed_norm_lift()
        self.assertEqual(result["classification"], "REJECTED_AS_COUNTEREXAMPLE")

    def test_negative_fused_weight_exposes_proof_domain_gap(self) -> None:
        result = AUDIT.negative_fused_weight()
        self.assertEqual(len(result["global_minimizers"]), 2)
        self.assertEqual(result["minimum_value"], -4.0)


if __name__ == "__main__":
    unittest.main()
