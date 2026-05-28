# Limitations & When Not to Use

Be honest with yourself about whether this workflow fits your situation.

## When This Works Well

- New features with clear requirements
- CRUD operations, API endpoints, utilities
- Bug fixes where you can describe "it should do X"
- Greenfield projects or well-documented codebases
- Teams comfortable with spec-writing

## When to Use Traditional Coding Instead

| Situation | Why |
|-----------|-----|
| **Security-critical code** | Auth systems, payment processing, encryption. Human review isn't enough—you need human implementation with deep understanding. |
| **Performance-critical code** | AI generates "correct" but often suboptimal code. Profile-driven optimization requires human intuition. |
| **Novel algorithms** | AI can only recombine patterns it's seen. Truly new algorithms need human creativity. |
| **Legacy code without tests** | Claude needs guardrails. If you can't verify the output, don't use AI to change it. |
| **Learning fundamentals** | Junior developers need to write code to learn. Use AI as a tutor, not a replacement. |
| **Exploratory/research work** | When you don't know what you want, you can't write a spec for it. |
| **Regulated industries** | See [Enterprise Guide](ENTERPRISE.md) before proceeding. Additional controls required. |

## Known Technical Limitations

### LLM Limitations
- **Hallucinations**: Claude may reference APIs, libraries, or patterns that don't exist. Always verify.
- **Context window**: Large codebases exceed what Claude can see. Break work into smaller pieces.
- **Training cutoff**: Knowledge has a cutoff date. New frameworks/APIs may be unknown or outdated.
- **Non-deterministic**: Same prompt can produce different outputs. Don't expect reproducibility.

### Workflow Limitations
- **Tests aren't specifications**: Passing tests ≠ correct code. Tests are samples, not proofs.
- **Review fatigue**: If you rubber-stamp approvals, you'll ship bugs. Stay engaged.
- **Flaky tests**: Claude will waste cycles "fixing" tests that fail due to timing, not logic.

## Cost Awareness

Claude API calls cost money. The "iterate until tests pass" loop can run 5-10+ cycles.

**Rough estimates** (verify current pricing):
- Simple feature: $0.50-2.00
- Complex feature with many iterations: $5-15
- Heavy daily usage: $50-200/developer/month

Set token budgets in Anthropic Console to avoid surprises.

## Skill Degradation Risk

If you only review code and never write it:
- Debugging skills atrophy
- You lose intuition for performance tradeoffs
- You become dependent on AI availability

**Mitigation**: Regularly write code without AI. Use AI for acceleration, not replacement.

## Vendor Dependency

This workflow depends on:
- Anthropic's API availability
- Claude Code CLI stability
- MCP server maintenance

**Mitigation**: Don't use AI for code you couldn't write yourself. Keep human skills sharp.

## What This Framework Doesn't Cover

- Mobile development (iOS/Android)
- Data pipelines / ML workflows
- Microservices architecture patterns
- Internationalization (i18n)
- Accessibility (a11y) compliance
- CI/CD integration (see Enterprise Guide)
- Multi-language monorepos

These aren't failures—they're out of scope. The framework is intentionally focused.
