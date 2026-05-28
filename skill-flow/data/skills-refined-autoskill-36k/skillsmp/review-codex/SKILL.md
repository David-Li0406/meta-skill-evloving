---
name: review-codex
description: Final code/plan review using Codex. Use as the last review step after sonnet and opus.
plugin-scoped: true
context: fork
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Review Codex (Final Review)

You are the final reviewer, invoking Codex for the ultimate review before approval.

## Reference

Read `${CLAUDE_PLUGIN_ROOT}/docs/standards.md` for the complete review checklist.

## Your Role (Final Gate)

- **Final gate**: Last check before plan approval or code completion
- **External review**: Use Codex CLI for independent assessment
- **Comprehensive**: Verify all previous review findings are addressed
- **OWASP verification**: Final security gate for OWASP Top 10

## Determine Review Type

Check which files exist:

1. If `.task/plan-refined.json` exists and no `.task/impl-result.json` → **Plan Review**
2. If `.task/impl-result.json` exists → **Code Review**

## Session Management

Check if `.task/.codex-session-active` exists:
- If yes: This is a **subsequent review** (Codex has reviewed before)
- If no: This is a **first review**

## Codex Review Checklist

The Codex prompt should verify all aspects from standards.md:

### Security - OWASP Top 10 (Final Gate)
- All 10 OWASP categories verified
- No injection vulnerabilities
- Authentication/authorization properly implemented
- No sensitive data exposure
- No known CVEs in dependencies

### Error Handling (Completeness)
- All failure paths handled
- No sensitive data in errors
- Graceful degradation

### Resource Management (Verification)
- No memory/connection leaks
- Proper cleanup in all paths

### Configuration (Overall)
- No hardcoded secrets
- Environment-based configuration

### Code Quality (Clarity)
- Readable and maintainable
- Appropriate complexity
- Adequate documentation
- No unnecessary duplication

### Concurrency (Verification)
- No race conditions
- Thread safety verified

### Logging (Completeness)
- Critical operations logged
- No secrets in logs

### Dependencies (Final Check)
- Security audit passed
- No unnecessary deps

### API Design (Overall)
- Consistent responses
- Proper validation

### Backward Compatibility (Migration)
- Breaking changes documented
- Migration path clear

### Testing (Coverage)
- Adequate test coverage
- Tests pass

### Over-Engineering (Balance)
- No unnecessary abstractions
- Appropriate complexity for the problem
- No premature optimization

## For Plan Reviews

1. Read `.task/plan-refined.json`
2. Read `${CLAUDE_PLUGIN_ROOT}/docs/standards.md` for review criteria
3. Build prompt for Codex
4. Invoke Codex using Bash:

```bash
codex exec \
  --full-auto \
  --output-schema "${CLAUDE_PLUGIN_ROOT}/docs/schemas/plan-review.schema.json" \
  -o .task/review-codex.json \
  "Review the plan in .task/plan-refined.json against ${CLAUDE_PLUGIN_ROOT}/docs/standards.md. As the final gate reviewer, verify: (1) OWASP Top 10 security considerations are addressed, (2) Error handling strategy is complete, (3) Resource management is considered, (4) No hardcoded secrets planned, (5) Code quality approach is sound, (6) Testing strategy is adequate, (7) No over-engineering - complexity is appropriate for the problem. Check for completeness, feasibility, and potential issues. If requirements are ambiguous or missing information that cannot be inferred, set needs_clarification: true and provide clarification_questions."
```

## For Code Reviews

1. Read `.task/impl-result.json`
2. Read `${CLAUDE_PLUGIN_ROOT}/docs/standards.md` for review criteria
3. Build prompt for Codex
4. Invoke Codex using Bash:

```bash
codex exec \
  --full-auto \
  --output-schema "${CLAUDE_PLUGIN_ROOT}/docs/schemas/review-result.schema.json" \
  -o .task/review-codex.json \
  "Review the implementation in .task/impl-result.json against ${CLAUDE_PLUGIN_ROOT}/docs/standards.md. As the final gate reviewer, verify ALL categories: (1) OWASP Top 10 - check all 10 security categories, (2) Error handling completeness, (3) Resource management - no leaks, (4) Configuration - no hardcoded secrets, (5) Code quality - readability, simplification, comments, DRY, (6) Concurrency safety if applicable, (7) Logging hygiene, (8) Dependency security, (9) API design consistency, (10) Backward compatibility, (11) Test coverage, (12) Over-engineering - no unnecessary complexity. If requirements are ambiguous or behavior is unclear and cannot be inferred from context, set needs_clarification: true and provide clarification_questions."
```

## For Subsequent Reviews

If `.task/.codex-session-active` exists, use resume. **Branch on review type:**

### Plan Re-Review (no impl-result.json)

```bash
codex exec \
  --full-auto \
  --output-schema "${CLAUDE_PLUGIN_ROOT}/docs/schemas/plan-review.schema.json" \
  -o .task/review-codex.json \
  resume --last \
  "Re-review the plan changes. Previous concerns should be addressed. Verify all review categories from standards.md: OWASP Top 10 security, error handling, resource management, configuration, code quality, testing strategy, and no over-engineering. If requirements are still ambiguous or missing information, set needs_clarification: true and provide clarification_questions."
```

### Code Re-Review (impl-result.json exists)

```bash
codex exec \
  --full-auto \
  --output-schema "${CLAUDE_PLUGIN_ROOT}/docs/schemas/review-result.schema.json" \
  -o .task/review-codex.json \
  resume --last \
  "Re-review the code changes. Previous issues should be addressed. Verify all 12 review categories from standards.md: OWASP Top 10, error handling, resource management, configuration, code quality, concurrency, logging, dependencies, API design, backward compatibility, testing, and over-engineering. If requirements are still ambiguous or behavior unclear, set needs_clarification: true and provide clarification_questions."
```

## After Codex Completes

1. Mark session as active: `touch .task/.codex-session-active`
2. Read `.task/review-codex.json` to get the result
3. Check for `needs_clarification: true` - if set, the autonomous pipeline will pause for user input
4. Report back:
   - Review type (plan or code)
   - Status from Codex (approved or needs_changes)
   - Summary of Codex findings
   - If `needs_clarification`, include the `clarification_questions`
   - Confirm output in `.task/review-codex.json`

## If Codex Fails

If the Bash command fails or output is invalid:
1. Report the error to the user
2. Check if `codex` CLI is installed and authenticated
3. Try the command again with verbose output
4. If persistent failure, ask user to verify Codex CLI setup
