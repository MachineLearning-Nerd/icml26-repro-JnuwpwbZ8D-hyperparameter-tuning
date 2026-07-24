import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "audit_evaluator_visibility.py"
SPEC = importlib.util.spec_from_file_location("audit_evaluator_visibility", MODULE_PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


class VisibilityTests(unittest.TestCase):
    def test_manifest_parser_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = root / "sample.txt"
            sample.write_text("visible\n")
            digest = AUDIT.sha256(sample)
            manifest = root / "manifest.sha256"
            manifest.write_text(f"{digest}  sample.txt\n")
            self.assertEqual(AUDIT.parse_manifest(manifest), {"sample.txt": digest})


if __name__ == "__main__":
    unittest.main()
