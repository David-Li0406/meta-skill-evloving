# Ralph Loop Agent Skill

Implementation of the Ralph (Ralph Wiggum) technique for iterative, self-referential development loops. The recommended implementation is an **orchestrator + worker subagent + judge** loop; a Claude Code Stop-hook version is included as an optional example.

## What is Ralph?

Ralph is a development methodology based on continuous AI agent loops. As Geoffrey Huntley describes it: **"Ralph is a Bash loop"** - a simple `while true` that repeatedly feeds an AI agent a prompt file, allowing it to iteratively improve its work until completion.

The technique is named after Ralph Wiggum from The Simpsons, embodying the philosophy of persistent iteration despite setbacks.

### Core Concept

Ralph works by repeating the same prompt each iteration while persisting the working directory so changes accumulate.

Recommended architecture:

- **Orchestrator (main agent)** spawns a fresh **worker subagent** to make changes, then a strict **judge** to decide pass/fail.
- If the judge fails, the orchestrator spawns a **new** worker subagent with judge-informed guidance (do not reuse the same worker conversation).

In Claude Code specifically, it can also be implemented using a **Stop hook** that intercepts exit attempts:

```text
# Optional Claude Code-only example:
# The Stop hook blocks exit and re-injects the same prompt.

# Then Claude Code automatically:
# 1. Works on the task
# 2. Tries to exit
# 3. Stop hook blocks exit
# 4. Stop hook feeds the SAME prompt back
# 5. Repeat until completion
```

The Claude Code example Stop hook is in `examples/claude-code/stop-hook.sh`.

This creates a **self-referential feedback loop** where:
- The prompt never changes between iterations
- Claude's previous work persists in files
- Each iteration sees modified files and git history
- Claude autonomously improves by reading its own past work in files

## Quick Start

```text
Build a REST API for todos. Requirements: CRUD operations, input validation, tests.

Keep iterating until all tests pass. Use a worker subagent + judge loop. Max iterations: 20.
```

See `ralph-loop/SKILL.md` for the orchestrator/worker/judge contracts and prompt templates.

## Prompt Writing Best Practices

### 1. Clear Completion Criteria

❌ Bad: "Build a todo API and make it good."

✅ Good:
```markdown
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- README with API docs
```

### 2. Incremental Goals

❌ Bad: "Create a complete e-commerce platform."

✅ Good:
```markdown
Phase 1: User authentication (JWT, tests)
Phase 2: Product catalog (list/search, tests)
Phase 3: Shopping cart (add/remove, tests)

Stop only when all phases are complete and verifiers pass.
```

### 3. Self-Correction

❌ Bad: "Write code for feature X."

✅ Good:
```markdown
Implement feature X following TDD:
1. Write failing tests
2. Implement feature
3. Run tests
4. If any fail, debug and fix
5. Refactor if needed
6. Repeat until all green
```

### 4. Escape Hatches

Always use `--max-iterations` as a safety net to prevent infinite loops on impossible tasks:

```text
# Recommended: Always set a reasonable iteration limit
Try to implement feature X. Max iterations: 20.

# In your prompt, include what to do if stuck:
# "After 15 iterations, if not complete:
#  - Document what's blocking progress
#  - List what was attempted
#  - Suggest alternative approaches"
```

## Philosophy

Ralph embodies several key principles:

### 1. Iteration > Perfection
Don't aim for perfect on first try. Let the loop refine the work.

### 2. Failures Are Data
"Deterministically bad" means failures are predictable and informative. Use them to tune prompts.

### 3. Operator Skill Matters
Success depends on writing good prompts, not just having a good model.

### 4. Persistence Wins
Keep trying until success. The loop handles retry logic automatically.

## When to Use Ralph

**Good for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration and refinement (e.g., getting tests to pass)
- Greenfield projects where you can walk away
- Tasks with automatic verification (tests, linters)

**Not good for:**
- Tasks requiring human judgment or design decisions
- One-shot operations
- Tasks with unclear success criteria
- Production debugging (use targeted debugging instead)

## Real-World Results

- Successfully generated 6 repositories overnight in Y Combinator hackathon testing
- One $50k contract completed for $297 in API costs
- Created entire programming language ("cursed") over 3 months using this approach

## Learn More

- Original technique: https://ghuntley.com/ralph/
- Ralph Orchestrator: https://github.com/mikeyobrien/ralph-orchestrator

## For Help

Ask Claude to explain how to start/cancel a Ralph loop and how completion promises work.
