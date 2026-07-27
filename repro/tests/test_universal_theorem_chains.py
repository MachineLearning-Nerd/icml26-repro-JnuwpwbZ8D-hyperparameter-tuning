import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIMARY_PATH = ROOT / "repro/src/verify_universal_theorem_chains.py"
SPEC = importlib.util.spec_from_file_location("universal_proofs", PRIMARY_PATH)
PRIMARY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = PRIMARY
SPEC.loader.exec_module(PRIMARY)


class UniversalTheoremChainTests(unittest.TestCase):
    def test_all_six_quantified_chains(self) -> None:
        result = PRIMARY.certificate()
        self.assertTrue(result["all_universal_proof_chains_passed"])
        self.assertEqual(result["claim_count"], 6)
        self.assertEqual(result["finite_parameter_sweeps_used_as_proof"], 0)
        self.assertGreaterEqual(result["total_mutations_rejected"], 24)

    def test_each_claim_has_quantifiers_dependencies_and_controls(self) -> None:
        result = PRIMARY.certificate()
        for row in result["claims"].values():
            self.assertGreaterEqual(len(row["quantifiers"]), 3)
            self.assertGreaterEqual(len(row["proof_chain"]), 5)
            self.assertGreaterEqual(len(row["mutations_rejected"]), 4)
            self.assertTrue(row["exact_checks"])
            self.assertTrue(all(value is True for value in row["exact_checks"].values()))

    def test_independent_auditor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            primary_path = Path(directory) / "primary.json"
            audit_path = Path(directory) / "audit.json"
            primary_path.write_text(json.dumps(PRIMARY.certificate()))
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "repro/src/audit_universal_theorem_chains.py"),
                    "--input",
                    str(primary_path),
                    "--output",
                    str(audit_path),
                ],
                check=True,
                cwd=ROOT,
            )
            self.assertTrue(json.loads(audit_path.read_text())["independent_audit_passed"])


if __name__ == "__main__":
    unittest.main()
