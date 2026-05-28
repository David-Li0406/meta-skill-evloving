---
id: code-review-cycle
name: "Code Review Cycle"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Code Review Cycle

## Overview

The Code Review Cycle in SDD ensures quality, knowledge sharing, and continuous improvement through structured review processes. It integrates with the task lifecycle, quality gates, and reflexion learning to create a feedback loop that improves both code and process.

## When to Use

- Reviewing code changes before merging
- Validating task completion against acceptance criteria
- Ensuring consistency with design documents
- Identifying patterns and anti-patterns
- Knowledge transfer between team members

## Process/Steps

### 1. Review Cycle Overview

```
Task Completion → Self-Review → PR Creation → Automated Checks
                                                    │
       ┌────────────────────────────────────────────┘
       │
       ▼
Peer Review → Feedback → Iterations → Approval → Merge
       │                                           │
       └──────── Reflexion Learning ───────────────┘
```

**Review Types:**
| Type | Reviewer | Focus | Timing |
|------|----------|-------|--------|
| Self-Review | Author | Completeness, obvious issues | Before PR |
| Automated | CI/CD | Tests, lint, security | On PR creation |
| Peer Review | Team member | Logic, design, patterns | After automated |
| Architectural | Senior/Lead | System design, consistency | Complex changes |
| Security | Security team | Vulnerabilities | Sensitive code |

### 2. Self-Review Checklist

**Before Creating PR:**
```yaml
self_review_checklist:
  code_quality:
    - "Code follows project style guide"
    - "No commented-out code"
    - "No debug statements (console.log, print)"
    - "Error handling is appropriate"
    - "No hardcoded values (use constants/config)"

  functionality:
    - "All acceptance criteria are met"
    - "Edge cases are handled"
    - "Changes work locally"
    - "No regression in existing functionality"

  testing:
    - "Unit tests cover new code"
    - "Tests are meaningful, not just coverage"
    - "All tests pass locally"
    - "Integration tests updated if needed"

  documentation:
    - "Code is self-documenting with clear names"
    - "Complex logic has comments"
    - "API docs updated if needed"
    - "README updated if setup changed"

  sdd_compliance:
    - "Implementation matches design document"
    - "Deviations are documented and justified"
    - "Traceability links are correct"
```

### 3. PR Creation Standards

**PR Template:**
```markdown
## Summary
<!-- Brief description of changes -->

## SDD References
| Document | Section |
|----------|---------|
| Spec | [SPEC-XXX](link) |
| Design | [DESIGN-XXX](link) |
| Task | [TASK-XXX](link) |

## Changes
- [x] Feature/fix description
- [x] Another change

## Acceptance Criteria Verification
| AC | Status | Notes |
|----|--------|-------|
| AC-1: Given X, When Y, Then Z | Verified | Screenshot/test |
| AC-2: ... | Verified | |

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases tested

## Screenshots (if UI changes)
<!-- Before/After screenshots -->

## Checklist
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] No lint/type errors
- [ ] Documentation updated
- [ ] No secrets committed

## Notes for Reviewer
<!-- Any context that helps review -->
```

### 4. Review Process

**Review Focus Areas:**
```yaml
review_dimensions:
  correctness:
    questions:
      - "Does it solve the stated problem?"
      - "Does it handle edge cases?"
      - "Could it cause data corruption?"
      - "Are there race conditions?"

  design:
    questions:
      - "Does it follow architectural patterns?"
      - "Is it consistent with existing code?"
      - "Is it extensible for future needs?"
      - "Is there unnecessary complexity?"

  readability:
    questions:
      - "Can I understand without author explanation?"
      - "Are names clear and consistent?"
      - "Is the code well-organized?"
      - "Are comments helpful, not redundant?"

  performance:
    questions:
      - "Are there N+1 queries?"
      - "Is caching used appropriately?"
      - "Are there memory leaks?"
      - "Is it efficient at scale?"

  security:
    questions:
      - "Is input validated?"
      - "Are there injection risks?"
      - "Is authentication/authorization correct?"
      - "Are secrets handled properly?"

  testing:
    questions:
      - "Are tests meaningful?"
      - "Do tests cover edge cases?"
      - "Are mocks used appropriately?"
      - "Would tests catch regressions?"
```

### 5. Feedback Guidelines

**Comment Types:**
```yaml
comment_prefixes:
  required:
    prefix: "[Required]"
    meaning: "Must be addressed before merge"
    example: "[Required] This SQL query is vulnerable to injection"

  suggestion:
    prefix: "[Suggestion]"
    meaning: "Consider this improvement"
    example: "[Suggestion] Could use early return here"

  question:
    prefix: "[Question]"
    meaning: "Need clarification"
    example: "[Question] Why is this timeout set to 60s?"

  nitpick:
    prefix: "[Nitpick]"
    meaning: "Minor style preference, optional"
    example: "[Nitpick] Could rename this to be more descriptive"

  praise:
    prefix: "[Nice]"
    meaning: "Good pattern worth highlighting"
    example: "[Nice] Clean separation of concerns here"

  learning:
    prefix: "[FYI]"
    meaning: "Educational, no action needed"
    example: "[FYI] There's a utility for this in utils/string.ts"
```

