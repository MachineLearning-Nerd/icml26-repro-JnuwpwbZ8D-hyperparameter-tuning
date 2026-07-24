import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "verify_claims2_6_proofs.py"
SPEC = importlib.util.spec_from_file_location("verify_claims2_6_proofs", MODULE_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


class ClaimSpecializationTests(unittest.TestCase):
    def test_all_specializations(self) -> None:
        expected_cases = {"C2": 128, "C3": 128, "C4": 128, "C5": 12, "C6": 5}
        for function in (VERIFY.c2, VERIFY.c3, VERIFY.c4, VERIFY.c5, VERIFY.c6):
            result = function()
            self.assertEqual(result["verdict"], "VERIFIED")
            self.assertEqual(result["independent_checker_cases"], expected_cases[result["claim_id"]])

    def test_source_anchors_and_controls(self) -> None:
        VERIFY.source_and_controls()


if __name__ == "__main__":
    unittest.main()
