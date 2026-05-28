---
name: neuro-symbolic-reasoning
description: Use this skill when implementing neuro-symbolic AI that combines LLMs with symbolic solvers for tasks like NL-to-logic translation, logical reasoning, and self-refinement loops.
---

# Neuro-Symbolic Reasoning

## Pipeline

```
NL Problem → LLM Formulator → Logic Program → Symbolic Solver → Answer
                    ↑                              |
                    └──── Self-Refinement ←────────┘
```

## Solver Selection

| Logic Type          | Solver   | Output                  |
|---------------------|----------|-------------------------|
| First-order logic   | Prover9  | True/False/Unknown      |
| Constraints/SAT     | Z3       | sat/unsat/unknown       |
| Rule-based          | Pyke     | Bindings/No proof       |

## Logic Program Format

Programs use `:::` annotations to explain each line.

## Self-Refinement

When a solver returns an error, retry with the original program and the error message. Max 3 rounds, then fall back to LLM chain-of-thought or random guess.

## Quality Checks

1. Solver parses program without syntax errors.
2. Predicates/functions declared before use.
3. Answer mapping handles all outcomes.
4. Refinement loop has max iterations.

## References

- Prover9, Z3, Pyke integration
- Installation and API usage
- Logic-LM paper patterns
- Technical specialist workflow