**Constructive Feedback Patterns:**
```markdown
## Good Feedback Examples

### Instead of:
"This is wrong"

### Write:
"[Required] This could cause a null pointer exception when `user` is undefined.
Consider adding a null check:
```typescript
if (user) {
  processUser(user);
}
```
"

### Instead of:
"Why did you do it this way?"

### Write:
"[Question] I see you chose to use a Map here instead of an object.
Was this for a specific reason like preserving insertion order?
Just trying to understand the decision for future reference."
```

### 6. Review Response Protocol

**Author Response Guidelines:**
```yaml
author_responses:
  required_feedback:
    - "Address all [Required] comments"
    - "Explain why if you disagree"
    - "Mark as resolved when fixed"

  suggestions:
    - "Implement if it improves code"
    - "Explain reasoning if declining"
    - "Don't just ignore"

  questions:
    - "Answer clearly and completely"
    - "Update code if answer reveals confusion"
    - "Consider if docs need updating"

  resolution:
    - "Push fixes in new commits (for traceability)"
    - "Reply to each comment"
    - "Request re-review when ready"
```

### 7. Approval Criteria

**Merge Requirements:**
```yaml
merge_criteria:
  automated:
    - all_tests_pass: true
    - lint_clean: true
    - type_check_pass: true
    - coverage_threshold_met: true
    - security_scan_pass: true

  human_review:
    - required_approvals: 1  # or 2 for critical paths
    - no_unresolved_required_comments: true
    - all_discussions_resolved: true

  special_cases:
    critical_path:
      - additional_approval_from: "tech lead"
    security_sensitive:
      - additional_approval_from: "security team"
    database_changes:
      - additional_approval_from: "DBA or senior"
```

### 8. Post-Merge Actions

**After Merge Protocol:**
```yaml
post_merge:
  immediate:
    - verify_ci_cd_success: true
    - check_deployment_health: true
    - update_task_status: "done"

  documentation:
    - update_changelog: if_user_facing
    - update_api_docs: if_api_changed
    - note_lessons_learned: if_applicable

  reflexion:
    - identify_patterns: "What worked well?"
    - identify_improvements: "What could be better?"
    - update_memory: "patterns_learned.jsonl"
```

## Best Practices

### For Authors
1. **Small PRs** - Easier to review, faster feedback
2. **Self-review first** - Catch obvious issues
3. **Good descriptions** - Help reviewers understand context
4. **Respond promptly** - Keep momentum

### For Reviewers
1. **Timely reviews** - Within 24 hours
2. **Be constructive** - Focus on code, not person
3. **Explain why** - Help author learn
4. **Acknowledge good work** - Positive reinforcement

### Process
1. **Consistent standards** - Everyone follows same rules
2. **Automate what you can** - Let CI catch style issues
3. **Track metrics** - Review time, iteration count
4. **Retrospect** - Improve the process itself

## Templates/Examples

### Review Checklist (Reviewer Copy)

```markdown
## Code Review Checklist

### PR: [Title]
### Reviewer: @name
### Date: YYYY-MM-DD

### Correctness
- [ ] Solves the stated problem
- [ ] Handles edge cases
- [ ] No obvious bugs
- [ ] Error handling appropriate

### Design
- [ ] Follows project patterns
- [ ] Appropriate abstraction level
- [ ] No unnecessary complexity
- [ ] Consistent with architecture

### Code Quality
- [ ] Clear naming
- [ ] Well-organized
- [ ] No code smells
- [ ] DRY (Don't Repeat Yourself)

### Testing
- [ ] Adequate test coverage
- [ ] Tests are meaningful
- [ ] Edge cases tested

### Security
- [ ] Input validation
- [ ] No hardcoded secrets
- [ ] Auth/authz correct

### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic commented
- [ ] API docs updated

### SDD Compliance
- [ ] Matches design document
- [ ] Deviations justified
- [ ] Acceptance criteria met

### Verdict
- [ ] Approved
- [ ] Approved with suggestions
- [ ] Request changes

### Summary
[Overall assessment and key points]
```

### Review Metrics Dashboard

```yaml
review_metrics:
  efficiency:
    - time_to_first_review: "< 4 hours"
    - time_to_merge: "< 24 hours"
    - review_iterations: "< 3"

  quality:
    - bugs_found_in_review: "track"
    - bugs_escaped_to_prod: "minimize"
    - rework_rate: "< 10%"

  engagement:
    - review_participation: "all team members"
    - feedback_ratio: "constructive vs blocking"
    - knowledge_sharing: "FYI comments"
```

## References

- [Google Code Review Guidelines](https://google.github.io/eng-practices/review/)
- [Microsoft Code Review Best Practices](https://docs.microsoft.com/en-us/devops/develop/git/git-code-review)
- [Conventional Comments](https://conventionalcomments.org/)
- [quality-gates-confidence: Quality Gates Confidence](./quality-gates-confidence_quality_gates_confidence.md)
- [reflexion-learning: Reflexion Learning](./reflexion-learning_reflexion_learning.md)
