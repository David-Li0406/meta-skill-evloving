# Bug Fix Workflow

> **STOP. Do not touch code until you can reproduce the bug.**

## Phase 1: Reproduce

Before any code changes:

- [ ] **Note the GitHub issue** — If bug came from roadmap's `GH` column, note the issue number (e.g., `#123`)
- [ ] **Confirm the bug exists** — Run the failing scenario manually or via test
- [ ] **Identify exact failure** — What happens vs what should happen?
- [ ] **Check if already fixed** — Search recent commits, PRs, issues

If you cannot reproduce the bug, **do not proceed**. Ask for more information.

## Phase 2: Write Failing Test

> **The test IS your bug report.**

```
1. Write a test that fails due to the bug
2. Confirm it fails for the right reason
3. This test becomes your regression guard
```

**Do not skip this step.** A bug without a test will come back.

## Phase 3: Understand Root Cause

Ask yourself:

| Question | Why It Matters |
|----------|----------------|
| **Why** does it fail, not just where? | Fixes symptoms vs root cause |
| Is this a single bug or pattern? | May need broader fix |
| When was it introduced? | `git bisect` can help |
| Is it a regression? | Higher urgency, may need hotfix |

## Phase 4: Fix Minimally

**Smallest change that makes the test pass.**

- Touch only what's necessary
- Don't refactor surrounding code (separate PR if needed)
- Don't add unrelated improvements

## Phase 5: Verify

- [ ] **Failing test now passes**
- [ ] **Full test suite passes** — No regressions introduced
- [ ] **Manual verification** — Confirm fix in real environment if applicable

## Phase 6: Documentation

| Situation | Action |
|-----------|--------|
| Bug exposed incorrect documentation | **Fix the docs** |
| Fix changes user-visible behavior | **Update CHANGELOG** |
| Bug was caused by misleading docs | **Fix the docs** |
| Internal bug, no user impact | No doc changes needed |
| Found unrelated doc drift | Fix it (but separate commit) |

## Quick Checklist

Before committing a bug fix:

```
[ ] Bug is reproduced
[ ] Failing test exists
[ ] Root cause is understood (not just symptom)
[ ] Fix is minimal
[ ] All tests pass
[ ] Docs updated (if applicable)
[ ] CHANGELOG updated (if user-visible)
[ ] GitHub issue noted for PR (if applicable)
```

> **Tip:** If this bug has a GitHub issue (from roadmap's `GH` column), include `Closes #123` in your PR description to auto-close it on merge.

---

**→ Next:** Load `references/precommit.md` to prepare commit.
