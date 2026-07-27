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

    def test_empirical_only_page_is_not_symbolic_code_visible(self) -> None:
        root = Path(__file__).resolve().parents[2]
        page = (root / "pages/current-c2/page.md").read_text()
        empirical = AUDIT.fenced_source(
            page,
            "repro/src/measure_theorem_signatures.py",
        )
        with self.assertRaises(AssertionError):
            AUDIT.fenced_source(
                f"````python title=repro/src/measure_theorem_signatures.py\n{empirical}\n````",
                "repro/src/verify_claims2_6_proofs.py",
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
            1: ("_count_patterns", "thm_a3_bound", "thm_4_1_bound", "claim_1"),
            2: (
                "_count_patterns", "thm_4_1_bound", "thm_5_1_bound",
                "_piecewise_polynomial_count", "claim_2",
            ),
            3: (
                "_count_patterns", "thm_4_1_bound", "thm_5_1_bound",
                "thm_6_1_bound", "_bilevel_count", "claim_3",
            ),
            4: (
                "thm_4_1_bound", "thm_6_1_bound", "thm_7_2_bound",
                "_soft_threshold", "claim_4",
            ),
            5: (
                "_count_patterns", "thm_4_1_bound", "thm_8_1_bound",
                "_solve_group_lasso_batch", "_group_lasso_patterns",
                "_norm_nonpolynomial_check", "claim_5",
            ),
            6: (
                "thm_7_2_bound", "thm_8_2_bound", "_difference_matrix",
                "_solve_box_qp_batch", "_fused_measurement", "claim_6",
            ),
        }
        for claim, names in functions.items():
            page = (root / f"pages/current-c{claim}/page.md").read_text()
            displayed = AUDIT.fenced_source(
                page,
                "repro/src/measure_theorem_signatures.py",
            )
            self.assertEqual(displayed, AUDIT.function_segments(source, names))

    def test_current_claims_link_raw_protocol_and_checker(self) -> None:
        root = Path(__file__).resolve().parents[2]
        for claim in range(1, 7):
            page = (root / f"pages/current-c{claim}/page.md").read_text()
            self.assertIn(
                ".openresearch/artifacts/reference_protocols/raw_output.json",
                page,
            )
            self.assertIn(
                ".openresearch/artifacts/reference_protocols/checker_output.json",
                page,
            )


if __name__ == "__main__":
    unittest.main()
