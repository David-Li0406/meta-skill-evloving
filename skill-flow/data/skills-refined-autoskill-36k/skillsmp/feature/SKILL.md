---
name: feature
description: Start structured feature implementation workflow. Use when implementing new features, adding functionality, or building complete user-facing capabilities.
allowed-tools: ["shell", "read_file", "apply_patch", "write_file", "update_plan"]
metadata:
  short-description: Complete feature implementation workflow
---

# Feature Implementation Workflow

**Read this reference:**
- `~/.config/agent/workflows/feature.md` - Complete 7-phase feature workflow

## Mode Awareness

This skill respects coding modes when performing implementation work:
- Check if a mode is active in the session (normal/autopilot/full-auto)
- During Phase 3 (Implement) and Phase 5 (Quality Check), apply mode-specific confirmation behavior
- See the `coding` skill for full mode definitions and guardrails

If no mode is active, default to `normal` mode (confirm all modifications).

## Instructions

Follow this structured 7-phase workflow for feature implementation:

### Phase 1: Understand

Per AGENT.md Problem-Solving Framework:
- Gather all requirements and constraints
- Identify unknowns and dependencies
- Restate the problem to confirm understanding
- Read relevant existing code
- Ask clarifying questions if needed

### Phase 2: Plan

Apply decomposition and parallelization:
- Design approach from first principles
- Break into atomic, testable subproblems
- Identify dependencies and execution order
- Find parallelization opportunities
- Create TODO list with all tasks

### Phase 3: Implement

Apply task discipline:
- Work through TODO list systematically
- Exactly ONE task in_progress at a time
- Mark completed immediately after finishing
- Validate incrementally (don't defer all verification)
- Document decisions as you go

### Phase 4: Test

Apply testing guidelines:
- Write unit tests (table-driven for Go)
- Aim for 100% coverage, minimum 80%
- Test edge cases and error paths
- Run with race detector: `go test -race ./...`
- Ensure tests are isolated (no containers/network)

**TDD guidance:** TDD is encouraged by default, not required. If strict TDD is explicitly requested, invoke `tdd-enforce`.

### Phase 5: Quality Check

Apply quality and safety standards:
- Run full pre-commit workflow (format, lint, test)
- Verify code correctness
- Check runtime safety (race conditions, nil checks, resource leaks)
- Check security safety (injection, auth, input validation)
- Ensure performance is acceptable

### Phase 6: Document

Update documentation:
- Add/update code comments where logic isn't self-evident
- Update README if public API changed
- Document design decisions
- Note any caveats or limitations

### Phase 7: Review

Perform self-review:
- Read through all changes
- Verify priorities (safety, correctness, idiomaticity, performance)
- Check for issues you'd catch in code review
- Fix any problems found
- Ready for external review

## Success Criteria

- All tests pass
- No lint errors
- 80%+ coverage
- All safety checks pass
- Documentation updated
- Ready for code review

**Completion gate:** Use `verification-before-completion` before any completion claim.

## Arguments

Feature to implement: ${ARGUMENTS}
