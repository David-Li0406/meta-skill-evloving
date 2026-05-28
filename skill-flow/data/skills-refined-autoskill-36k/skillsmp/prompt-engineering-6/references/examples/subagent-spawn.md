# Example: Subagent Spawn

Complete example of spawning a focused subagent.

## Scenario

Spawn security reviewer for auth module before audit.

## Final Spawn Prompt

```xml
Spawn subagent as security-reviewer to analyze authentication module

<context>
SOC2 audit next month. Need to identify vulnerabilities in auth
module before external penetration testing. Priority: Find issues
we can fix before auditors arrive.
</context>

<instructions>
Use this workflow:

Thought: [What to check next]
Action: read_file[path] or grep[pattern]
Observation: [What you found]

Repeat until thorough, then compile findings.

Focus areas (in order):
1. Hardcoded credentials or secrets
2. SQL injection vulnerabilities
3. Authentication bypass possibilities
4. Session management issues
5. Input validation gaps
</instructions>

<constraints>
- Do not modify any code
- Focus only on security (not style/performance)
- Maximum 20 findings (prioritize by severity)
- Only analyze files in /src/auth/
</constraints>

<output_format>
## Security Analysis: Auth Module

**Scan Date**: [date]
**Files Analyzed**: [count]

### Critical (Fix Immediately)
| Finding | File:Line | Description | Remediation |

### High (Fix Before Audit)
| Finding | File:Line | Description | Remediation |

### Medium (Fix When Possible)
| Finding | File:Line | Description | Remediation |

### Summary
- Critical: X, High: Y, Medium: Z
- Estimated remediation: [hours]
</output_format>

<success_criteria>
- All .py and .js files in /src/auth/ reviewed
- Each finding has specific file:line reference
- Severity per OWASP guidelines
- Actionable remediation suggestions
</success_criteria>
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Technique | ReAct | Needs file reading, systematic search |
| Framework | Custom (context-heavy) | Security needs clear constraints |
| Output | Structured tables | Easy to track remediation |
| Scope limit | /src/auth/ only | Focused, achievable in one session |
