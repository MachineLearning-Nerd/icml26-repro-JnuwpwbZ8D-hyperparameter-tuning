# C2 method

The checker reconstructs the universal formula, verifies its atom and degree
counts, substitutes `K=1,d_1=d` into C1, and checks the constant-factor
absorptions independently over 64 cases. Fixed command: `uv run --frozen
--python 3.12 repro/src/run_publication_gate.py --output
outputs/publication_gate.json`.
