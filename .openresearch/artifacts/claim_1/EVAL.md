# C1 — Theorem 4.1 symbolic certificate

Verdict: **VERIFIED**

The exact main-source contract is reconstructed from the stated
quantifier-elimination and GJ lemmas. The symbolic checker proves the displayed
big-O form, an independent implementation covers 384 parameter/constant
combinations, and all three targeted mutations are rejected.

- Raw result: [`raw_output.json`](raw_output.json)
- Contract: [`claim_contract.json`](claim_contract.json)
- Certificate: [`proof_certificate.json`](proof_certificate.json)
- Source audit: [`source_audit.md`](source_audit.md)
- Method: [`method.md`](method.md)
- Limitations: [`limitations.md`](limitations.md)

The historical formula-substitution verifier is superseded for C1. It remains
preserved as **Historical rejected baseline** evidence.
