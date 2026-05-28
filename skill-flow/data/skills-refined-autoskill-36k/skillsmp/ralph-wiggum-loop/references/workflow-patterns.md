# Workflow Patterns

Structured approaches built on top of the core Ralph technique. Not required — the basic loop works on its own.

## Two-Mode Operation

Split planning and building into separate prompt files.

### Planning Mode

Gap analysis. Generates prioritized task list.

```bash
gumloop --prompt PROMPT_plan.md --choo-choo 5
```

**PROMPT_plan.md:**
```markdown
1. Study specs/* to understand requirements.
2. Study src/* to understand current implementation.
3. Compare: what's specified vs what exists?
4. Create/update IMPLEMENTATION_PLAN.md with gaps.
5. Do NOT implement anything.
```

### Building Mode

Implements from the plan, one task per iteration.

```bash
gumloop --prompt PROMPT_build.md --choo-choo 20
```

**PROMPT_build.md:**
```markdown
1. Read IMPLEMENTATION_PLAN.md for priorities.
2. Pick the most important incomplete task.
3. Implement it completely.
4. Run tests.
5. Mark complete in plan. Commit. Exit.
```

### Switching Modes

- Plan mode when starting or plan is stale
- Build mode to execute
- Back to plan if going off track
- Plan is disposable — regenerate don't fight

## File Structure

```
project/
├── PROMPT.md              # Or _plan.md / _build.md
├── AGENTS.md              # How to build/run (operational)
├── IMPLEMENTATION_PLAN.md # Task list (maintained by agent)
├── specs/                 # Requirements
│   ├── feature-a.md
│   └── feature-b.md
└── src/
```

### PROMPT.md

Instructions loaded each iteration. Keep lean — consumes context budget.

### AGENTS.md

Operational: how to build, test, run. ~50 lines max.

```markdown
## Build
npm install && npm run build

## Test
npm test

## Patterns
- Components in src/components/
- Tests co-located with source
```

NOT a changelog. Progress notes go in IMPLEMENTATION_PLAN.md.

### IMPLEMENTATION_PLAN.md

Task list maintained by the agent:

```markdown
## In Progress
- [ ] Working on X

## High Priority
- [ ] Next task
- [ ] Second priority

## Done
- [x] Completed task

## Notes
- Discovered issue with Y
```

### specs/

One file per topic. Requirements the agent works toward.

## Backpressure

Mechanisms that reject invalid work.

### Using --verify

Run automated checks after each iteration:

```bash
gumloop --choo-choo --verify "npm test"
gumloop --choo-choo --verify "tsc --noEmit"
gumloop --choo-choo --verify "npm test && npm run lint"
```

### Common Checks

| Type | Command | Catches |
|------|---------|---------|
| Types | `tsc --noEmit` | Type errors |
| Tests | `npm test` | Logic errors |
| Lint | `eslint .` | Style issues |
| Build | `npm run build` | Compilation |

### In Your Prompt

Also add backpressure instructions:
```markdown
Run tests. Only commit if tests pass.
If tests fail, fix before committing.
```

**Strong backpressure:** Tests, types — binary pass/fail.
**Weak backpressure:** "Make sure it works" — subjective, gameable.

## Subagents

Some CLIs (Claude Code, Amp) support parallel subagents.

**Fan out for reading:**
```markdown
Use parallel subagents to search codebase for existing implementations.
```

**Single for validation:**
```markdown
Use 1 subagent for running tests.
```

If your CLI doesn't support subagents, remove references. Technique still works.

## Guardrail Numbering

Higher numbers = higher priority:

```markdown
1. Study codebase before changes.
2. Implement one task, commit.

99999. Search before implementing.
999999. Run tests before committing.
```

New guardrails go at end with more digits.
