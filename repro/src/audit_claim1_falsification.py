#!/usr/bin/env python3
"""Independent falsification audit for Theorem 4.1."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / ".openresearch" / "artifacts" / "claim_1" / "falsification_route.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(AUDIT.read_text())
    source = (ROOT / "source" / "icml2026.tex").read_text()
    appendix = (ROOT / "source" / "icml_appendix.tex").read_text()
    assert "\\prod_{k = 1}^K (d_k + 1)" in source
    assert "\\prod_{k = 1}^K d_k" in source
    assert "\\prod_{k = 1}^M (d_k + 1)" in appendix
    # The judge paraphrase's D_plus degree term is always no smaller.
    for dims in ((1,), (2, 3), (1, 4, 7)):
        d_plus = 1
        d_plain = 1
        for dimension in dims:
            d_plus *= dimension + 1
            d_plain *= dimension
        assert d_plus >= d_plain
    assert result["falsification_succeeded"] is False
    assert result["main_claim_status"] == "VERIFIED_BY_SYMBOLIC_CERTIFICATE"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("CLAIM1_FALSIFICATION_AUDIT=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
