# When Review is Not Needed

## Minimal Review Conditions

Review can be MINIMAL (not skipped) when ALL these conditions are met:

| Condition                      | Verification Required                                 |
| ------------------------------ | ----------------------------------------------------- |
| **Documentation-only changes** | Verify .md files only, no code changes                |
| **Pure formatting/whitespace** | Verify no logic modifications via git diff            |
| **Generated/lock files only**  | Verify package-lock.json, go.sum, etc.                |
| **Reverts previous commit**    | Reference original review that approved reverted code |

**IMPORTANT:** "Minimal" means reduced scope, NOT skipped review.

---

## Still Required in Minimal Mode

Even in minimal mode, these checks are MANDATORY:

| File Type                    | Required Check                                |
| ---------------------------- | --------------------------------------------- |
| **Generated config files**   | Verify correctness, no security issues        |
| **Lock file changes**        | Verify no security vulnerabilities introduced |
| **Dependency version bumps** | Check for CVEs in new versions                |
| **Revert commits**           | Confirm revert is intentional, not accidental |
| **Database migrations**      | ALWAYS full review (data integrity risk)      |
| **Auth/authz code**          | ALWAYS full review (security risk)            |
| **State machine changes**    | ALWAYS full review (business logic risk)      |

---

## Domain-Specific "Not Needed" Criteria

### Code Reviewer

- Documentation-only changes (no code)
- Formatting/whitespace only (no logic)
- Generated files only (package-lock, etc.)

### Business Logic Reviewer

- Documentation/comments only (no executable code)
- Pure formatting (whitespace changes)
- Configuration values only (no business rule changes)

**STILL REQUIRED:** Configuration changes affecting business rules, database migrations, workflow changes

### Security Reviewer

- Documentation-only (no executable content)
- Pure formatting (no logic changes)
- Previous security review covers same scope in same PR

**STILL REQUIRED:** Dependency changes (even version bumps), configuration changes (secrets exposure risk), auth/authz logic

### Test Reviewer

- Changes to non-test code only (test files unchanged)
- Test configuration only (no test logic)

**STILL REQUIRED:** Any changes to test files, new functionality without tests

---

## Decision Framework

```
Is it documentation/comments only?
├── YES → Minimal review (verify no executable content)
└── NO → Continue

Is it formatting/whitespace only?
├── YES → Minimal review (verify via git diff)
└── NO → Continue

Is it generated/lock files only?
├── YES → Minimal review (check for vulnerabilities)
└── NO → Continue

Is it in critical category (auth, DB, state machine)?
├── YES → FULL REVIEW REQUIRED
└── NO → Continue

Does it touch code in my domain?
├── YES → FULL REVIEW REQUIRED
└── NO → Minimal review
```

---

## When in Doubt

**ALWAYS conduct full review.**

- Missed issues compound over time
- Business logic errors are expensive
- Security vulnerabilities are catastrophic
- The cost of full review < cost of missed bug

---

## Anti-Rationalization

Do NOT skip review because:

| Rationalization              | Why It's Wrong                                |
| ---------------------------- | --------------------------------------------- |
| "It's just a config change"  | Config can affect behavior, expose secrets    |
| "Tests don't need review"    | Tests can be wrong, test mock behavior        |
| "It's a minor version bump"  | Minor versions can introduce breaking changes |
| "Previous PR reviewed this"  | Each PR is independent, code may have changed |
| "It's already in production" | Production duration ≠ correctness             |

**Default:** Full review. Minimal review is the exception, not the rule.

