# Reviewer Blocker Criteria

## Decision Type Framework

Reviewers MUST understand what decisions they can make independently vs. what requires escalation:

| Decision Type       | Action                | Examples                                                                 |
| ------------------- | --------------------- | ------------------------------------------------------------------------ |
| **Can Decide**      | Proceed with review   | Severity classification, pattern violations, quality issues              |
| **MUST Escalate**   | STOP and report       | Unclear scope, ambiguous requirements, conflicting decisions             |
| **CANNOT Override** | HARD BLOCK - must fix | Critical security issues, data integrity violations, compliance failures |

---

## Universal Blocker Criteria

These apply to ALL reviewers:

### Can Decide (Proceed Independently)

| Area                   | What You Can Decide                         |
| ---------------------- | ------------------------------------------- |
| **Severity**           | Classify issues as CRITICAL/HIGH/MEDIUM/LOW |
| **Pattern violations** | Identify and document violations            |
| **Quality assessment** | Evaluate against checklist items            |
| **Recommendations**    | Provide remediation guidance                |

### MUST Escalate (STOP and Report)

| Trigger                    | Action                                     |
| -------------------------- | ------------------------------------------ |
| **Unclear scope**          | STOP - Ask: "Which files should I review?" |
| **Ambiguous requirements** | STOP - Ask: "What are the requirements?"   |
| **Conflicting decisions**  | Use NEEDS_DISCUSSION verdict               |
| **Missing context**        | STOP - Ask for clarification               |

### CANNOT Override (NON-NEGOTIABLE)

| Requirement                             | Enforcement                                |
| --------------------------------------- | ------------------------------------------ |
| **Critical issues = FAIL**              | Automatic FAIL, no exceptions              |
| **3+ High issues = FAIL**               | Automatic FAIL, no exceptions              |
| **All checklist categories verified**   | Cannot skip any section                    |
| **File:line references for all issues** | Every issue must include location          |
| **Independent review**                  | Cannot assume other reviewers catch issues |
| **Output schema compliance**            | Must follow exact format                   |

---

## When to Use Each Verdict

| VERDICT              | Condition        | Requirements                             |
| -------------------- | ---------------- | ---------------------------------------- |
| **PASS**             | No blockers      | 0 Critical, < 3 High, requirements met   |
| **FAIL**             | Blockers found   | 1+ Critical OR 3+ High issues            |
| **NEEDS_DISCUSSION** | Cannot determine | Requirements unclear, need clarification |

---

## Domain-Specific Non-Negotiables

Each reviewer has additional non-negotiable requirements:

### Code Reviewer

- Critical issues (security, data corruption, core functionality) = FAIL
- All checklist categories must be verified
- AI slop detection must be performed

### Business Logic Reviewer

- Mental Execution Analysis section REQUIRED (cannot skip)
- Financial calculations MUST use Decimal types
- State transitions MUST be validated
- All 8 required output sections MUST be included

### Security Reviewer

- SQL injection, auth bypass, hardcoded secrets = CRITICAL, automatic FAIL
- OWASP Top 10 coverage REQUIRED
- Dependency verification REQUIRED (slopsquatting check)
- Compliance violations = FAIL

### Test Reviewer

| Non-Negotiable                      | Why                                            |
| ----------------------------------- | ---------------------------------------------- |
| All 9 checklist categories verified | Incomplete coverage misses test quality issues |
| Test anti-patterns flagged          | Silent failures corrupt test suite integrity   |
| Edge case coverage assessed         | Missing edge cases = missing bugs              |
| Mock appropriateness verified       | Testing mock behavior = false confidence       |

---

## Escalation Protocol

When you encounter a MUST Escalate situation:

1. **Document what you found** - Be specific about the ambiguity
2. **Use NEEDS_DISCUSSION verdict** - Not PASS or FAIL
3. **List specific questions** - What needs clarification
4. **Do NOT proceed** - Wait for clarification before continuing

**Example escalation output:**

```markdown
## VERDICT: NEEDS_DISCUSSION

## Summary

Cannot complete review due to unclear requirements.

## Clarification Needed

1. What files should I review? No planning document found.
2. What are the business requirements? PRD.md not present.

## Next Steps

- Please provide scope and requirements
- Review will resume after clarification
```

