# Advisory Panel Guidelines

The Advisory Panel provides three perspectives on high-stakes decisions: Pragmatist, Purist, and Skeptic.

## When to Invoke

**Invoke when:**
- High-stakes decisions (security, data integrity, financial)
- Multiple valid approaches with significant tradeoffs
- Team uncertainty about direction
- Low reversibility (hard to change later)

**Skip when:**
- Clear precedent exists in codebase
- Low-risk, easily reversible changes
- Time-critical fixes with obvious solutions

## The Three Perspectives

- **Pragmatist**: Fastest path to working software—minimal change, reuse patterns, accept reasonable debt
- **Purist**: Right way long-term—design principles, maintainability, prevent future debt
- **Skeptic**: What could go wrong—failure modes, security risks, operational concerns

## Synthesis Guidelines

| Favor | When |
|-------|------|
| Pragmatist | Time pressure justified, low risk, MVP/prototype |
| Purist | Core components, public API, security-critical |
| Hybrid | Ship pragmatist + schedule purist refactor |

For detailed output format and guidelines, see `agents/advisory-panel.md`.
