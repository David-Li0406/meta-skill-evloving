# Hindsight Reference

This document is the single source of truth for Hindsight memory operations in Unit Work. All commands and agents that interact with Hindsight should reference this file for consistent bank name derivation, command patterns, and output handling.

## Bank Name Derivation

**CRITICAL:** The bank name must be consistent across all worktrees of the same repository.

```bash
# Correct: Use remote origin URL (consistent across worktrees)
BANK=$(git config --get remote.origin.url 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//' || basename "$(git worktree list 2>/dev/null | head -1 | awk '{print $1}')" || basename "$(pwd)")

# WRONG: Do NOT use git rev-parse --show-toplevel
# This returns the worktree path, causing each worktree to create a separate bank
```

**Fallback chain:**
1. Git remote origin URL → extract repo name
2. First worktree in list → extract directory name
3. Current working directory → use as fallback

## Memory Operations

### Recall (Read Operations)

**Use freely - recall is cheap.** Query memory before making decisions.

```bash
# Basic recall
hindsight memory recall "$BANK" "query describing what you need" --budget low

# With chunks for detailed context
hindsight memory recall "$BANK" "query" --budget mid --include-chunks

# Budget levels:
# --budget low   → Fast, surface-level results (use for resume detection)
# --budget mid   → Balanced depth (use for context gathering)
# --budget high  → Deep search (use sparingly, expensive)
```

**Common recall patterns:**

```bash
# Gotchas and learnings
hindsight memory recall "$BANK" "gotchas and learnings for <feature-type>" --budget mid --include-chunks

# Code location
hindsight memory recall "$BANK" "location of code related to: <topic>" --budget mid --include-chunks

# Progress tracking
hindsight memory recall "$BANK" "progress on <feature>" --budget low

# Review learnings
hindsight memory recall "$BANK" "code review learnings, past mistakes, type safety issues" --budget mid --include-chunks
```

### Retain (Write Operations)

**Always use --async.** Never block on memory writes.

```bash
hindsight memory retain "$BANK" "narrative description of learning" \
  --context "context-type: feature-name" \
  --doc-id "doc-identifier" \
  --async
```

**Context and doc-id conventions:**

| Use Case | Context Pattern | Doc-ID Pattern |
|----------|----------------|----------------|
| Gotcha/bug fix | `gotcha from <feature>` | `learn-<feature>` |
| Exploration | `exploration: <feature-type>` | `explore-<feature>` |
| Planning | `planning <feature>` | `plan-<feature>` |
| Implementation | `implementation: <feature>` | `impl-<feature>` |
| Review learning | `review learning` | `review-<feature>` |
| CI fix | `ci-fix: <error-type>` | `ci-<error-type>` |

### Reflect (Reasoning Operations)

**Use for complex reasoning** when you need Hindsight to think about something.

```bash
hindsight memory reflect "$BANK" "question requiring reasoning" --context "context"
```

## Output Handling

### ANSI Color Code Stripping

**CRITICAL:** Hindsight output contains ANSI color codes that must be stripped before processing.

```bash
# Strip ANSI codes from output
hindsight memory recall "$BANK" "query" --budget mid 2>&1 | sed 's/\x1b\[[0-9;]*m//g'

# For capturing into a variable
OUTPUT=$(hindsight memory recall "$BANK" "query" --budget mid 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
```

**Why this matters:**
- Raw output includes escape sequences like `[38;2;0;117;214m`
- These break text parsing and display
- Always strip when programmatically processing output

### Error Handling

**Graceful degradation - never block on Hindsight failures.**

```bash
# Check if Hindsight is available
if ! command -v hindsight &> /dev/null; then
  echo "Warning: Hindsight not available - proceeding without memory"
  # Continue without memory operations
fi

# Handle recall failures
OUTPUT=$(hindsight memory recall "$BANK" "query" --budget mid 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
if [[ $? -ne 0 ]] || [[ "$OUTPUT" == *"error"* ]]; then
  echo "Warning: Memory recall failed - starting fresh"
  # Continue without recalled context
fi

# Retain failures are non-blocking (--async handles this)
```

## Complete Example

```bash
# 1. Derive bank name (worktree-safe)
BANK=$(git config --get remote.origin.url 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//' || basename "$(git worktree list 2>/dev/null | head -1 | awk '{print $1}')" || basename "$(pwd)")

# 2. Recall with ANSI stripping
LEARNINGS=$(hindsight memory recall "$BANK" "gotchas for authentication" --budget mid --include-chunks 2>&1 | sed 's/\x1b\[[0-9;]*m//g')

# 3. Process the output
if [[ -n "$LEARNINGS" ]] && [[ "$LEARNINGS" != *"No results"* ]]; then
  echo "Found relevant learnings:"
  echo "$LEARNINGS"
else
  echo "No prior learnings found"
fi

# 4. Retain new learning (async, non-blocking)
hindsight memory retain "$BANK" "GOTCHA: OAuth tokens need 60-second buffer before expiry check" \
  --context "gotcha from authentication" \
  --doc-id "learn-auth-token-buffer" \
  --async
```

## Flags Reference

| Flag | Description | When to Use |
|------|-------------|-------------|
| `--budget low` | Fast, shallow search | Resume detection, quick checks |
| `--budget mid` | Balanced search | Context gathering, learnings |
| `--budget high` | Deep, expensive search | Comprehensive research (rare) |
| `--include-chunks` | Include source chunks | When you need detailed context |
| `--async` | Non-blocking write | **Always** for retain operations |
| `--context "..."` | Categorize the memory | All retain operations |
| `--doc-id "..."` | Unique document ID | All retain operations |

## Important Rules

1. **Always use remote origin URL for bank name** - NOT `git rev-parse --show-toplevel`
2. **Always strip ANSI codes** when processing output programmatically
3. **Always use --async for retain** - never block on memory writes
4. **Always use --include-chunks for recall** - provides source context
5. **Graceful degradation** - work without Hindsight if unavailable
6. **Budget appropriately** - `low` for quick checks, `mid` for context, `high` rarely
