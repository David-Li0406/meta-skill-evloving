---
name: skill-orchestrator
description: "Orchestrate the full implementation workflow: implement -> architecture review -> code review. Use when you need a complete implementation with reviews. Triggers on: full implementation, implement with review, implement and review, complete workflow."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Skill Orchestrator

You orchestrate the complete implementation workflow by invoking skills in sequence and presenting a unified report.

## Workflow

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  1. IMPLEMENT       │────▶│  2. ARCH REVIEW     │────▶│  3. CODE REVIEW     │
│  azure-durable-     │     │  arch-reviewer      │     │  code-reviewer      │
│  implementer        │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌─────────────────────┐
                                                        │  4. UNIFIED REPORT  │
                                                        │  Present all issues │
                                                        │  Wait for decision  │
                                                        └─────────────────────┘
```

## Execution Steps

### Phase 1: Implementation

1. Read `opus45design.md` to understand the architecture
2. Apply the `azure-durable-implementer` skill knowledge
3. Implement the requested feature/component following:
   - Event Ingress → Entities → Orchestrator → Activities pattern
   - .NET 10 / C# 13 best practices
   - Isolated worker model
   - All required patterns from the design doc

4. **Output**: Working implementation with all necessary files

### Phase 2: Architecture Review

1. Apply the `arch-reviewer` skill knowledge
2. Review the implemented code against:
   - opus45design.md architecture
   - Modular Monolith principles
   - Layer separation
   - Scalability considerations
   - Integration patterns

3. **Output**: List of architectural findings with severity

### Phase 3: Code Review

1. Apply the `code-reviewer` skill knowledge
2. Review the implemented code for:
   - C# 13 / .NET 10 best practices
   - Azure Durable-specific rules (determinism, idempotency)
   - Security vulnerabilities
   - Test coverage gaps

3. **Output**: List of code quality/security findings with severity

### Phase 4: Unified Report

Present a combined report of all findings:

```markdown
# Implementation & Review Report

## Implementation Summary
- **Feature**: [What was implemented]
- **Files Created/Modified**:
  - `path/to/file1.cs`
  - `path/to/file2.cs`

## Review Results

### Architecture Review
| Severity | Count |
|----------|-------|
| Critical | X     |
| High     | X     |
| Medium   | X     |
| Low      | X     |

#### Findings
1. **[CRITICAL]** Finding description
   - Location: `file.cs:line`
   - Recommendation: ...

2. **[HIGH]** Finding description
   ...

### Code Review
| Severity | Count |
|----------|-------|
| Critical | X     |
| High     | X     |
| Medium   | X     |
| Low      | X     |

#### Findings
1. **[CRITICAL]** Finding description
   - Location: `file.cs:line`
   - Recommendation: ...

2. **[HIGH]** Finding description
   ...

### Security Findings
1. **[CRITICAL]** Security issue
   ...

## Action Required

**Total Issues**: X Critical, X High, X Medium, X Low

### Critical Issues (Must Fix)
1. Issue 1 - [File:Line]
2. Issue 2 - [File:Line]

### High Priority (Should Fix)
1. Issue 1 - [File:Line]
2. Issue 2 - [File:Line]

### Recommended Improvements
1. Improvement 1
2. Improvement 2

---

**Please review the findings above and let me know which issues you'd like me to fix.**
```

## Important Rules

1. **DO NOT automatically fix issues** - Present findings and wait for user decision
2. **Be thorough** - Don't skip any review category
3. **Be specific** - Include file paths and line numbers
4. **Prioritize** - Critical issues first, then High, Medium, Low
5. **Explain impact** - Why each issue matters

## User Decisions

After presenting the report, the user may:

1. **"Fix all critical issues"** - Fix only critical severity
2. **"Fix all high and critical"** - Fix high + critical
3. **"Fix issue #X"** - Fix specific issue by number
4. **"Fix all"** - Fix everything
5. **"Proceed without fixes"** - Accept current implementation
6. **"Explain issue #X"** - Provide more detail on specific issue

## Re-Review After Fixes

If fixes are applied:
1. Re-run the affected review phase(s)
2. Present updated report showing:
   - Issues fixed
   - Any new issues introduced
   - Remaining issues

## Example Invocation

User: "Implement the Event Ingress Function with full review"

Response:
1. Implement Event Ingress Function following opus45design.md
2. Run architecture review
3. Run code review
4. Present unified report
5. Wait for user decision on fixes
