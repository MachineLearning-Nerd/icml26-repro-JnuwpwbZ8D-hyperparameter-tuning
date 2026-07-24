import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "verify_claim1_proof.py"
SPEC = importlib.util.spec_from_file_location("verify_claim1_proof", MODULE_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


class Claim1ProofTests(unittest.TestCase):
    def test_symbolic_and_independent_routes(self) -> None:
        VERIFY.symbolic_check()
        self.assertEqual(VERIFY.independent_check(), 384)

    def test_all_mutations_are_rejected(self) -> None:
        self.assertEqual(len(VERIFY.reject_mutations()), 3)


if __name__ == "__main__":
    unittest.main()
