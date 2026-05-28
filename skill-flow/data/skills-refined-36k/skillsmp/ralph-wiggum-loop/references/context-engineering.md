# Context Engineering: The malloc/free Problem

This explains the theoretical foundation for why the Ralph loop works.

## The Problem: No `free()`

Traditional programming:
```c
char* data = malloc(1024);  // Allocate
// ... use data ...
free(data);                  // Release
```

LLM context windows:
```
prompt = "Your task is..."              // Allocate
file_content = read_file("main.py")     // Allocate
result = run_command("npm test")        // Allocate
error = "Test failed: ..."              // Allocate
// ... no way to release ...
```

Every interaction permanently consumes context. No mechanism to discard stale information.

## Context Pollution

**Early session (fresh):**
```
[System: 2K] [Task: 500] [File: 1K]
Total: ~3.5K of 200K — Sharp reasoning
```

**Late session (polluted):**
```
[System: 2K] [Task: 500] [20 files: 30K] [50 tools: 15K] [Errors: 8K] [Old reasoning: 10K]
Total: ~65K — Gutter state
```

Critical information buried. Attention diluted. Agent forgets what it was doing.

## The "Smart Zone"

LLMs perform best at 40-60% context utilization.

For 200K context:
- Below 80K: Generally sharp
- 80K-120K: Functional but declining
- Above 120K: Gutter territory

## Why Traditional Solutions Fail

**"Bigger context window"** — Delays the problem, doesn't solve it. 1M tokens still has no `free()`.

**"Summarize old content"** — Loses information. Summarized stack traces lose line numbers.

**"Use RAG"** — Helps for reference, doesn't clear working context of tool results and reasoning.

## The Ralph Solution: Exit as `free()`

The only way to free LLM context is process termination.

```bash
gumloop --choo-choo
# Internally:
# while :; do cat PROMPT.md | $CLI ; done
```

Each iteration:
1. Allocates fresh context
2. Reads state from disk (not memory)
3. Does one task
4. Writes to disk
5. Exits → context freed

## Why Git Is Required

Git is external memory:

| Lost on Exit | Persists in Git |
|--------------|-----------------|
| Files read | Modified source |
| Tool output | Commits |
| Error traces | Commit messages |
| Reasoning | Implementation state |

Each iteration: `git log`, `git diff`, read files = fresh understanding of current state.

## Prompt Design Implications

**Keep prompts lean:** Loaded every iteration. 10K prompt = 10K overhead per loop.

**One task per iteration:** Multiple tasks = accumulated context within the iteration.

**Progress in files:** Bad: "Continue from step 5." Good: "Check IMPLEMENTATION_PLAN.md for status."

## Context Budgeting

```
200K total
- 2K   system prompt
- 5K   PROMPT.md
- 10K  reference docs
- 50K  working room
= 133K reasoning headroom

Target: Exit before 100K total
```

## The Primitive

The Ralph loop is a primitive like `for` or `while`. Complex orchestration patterns are built FROM this, not instead of it.

Master the single loop. Then compose.
