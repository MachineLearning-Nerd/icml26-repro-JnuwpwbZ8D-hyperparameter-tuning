# Limitations and deviations

- Quantifier elimination, Goldberg--Jerrum, and the Bemporad mp-QP theorem are
  explicit trusted dependencies, not re-proved from first principles.
- C2 and C3 use the attainment/nonempty-argmin condition needed by the paper's
  written minimum and strict-witness formulas.
- C4 is conditional on the paper's singleton rational-path assumption.
- C5 uses nonempty groups, so `p<=d`.
- C6 is verified with MEDIUM confidence only on the conventional
  nonnegative-weight domain required by its proof. The all-real typesetting
  remains a proof-domain gap.
- No finite parameter sweep is used to establish a universal theorem.
