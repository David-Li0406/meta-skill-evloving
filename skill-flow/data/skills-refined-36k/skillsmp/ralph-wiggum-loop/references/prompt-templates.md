# Prompt Templates

Starting points for PROMPT.md. Meant to be **tuned** — start here, observe failures, add guardrails.

## Minimal

```markdown
Study the codebase.
Find the most important thing to implement.
Implement it.
Run tests.
Commit and exit.
```

## Basic Build

```markdown
1. Study codebase to understand current state.
2. Check IMPLEMENTATION_PLAN.md (if exists) for priorities.
3. Choose ONE task.
4. Search to confirm it's not already done.
5. Implement the task.
6. Run tests. Fix failures before continuing.
7. Commit with descriptive message.
8. Update IMPLEMENTATION_PLAN.md if it exists.
```

## Planning

```markdown
1. Study specs/* for requirements.
2. Study src/* for current implementation.
3. Compare: what's specified vs what exists?
4. Create/update IMPLEMENTATION_PLAN.md:
   - What's missing
   - What's incomplete
   - Prioritized by importance

Do NOT implement anything. Planning only.
```

## Elaborate Build

Fuller prompt with guardrails baked in:

```markdown
0. Study specs/* for requirements.
1. Read IMPLEMENTATION_PLAN.md for highest priority task.
2. Search codebase to confirm not already done.
3. Implement completely. No placeholders.
4. Run tests. Fix failures before proceeding.
5. Update IMPLEMENTATION_PLAN.md.
6. Commit with descriptive message.

Guidelines:
- One task per session. Commit and exit after one task.
- Search before implementing.
- Run tests before committing.
- Update plan with learnings.
- Keep commits atomic.
```

## Reverse Engineering

```markdown
1. Study target system behavior (logs, API, docs).
2. Document understanding in specs/[component].md.
3. Identify one aspect to implement.
4. Write tests based on observed behavior.
5. Implement to pass tests.
6. Commit.

Do not copy code. Implement from observed behavior only.
```

## Guardrail Examples

Add when you observe failure patterns:

```markdown
# Reimplements existing code:
99999. Before implementing, search codebase first.

# Writes incomplete code:
99999. Implement completely. No placeholders or TODOs.

# Forgets tests:
99999. Run tests before committing.

# Bloated AGENTS.md:
99999. Keep AGENTS.md operational only.

# Ignores plan:
99999. Follow IMPLEMENTATION_PLAN.md priorities.

# Too many changes:
99999. One task per session. Commit and exit.
```

## CLI-Specific Notes

### Claude Code
- Supports subagents
- Choo-choo flags: `--dangerously-skip-permissions`
- Has `ultrathink` for complex reasoning

### Amp
- Supports parallel workers
- Choo-choo flags: `--dangerously-allow-all`

### Aider
- No subagents — remove references
- Choo-choo flags: `--yes-always --no-pretty`
- Works well with simpler prompts

### Generic
- If piping works, gumloop works
- Start minimal, add based on CLI capabilities
