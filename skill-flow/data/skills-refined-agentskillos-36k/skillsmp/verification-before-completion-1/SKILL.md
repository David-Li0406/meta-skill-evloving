---
name: verification-before-completion
description: Forces agents to run verification commands and show evidence before claiming completion. Prevents "it should work" without proof.
---

# Verification Before Completion

> **Load this skill** when you need to ensure work is actually verified, not just claimed complete.

## Core Principle

**NOTHING is "done" without PROOF it works.**

Claims without evidence are worthless. Every completion claim must be backed by:
- Command output showing success
- Test results showing pass
- Build output showing no errors
- Observable behavior matching requirements

---

## Verification Checklist

Before marking ANY task complete, verify:

### 1. Type Safety
```bash
# Run LSP diagnostics on changed files
lsp_diagnostics(filePath="path/to/changed/file.ts")
```
**Required Evidence:** Clean output (no errors)

### 2. Build Success
```bash
# Run project build command
bun run build  # or npm run build, etc.
```
**Required Evidence:** Exit code 0, no error messages

### 3. Test Passage
```bash
# Run relevant tests
bun test  # or npm test, pytest, etc.
```
**Required Evidence:** All tests pass (or document pre-existing failures)

### 4. Manual Verification
- Read the changed files
- Verify changes match requirements
- Check edge cases

**Required Evidence:** Describe what you observed

---

## Anti-Patterns (BLOCKING)

| Violation | Why It Fails |
|-----------|--------------|
| "It should work now" | No evidence. Run it. |
| "I added the tests" | Did they pass? Show output. |
| "Fixed the bug" | How do you know? What did you test? |
| "Implementation complete" | Did you verify against success criteria? |
| Skipping test execution | Tests exist to be RUN |
| "The code looks correct" | Looking isn't testing. Execute it. |

---

## Evidence Format

When reporting completion, include:

```
## Verification Evidence

### Build
✅ `bun run build` - Exit code 0
Output: [paste relevant output]

### Tests
✅ `bun test` - 42 tests passed
Output: [paste test summary]

### Type Check
✅ `lsp_diagnostics` - No errors in changed files

### Manual Check
✅ Verified [specific behavior] works as expected
```

---

## When to Load This Skill

- Before completing any implementation task
- When delegating to coder/frontend agents
- Before reporting task completion to user
- When reviewing subagent work

---

## Quick Reference

| Phase | Command | Evidence Needed |
|-------|---------|-----------------|
| Build | `bun run build` | Exit code 0 |
| Test | `bun test` | All pass |
| Types | `lsp_diagnostics` | No errors |
| Lint | `bun run lint` | No warnings |

**CLAIM NOTHING WITHOUT PROOF. EXECUTE. VERIFY. SHOW EVIDENCE.**
