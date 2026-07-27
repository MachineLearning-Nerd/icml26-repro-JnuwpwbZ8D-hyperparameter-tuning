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

    def test_link_only_page_is_not_code_visible(self) -> None:
        with self.assertRaises(AssertionError):
            AUDIT.fenced_source(
                "[Verifier source](../../repro/src/measure_theorem_signatures.py)",
                "repro/src/measure_theorem_signatures.py",
            )

    def test_historical_candidate_supports_downloaded_space(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            published = root / "pages" / "historical.md"
            published.parent.mkdir(parents=True)
            published.write_text("published\n")
            self.assertEqual(
                AUDIT.historical_candidate(root, "pages/historical.md"),
                published,
            )
            mirror = root / ".trackio" / "logbook" / "pages" / "historical.md"
            mirror.parent.mkdir(parents=True)
            mirror.write_text("mirror\n")
            self.assertEqual(
                AUDIT.historical_candidate(root, "pages/historical.md"),
                mirror,
            )

    def test_current_claim_fences_match_executed_functions(self) -> None:
        root = Path(__file__).resolve().parents[2]
        source = (root / "repro/src/measure_theorem_signatures.py").read_text()
        functions = {
            1: ("claim_1",),
            2: ("_piecewise_polynomial_count", "claim_2"),
            3: ("_bilevel_count", "claim_3"),
            4: ("_soft_threshold", "claim_4"),
            5: ("_group_lasso_instance", "claim_5"),
            6: ("_fused_dual", "_fused_measurement", "claim_6"),
        }
        for claim, names in functions.items():
            page = (root / f"pages/current-c{claim}/page.md").read_text()
            displayed = AUDIT.fenced_source(
                page,
                "repro/src/measure_theorem_signatures.py",
            )
            self.assertEqual(displayed, AUDIT.function_segments(source, names))


if __name__ == "__main__":
    unittest.main()
