import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "verify_hyperparameters.py"
SPEC = importlib.util.spec_from_file_location("verify_hyperparameters", MODULE_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


class HyperparameterTuningTests(unittest.TestCase):
    def test_all_six_independent_checks(self) -> None:
        self.assertEqual(VERIFY.check_fol_formula()["cases"], 96)
        self.assertEqual(VERIFY.check_training_identity()["finite_universal_cases"], 189)
        self.assertEqual(VERIFY.check_validation_identity()["finite_argmin_cases"], 75)
        self.assertEqual(VERIFY.check_rational_path()["piecewise_rational_cases"], 300)
        self.assertEqual(VERIFY.check_group_lasso()["kkt_cases"], 15)
        self.assertEqual(VERIFY.check_fused_lasso()["kkt_path_cases"], 153)

    def test_negative_controls_are_rejected(self) -> None:
        fol = VERIFY.check_fol_formula()
        self.assertGreater(fol["correct_expression"], fol["rejected_missing_plus_one"])
        group = VERIFY.check_group_lasso()
        self.assertLess(group["rejected_negative_nu"], 0)
        fused = VERIFY.check_fused_lasso()
        self.assertGreater(fused["rejected_wrong_threshold_difference"], 0)


if __name__ == "__main__":
    unittest.main()
