---
name: graph-number-theory
description: Use this skill when solving problems related to graph number theory, including modular arithmetic, prime numbers, and graph algorithms.
---

# Graph Number Theory

## When to Use

Use this skill when working on problems in graph number theory, encompassing modular arithmetic, prime numbers, and graph algorithms.

## Decision Tree

### Modular Arithmetic
1. **Extended Euclidean Algorithm**
   - Find gcd(a,b) and x,y with ax + by = gcd(a,b)
   - Modular inverse: a^{-1} mod n when gcd(a,n) = 1

2. **Chinese Remainder Theorem**
   - System x = a_i (mod m_i) with coprime m_i
   - Unique solution mod prod(m_i)

3. **Euler's Theorem**
   - a^{phi(n)} = 1 (mod n) when gcd(a,n) = 1

4. **Quadratic Residues**
   - Legendre symbol: (a/p) = a^{(p-1)/2} mod p

5. **Order and Primitive Roots**
   - ord_n(a) = smallest k with a^k = 1 (mod n)

### Prime Numbers
1. **Primality Testing Hierarchy**
   - Trial division, Miller-Rabin, AKS

2. **Factorization**
   - Trial division, Pollard's rho, Quadratic sieve

3. **Prime Distribution**
   - Prime Number Theorem and prime gaps

4. **Fermat's Little Theorem**
   - a^{p-1} = 1 (mod p) for a not divisible by p

5. **Wilson's Theorem**
   - (p-1)! = -1 (mod p) iff p is prime

### Graph Algorithms
1. **Traversal Selection**
   - BFS for shortest paths, DFS for cycle detection

2. **Shortest Path Algorithms**
   - Dijkstra, Bellman-Ford, Floyd-Warshall

3. **Minimum Spanning Tree**
   - Prim's and Kruskal's algorithms

4. **Network Flow**
   - Max-flow = min-cut (Ford-Fulkerson)

5. **Graph Properties**
   - Spectral properties, connectivity, and coloring

## Tool Commands

### Modular Arithmetic Tools
```bash
uv run python -m runtime.harness scripts/sympy_compute.py solve "a*x == 1 mod n" --var x
uv run python -m runtime.harness scripts/z3_solve.py prove "crt_solution_exists"
uv run python -m runtime.harness scripts/sympy_compute.py simplify "phi(p**k) == p**(k-1)*(p-1)"
uv run python -m runtime.harness scripts/z3_solve.py prove "legendre_symbol_multiplicative"
```

### Prime Numbers Tools
```bash
uv run python -m runtime.harness scripts/sympy_compute.py factor "n"
uv run python -m runtime.harness scripts/z3_solve.py prove "no_divisor_between_1_and_sqrt_n"
uv run python -m runtime.harness scripts/sympy_compute.py simplify "pi(x) ~ x/ln(x)"
uv run python -m runtime.harness scripts/z3_solve.py prove "a**(p-1) == 1 mod p"
```

### Graph Algorithms Tools
```bash
uv run python -m runtime.harness scripts/sympy_compute.py eigenvalues "adjacency_matrix"
uv run python -m runtime.harness scripts/z3_solve.py prove "d[v] >= d[u] + w(u,v) for all edges"
uv run python -m runtime.harness scripts/z3_solve.py prove "min_edge_crossing_cut_in_mst"
uv run python -m runtime.harness scripts/sympy_compute.py linsolve "flow_conservation_equations"
```

## Key Techniques

*From indexed textbooks:*

- [Graph Theory (Graduate Texts in Mathematics (173))] Various techniques and theorems related to graph properties, primality, and modular arithmetic.

## Cognitive Tools Reference

See `.claude/skills/math-mode/SKILL.md` for full tool documentation.