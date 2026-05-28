---
name: graph-number-theory
description: Use this skill when solving problems related to graph number theory, including modular arithmetic, prime numbers, and graph algorithms.
---

# Graph Number Theory

## When to Use

Use this skill when working on problems in graph number theory that involve modular arithmetic, prime numbers, or graph algorithms.

## Decision Tree

1. **Modular Arithmetic**
   - **Extended Euclidean Algorithm**
     - Find gcd(a,b) and x,y with ax + by = gcd(a,b)
     - Modular inverse: a^{-1} mod n when gcd(a,n) = 1
     - Command: `uv run python -m runtime.harness scripts/sympy_compute.py solve "a*x == 1 mod n" --var x`
   - **Chinese Remainder Theorem**
     - System x = a_i (mod m_i) with coprime m_i
     - Unique solution mod prod(m_i)
     - Command: `uv run python -m runtime.harness scripts/z3_solve.py prove "crt_solution_exists"`
   - **Euler's Theorem**
     - a^{phi(n)} = 1 (mod n) when gcd(a,n) = 1
     - Command: `uv run python -m runtime.harness scripts/sympy_compute.py simplify "phi(p**k) == p**(k-1)*(p-1)"`
   - **Quadratic Residues**
     - Legendre symbol: (a/p) = a^{(p-1)/2} mod p
     - Command: `uv run python -m runtime.harness scripts/z3_solve.py prove "legendre_symbol_multiplicative"`
   - **Order and Primitive Roots**
     - ord_n(a) = smallest k with a^k = 1 (mod n)

2. **Prime Numbers**
   - **Primality Testing**
     - Trial division, Miller-Rabin, AKS
     - Command: `uv run python -m runtime.harness scripts/z3_solve.py prove "no_divisor_between_1_and_sqrt_n"`
   - **Factorization**
     - Trial division, Pollard's rho, Quadratic sieve
     - Command: `uv run python -m runtime.harness scripts/sympy_compute.py factor "n"`
   - **Prime Distribution**
     - Prime Number Theorem, Prime gaps
     - Command: `uv run python -m runtime.harness scripts/sympy_compute.py simplify "pi(x) ~ x/ln(x)"`
   - **Fermat's Little Theorem**
     - a^{p-1} = 1 (mod p) for a not divisible by p
     - Command: `uv run python -m runtime.harness scripts/z3_solve.py prove "a**(p-1) == 1 mod p"`
   - **Wilson's Theorem**
     - (p-1)! = -1 (mod p) iff p is prime

3. **Graph Algorithms**
   - **Traversal Selection**
     - BFS for shortest paths, DFS for cycle detection
   - **Shortest Path Algorithms**
     - Dijkstra, Bellman-Ford, Floyd-Warshall
   - **Minimum Spanning Tree**
     - Prim's and Kruskal's algorithms
     - Command: `uv run python -m runtime.harness scripts/z3_solve.py prove "cut_property"`
   - **Network Flow**
     - Max-flow = min-cut (Ford-Fulkerson)
     - Command: `uv run python -m runtime.harness scripts/sympy_compute.py linsolve "flow_conservation"`
   - **Graph Properties**
     - Spectral properties, connectivity, coloring

## Key Techniques

*From indexed textbooks:*

- [Graph Theory (Graduate Texts in Mathematics (173))] Various techniques and theorems related to graph number theory, modular arithmetic, and prime numbers.