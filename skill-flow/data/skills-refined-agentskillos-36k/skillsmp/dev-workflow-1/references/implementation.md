# Implementation Phase

> **Prerequisite:** Design phase complete. Tests are written and failing.

## Prerequisites Checklist

Before writing implementation code, confirm:

- [ ] I have completed `design.md` (or `bugfix.md` for bug fixes)
- [ ] I have written tests that define the expected behavior
- [ ] My tests fail for the expected reason (not due to syntax errors)

**If any answer is NO → Go back to `design.md` or `bugfix.md`.**

## Code Standards

- Type annotations on function parameters and return values
- Small, testable functions
- Keep failure modes explicit; avoid silent `except:` catches
- No secrets in code or logs — use env vars; prefer `.env` locally (not committed)

## Implementation Workflow

```
1. Run your failing tests (confirm they fail)
2. Write minimal code to make tests pass
3. Run tests again (confirm they pass)
4. Refactor if needed (tests still pass)
```

**Rule:** If tests don't pass, don't move forward.

## Handling Missing/Flaky Tests

- No tests exist → Go back to design phase, add tests first
- Tests are flaky → Fix or skip with justification before proceeding
- Slow tests (>5s) → Mark and run separately; don't block fast feedback

## When Blocked

- Environment issues (network/SSL/quotas) → Surface issue, skip gracefully
- Be explicit about paid API usage; default to cheapest safe model

## LLM/Agent Usage

- Use cheapest safe model for tests/smoke; escalate only when accuracy requires
- API keys from env vars only; never embed or log plaintext
- Ask user which env var to use for LLM key
- Redact PII/secrets from prompts and logs

## CI & Lint

- Run linter/formatter during implementation; fix errors as you go
- Use project-defined tools (don't mix formatters)

## Dependency Management

- Pin versions in dependency files
- Update dependencies intentionally, not drive-by
- Prioritize security updates

---

**→ Next:** When implementation is complete, load `references/precommit.md` to prepare commit.
