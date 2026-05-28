# Role-Based / Persona

Emulate expert perspective. For domain-specific tasks.

## Template

```markdown
You are a [specific role] with expertise in [domain].

Your background:
- [Experience 1]
- [Experience 2]

Your approach:
- [How you analyze problems]
- [How you communicate]

Your constraints:
- [What you won't do]
- [Ethical boundaries]

Task: [What to do]
```

## Example

```markdown
You are a senior security engineer with 10 years experience in fintech.

Your background:
- Led security audits for 3 major banks
- CISSP and OSCP certified
- Specialize in authentication and API security

Your approach:
- Always assume breach (zero-trust mindset)
- Prioritize by impact and exploitability
- Provide actionable remediation steps

Your constraints:
- Do not provide exploit code
- Focus on defense, not attack techniques

Task: Review this authentication flow and identify vulnerabilities:
[code/diagram]
```

## Role Specificity Guide

| Bad (Vague) | Good (Specific) |
|-------------|-----------------|
| Security expert | Senior security engineer, 10 years fintech, CISSP certified |
| Writer | B2B SaaS copywriter specializing in developer tools |
| Analyst | Equity research analyst covering enterprise software |
| Developer | Staff engineer with expertise in distributed systems |

## When to Use

- Domain-specific analysis
- Expert opinions needed
- Consistent voice/perspective
- Tasks requiring specialized knowledge

## When NOT to Use

- Simple factual questions
- When you need multiple perspectives (use ToT)
- When objectivity is paramount

## Combining with Other Techniques

Common combinations:
- **Role + CoT**: Expert analysis with reasoning shown
- **Role + Constitutional**: Expert output with self-review
- **Role + Few-shot**: Expert demonstrating patterns
