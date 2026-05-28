# Reviewer Model Requirement

## Model Requirement

**HARD GATE:** All reviewer agents REQUIRE Claude Sonnet 4.5, Claude Opus 4.5, Gemini 3.0 Pro or higher.

### Self-Verification (MANDATORY - Check FIRST)

If you are NOT Claude Sonnet 4.5, Claude Opus 4.5, Gemini 3.0 Pro or higher → **STOP immediately and report:**

```
ERROR: Model requirement not met
Required: Claude Sonnet 4.5, Claude Opus 4.5, Gemini 3.0 Pro or higher
Current: [your model]
Action: Cannot proceed. Orchestrator must reinvoke with model="sonnet" or "opus"
```

### Why Opus is Required for Reviewers

| Review Capability               | Why It Requires Opus                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------- |
| **Complex code tracing**        | Tracing data flows across components, following function calls, understanding state changes |
| **Pattern recognition**         | Identifying subtle design patterns, anti-patterns, and inconsistencies                      |
| **Mental execution**            | Walking through code with concrete scenarios to verify correctness                          |
| **Context integration**         | Understanding full file context, adjacent functions, ripple effects                         |
| **Security analysis**           | Identifying attack vectors, OWASP vulnerabilities, cryptographic weaknesses                 |
| **Business logic verification** | Tracing business rules, edge cases, state machine transitions                               |

**Domain-Specific Rationale:**

- **Code Reviewer:** Requires tracing algorithmic flow, context propagation, and codebase consistency patterns
- **Business Logic Reviewer:** Requires mental execution analysis with concrete scenarios and full file context
- **Security Reviewer:** Requires deep vulnerability detection, OWASP Top 10 coverage, and cryptographic evaluation
- **Test Reviewer:** Requires analyzing test quality, coverage gaps, and test anti-patterns

---

## Enforcement

This is a **HARD GATE** - no reviewer can proceed without Opus model verification.

If invoked with wrong model, the agent MUST:

1. NOT perform any review
2. Output the error message above
3. Return immediately

