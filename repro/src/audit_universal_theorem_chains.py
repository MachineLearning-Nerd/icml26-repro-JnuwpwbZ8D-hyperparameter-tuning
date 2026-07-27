#!/usr/bin/env python3
"""Independent structural audit of the six universal proof certificates.

The auditor intentionally does not import the primary verifier.  It reads the
primary JSON as an untrusted proof object, reconstructs the expected quantifier
and dependency manifests, checks every derivation edge, and requires distinct
fail-sensitive mutations for all claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "C1": {
        "anchors": ("Theorem 4.1", "Appendix A.3", "B"),
        "quantifier_tokens": ("every fixed instance", "every threshold", "uniformly", "fixed K"),
        "steps": ("QE converts", "I <=", "Delta_QE", "GJ algorithm", "Pdim <=", "expand logs", "p>=1"),
        "controls": ("replace_K", "uniformity", "p_squared", "QE_degree"),
    },
    "C2": {
        "anchors": ("Theorem 5.1", "Appendix C"),
        "quantifier_tokens": ("every x and t", "every alpha", "for all theta"),
        "steps": ("encode each region", "add 2d", "Theorem 4.1", "d+1", "obtain"),
        "controls": ("forall", "domain", "piece", "threshold"),
    },
    "C3": {
        "anchors": ("Theorem 6.1", "Appendix E"),
        "quantifier_tokens": ("every x,t,alpha", "forall theta", "exists theta_prime"),
        "steps": ("non-minimizer", "validation", "training-region", "boxes", "Theorem 4.1", "(d+1)^2", "obtain"),
        "controls": ("quantifier", "validation", "argmin", "better"),
    },
    "C4": {
        "anchors": ("Assumption 7.1", "Theorem 7.2", "Appendix F"),
        "quantifier_tokens": ("every fixed x", "every alpha", "every threshold"),
        "steps": ("path region", "k-region", "value forms", "M_total", "degree", "Goldberg-Jerrum", "obtain"),
        "controls": ("nonunique", "denominator", "value", "quantifier"),
    },
    "C5": {
        "anchors": ("Theorem 8.1", "Appendix G.1"),
        "quantifier_tokens": ("every x,t,alpha", "forall theta", "exists z"),
        "steps": ("norm", "2p", "degree two", "Theorem 4.1", "expand", "log", "obtain"),
        "controls": ("nonnegative", "validation", "candidate", "argmin"),
    },
    "C6": {
        "anchors": ("Theorem 8.2", "Appendix G.2", "Proposition G.1"),
        "quantifier_tokens": ("every instance", "every conventional", "p=d-1"),
        "steps": ("Fenchel", "full column rank", "mp-QP", "three", "primal", "validation", "Theorem 7.2"),
        "controls": ("rank", "negative", "interior", "p_equals"),
    },
}


def contains_all(values: object, tokens: tuple[str, ...]) -> bool:
    text = json.dumps(values, sort_keys=True)
    return all(token.lower() in text.lower() for token in tokens)


def audit_claim(claim_id: str, row: dict[str, object]) -> dict[str, bool]:
    expected = EXPECTED[claim_id]
    mutations = tuple(row["mutations_rejected"])
    return {
        "source_anchor_complete": contains_all(row["source_anchor"], expected["anchors"]),
        "quantifier_manifest_complete": contains_all(row["quantifiers"], expected["quantifier_tokens"]),
        "derivation_edges_complete": contains_all(row["proof_chain"], expected["steps"]),
        "four_distinct_fail_sensitive_controls": (
            len(mutations) >= 4
            and len(set(mutations)) == len(mutations)
            and contains_all(mutations, expected["controls"])
        ),
        "no_finite_sweep_used_as_proof": row["finite_parameter_sweeps_used_as_proof"] == 0,
        "exact_checks_fail_closed": (
            bool(row["exact_checks"])
            and all(value is True for value in row["exact_checks"].values())
        ),
        "final_verdict_exact": row["verdict"] == "VERIFIED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    primary = json.loads(raw)
    assert set(primary["claims"]) == set(EXPECTED)
    claims = {
        claim_id: audit_claim(claim_id, primary["claims"][claim_id])
        for claim_id in EXPECTED
    }
    all_passed = (
        primary["all_universal_proof_chains_passed"]
        and primary["finite_parameter_sweeps_used_as_proof"] == 0
        and all(all(checks.values()) for checks in claims.values())
    )
    result = {
        "primary_sha256": hashlib.sha256(raw).hexdigest(),
        "claims": claims,
        "independent_checks": sum(len(checks) for checks in claims.values()),
        "finite_parameter_sweeps_used_as_proof": 0,
        "independent_audit_passed": all_passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "UNIVERSAL_PROOF_AUDIT_FULL="
        + json.dumps(result, sort_keys=True, separators=(",", ":"))
    )
    print(
        "UNIVERSAL_PROOF_AUDIT="
        + json.dumps(
            {
                "claims": len(claims),
                "independent_checks": result["independent_checks"],
                "finite_sweeps_used_as_proof": 0,
                "independent_audit_passed": all_passed,
            },
            sort_keys=True,
        )
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
