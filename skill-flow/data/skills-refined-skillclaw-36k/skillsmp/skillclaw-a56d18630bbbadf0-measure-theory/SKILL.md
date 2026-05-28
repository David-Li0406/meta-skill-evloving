---
name: measure-theory
description: Use this skill when solving problems related to measure theory, including integration and Lebesgue measure.
---

# Measure Theory

## When to Use

Use this skill when working on problems in measure theory, particularly those involving integration theory and Lebesgue measure.

## Decision Tree

1. **Simple Function Integration**
   - For \( s = \sum(a_i \cdot \chi_{E_i}) \): 
   - \( \int s \, d\mu = \sum(a_i \cdot \mu(E_i)) \)
   - Command: 
   ```bash
   uv run python -m runtime.harness scripts/sympy_compute.py integrate "sum(a_i * chi_E_i)" --var mu
   ```

2. **Monotone Convergence Theorem (MCT)**
   - If \( 0 \leq f_n \leq f_{n+1} \) and \( f_n \to f \):
   - \( \lim \int f_n = \int \lim f_n \)
   - Command: 
   ```bash
   uv run python -m runtime.harness scripts/z3_solve.py prove "f_n_increasing implies lim_integral_equals_integral_lim"
   ```

3. **Dominated Convergence Theorem (DCT)**
   - If \( |f_n| \leq g \) (integrable) and \( f_n \to f \) pointwise:
   - \( \lim \int f_n = \int f \)
   - Command: 
   ```bash
   uv run python -m runtime.harness scripts/z3_solve.py prove "abs(f_n) <= g and g_integrable implies limit_exchange"
   ```

4. **Fatou's Lemma**
   - \( \int(\liminf f_n) \leq \liminf(\int f_n) \)
   - Use as a lower bound when MCT/DCT don't apply.
   - Command: 
   ```bash
   uv run python -m runtime.harness scripts/sympy_compute.py limit "liminf(integral_f_n)" --comparison "integral_liminf_f_n"
   ```

5. **Outer Measure Construction**
   - \( m^*(A) = \inf\{\sum |I_n| : A \subseteq \bigcup I_n\} \)
   - Command: 
   ```bash
   uv run python -m runtime.harness scripts/sympy_compute.py sum "length(I_n)" --var n
   ```

6. **Caratheodory Criterion**
   - \( E \) is measurable if: \( m^*(A) = m^*(A \cap E) + m^*(A \cap E^c) \) for all \( A \)
   - Command: 
   ```bash
   uv run python -m runtime.harness scripts/z3_solve.py prove "caratheodory_criterion"
   ```

7. **Lebesgue Measure Properties**
   - Translation invariant: \( m(E + x) = m(E) \)
   - Sigma-additive on measurable sets: \( m([a,b]) = b - a \)

8. **Regularity Theorems**
   - Inner regularity: \( m(E) = \sup\{m(K) : K \text{ compact}, K \subseteq E\} \)
   - Outer regularity: \( m(E) = \inf\{m(U) : U \text{ open}, E \subseteq U\} \)

## Key Techniques

*From indexed textbooks:*

- [Measure, Integration Real Analysis (... (Z-Library)] Lebesgue measure on the Lebesgue measurable sets has advantages over Lebesgue measure on the Borel sets, particularly regarding subsets of measure 0.
- [Measure, Integration Real Analysis (... (Z-Library)] Not every subset of \( \mathbb{R} \) is a Borel set, but every subset of a set with outer measure 0 is Lebesgue measurable.