# Limitations and deviations

- Quantifier elimination, Goldberg--Jerrum, and the Bemporad mp-QP theorem are
  explicit trusted dependencies, not re-proved from first principles.
- The C1/C4 falsifications target the literal unguarded logarithms; guarded
  variants such as `log(1+z)` are not refuted.
- C2 and C3 use the attainment/nonempty-argmin condition needed by the paper's
  written minimum and strict-witness formulas.
- The C4 witness satisfies the singleton rational-path assumption exactly.
- C5 uses nonempty groups, so `p<=d`.
- C6 is verified with MEDIUM confidence only on the conventional
  nonnegative-weight domain required by its proof. The all-real typesetting
  remains a proof-domain gap.
- No finite parameter sweep is used to establish a universal theorem.
