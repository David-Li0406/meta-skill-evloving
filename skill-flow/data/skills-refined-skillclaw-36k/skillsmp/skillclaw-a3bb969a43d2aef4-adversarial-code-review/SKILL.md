---
name: adversarial-code-review
description: Use this skill when you need to review code from hostile perspectives to uncover bugs, security issues, and unintended consequences that the author may have overlooked.
---

# Adversarial Code Review

**Core Principle:** Review as if you're trying to break the code. Deliberately adopt hostile perspectives—each reveals issues the others miss. This is not about finding fault; it's about identifying problems before users do.

## Review Mode

| Mode                       | Trigger                                | Focus                              |
| -------------------------- | -------------------------------------- | ---------------------------------- |
| **Diff-Focused** (default) | No explicit instruction, PR review     | What changed? What could break?    |
| **Audit**                  | "audit", "holistic", "codebase review" | Broader scope, systematic coverage |

When in doubt, use diff-focused mode. Audit mode requires explicit request.

## The Six Adversarial Lenses

Review through each lens deliberately. Don't blend them—switching perspectives forces deeper analysis.

| Lens                    | Core Question                         | Reveals                                                        |
| ----------------------- | ------------------------------------- | -------------------------------------------------------------- |
| **Malicious User**      | "How would I exploit this?"           | Input validation gaps, injection vectors, privilege escalation |
| **Careless Colleague**  | "How would this break if used wrong?" | API misuse, unclear contracts, error handling gaps             |
| **Future Maintainer**   | "What will confuse me in 6 months?"   | Implicit assumptions, missing context, temporal coupling       |
| **Ops/On-Call**         | "How will this fail at 3am?"          | Observability gaps, recovery paths, failure modes              |
| **Data Integrity**      | "What happens to state?"              | Race conditions, partial failures, consistency violations      |
| **Interaction Effects** | "What does this change elsewhere?"    | Unintended side effects, behavioral changes, contract breaks   |

### Lens Details

#### Malicious User

Assume the user is actively trying to break or exploit the system.

- What inputs are trusted that shouldn't be?
- Can I escalate privileges or access unauthorized data?
- What happens if I send malformed/oversized/unexpected input?
- ...