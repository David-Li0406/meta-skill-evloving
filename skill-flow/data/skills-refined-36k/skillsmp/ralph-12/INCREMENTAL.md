# Incremental Analysis for Ralph

Avoid full codebase re-analysis on subsequent `/ralph` calls.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  .ralph/                                                    │
│                                                             │
│  project-context.md     ← Base analysis (cached)            │
│  analysis-meta.json     ← Timestamps, hashes, version       │
│  goal-context.md        ← Goal-specific (always fresh)      │
│  task.md                ← Current tasks                     │
│  guardrails.md          ← Accumulated guardrails            │
└─────────────────────────────────────────────────────────────┘
```

## Analysis Layers

### Layer 1: Base Analysis (Cached)

Stable project information that rarely changes:
- Framework/stack detection
- Directory structure
- Available commands (test, lint, build)
- Database setup
- Auth patterns
- Code style patterns

**Cache invalidation triggers:**
- `package.json` changed (dependencies)
- Major config files changed
- New directories added
- > 7 days old

### Layer 2: File Index (Incremental)

Map of all source files with metadata:
- File path
- Last modified time
- Key exports/functions
- Hash of content

**Update strategy:**
- Only re-index files with changed mtime
- Add new files
- Remove deleted files

### Layer 3: Goal Context (Always Fresh)

Goal-specific exploration:
- Files related to current goal
- Functions to modify
- Tests to run
- Specific patterns for this task

**Always regenerated** because goals differ.

---

## analysis-meta.json Schema

```json
{
  "version": "1.0",
  "project": "my-app",
  "created": "2026-01-22T10:00:00Z",
  "lastUpdated": "2026-01-22T15:30:00Z",
  "lastGoal": "fix auth bug",

  "baseAnalysis": {
    "timestamp": "2026-01-22T10:00:00Z",
    "packageJsonHash": "abc123",
    "configHashes": {
      "tsconfig.json": "def456",
      "prisma/schema.prisma": "ghi789"
    }
  },

  "fileIndex": {
    "lastScan": "2026-01-22T15:30:00Z",
    "totalFiles": 245,
    "indexed": {
      "src/lib/auth/token.ts": {
        "mtime": "2026-01-22T14:00:00Z",
        "hash": "xyz123",
        "exports": ["refreshToken", "validateToken", "invalidateTokens"]
      }
    }
  },

  "guardrails": {
    "fromProject": 3,
    "fromMemory": 2,
    "learnedThisRun": 1
  }
}
```

---

## Incremental Workflow

### On `/ralph "goal"`:

```
1. Check .ralph/analysis-meta.json exists?
   │
   ├─ NO: Full analysis
   │      - Analyze codebase
   │      - Create project-context.md
   │      - Create analysis-meta.json
   │      - Do goal-specific exploration
   │
   └─ YES: Incremental update
           │
           ├─ Check base analysis validity
           │   - package.json hash same?
           │   - Config files unchanged?
           │   - Age < 7 days?
           │   │
           │   ├─ Valid: Reuse base analysis
           │   └─ Invalid: Re-run base analysis
           │
           ├─ Incremental file index
           │   - git diff --name-only {last_scan}
           │   - Re-index only changed files
           │   - Update file index in meta.json
           │
           └─ Goal-specific exploration (always fresh)
               - Find files related to new goal
               - Create goal-context.md
```

### Change Detection Methods

**Method 1: Git-based (fast)**
```bash
# Files changed since last analysis
git diff --name-only --since="{last_scan_time}" HEAD

# Or using commit
git diff --name-only {last_analyzed_commit} HEAD
```

**Method 2: Mtime-based (no git required)**
```bash
# Find files modified after timestamp
find src -type f -newermt "2026-01-22 10:00:00"
```

**Method 3: Hash-based (most accurate)**
```bash
# Compare content hashes
# Store in analysis-meta.json, compare on next run
```

---

## Clorch Implementation

### Check Analysis Freshness

```bash
# Quick check if analysis exists and is fresh
if [ -f ".ralph/analysis-meta.json" ]; then
  LAST_UPDATE=$(cat .ralph/analysis-meta.json | jq -r '.lastUpdated')
  AGE_HOURS=$(( ($(date +%s) - $(date -d "$LAST_UPDATE" +%s)) / 3600 ))

  if [ $AGE_HOURS -lt 168 ]; then  # Less than 7 days
    echo "INCREMENTAL"
  else
    echo "FULL"
  fi
else
  echo "FULL"
fi
```

### Incremental Update Script

```bash
# Get changed files since last scan
LAST_SCAN=$(cat .ralph/analysis-meta.json | jq -r '.fileIndex.lastScan')
CHANGED_FILES=$(git diff --name-only --since="$LAST_SCAN" HEAD 2>/dev/null || \
                find src -type f -newermt "$LAST_SCAN" 2>/dev/null)

if [ -z "$CHANGED_FILES" ]; then
  echo "No changes since last analysis"
else
  echo "Re-analyzing changed files:"
  echo "$CHANGED_FILES"
  # Re-run tldr structure only on changed files
  for file in $CHANGED_FILES; do
    tldr extract "$file" >> .ralph/incremental-update.md
  done
fi
```

---

## Prompt Enhancement

When reusing cached analysis, prompt includes:

```markdown
## Project Context

{from cached project-context.md}

## Recent Changes (since last Ralph run)

Files modified:
- src/lib/auth/token.ts (added invalidateOnPasswordChange)
- tests/auth.test.ts (added new test)

## Goal-Specific Context

{fresh exploration for current goal}
```

---

## Guardrails Accumulation

Guardrails persist across Ralph runs:

```markdown
# Guardrails

## Project Patterns (from initial analysis)
{stable patterns}

## From Memory
{recalled learnings}

## Learned from Previous Runs
- [2026-01-22 goal:"fix auth"] Always invalidate tokens on password change
- [2026-01-22 goal:"add rate limit"] Use Redis for rate limit state

## Learned This Run
{new guardrails added during current execution}
```

---

## Summary

| Aspect | First Run | Subsequent Runs |
|--------|-----------|-----------------|
| Base analysis | Full (~30s) | Cached (0s) |
| File index | Full scan | Incremental (changed only) |
| Goal exploration | Fresh | Fresh (different goal) |
| Guardrails | Seeded | Accumulated |
| Memory recall | Fresh | Fresh (goal-specific) |

**Time savings:**
- Large codebase: 30s → 2s for base analysis
- File indexing: O(n) → O(changed files)
- Goal exploration: Always fresh (required for accuracy)
