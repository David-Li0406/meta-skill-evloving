---
name: agents-digest
description: Generate narrative epubs from agent work artifacts. Triggers include "create digest", "summarize agent work", "prepare for sync", or when organizing agent sessions for e-ink review. Discovers sessions, plans, code changes, and trails for readable digests.
---

# agents-digest

generate narrative epubs from agent work artifacts. discover sessions, plans, code changes, and trails for readable digests on e-ink.

## when to use

| use | skip |
|-----|------|
| creating readable summaries of agent sessions | viewing raw logs |
| digesting multi-day loop work | single task reviews |
| keeping tabs on agent activity | real-time monitoring |
| organizing agent work for X4 /agents/ folder | archiving sessions |

## philosophy

> "agent work narratives, not raw logs"

| principle | application |
|-----------|-------------|
| narrative first | tell story of what was built, not command logs |
| context-rich | include code snippets, decisions, blockers |
| e-ink optimized | readable for hours on device |
| automated discovery | find artifacts without manual curation |

## artifact sources

| source | location | content |
|--------|----------|---------|
| **session logs** | `~/.claude/projects/*/` | Claude Code session transcripts |
| **trails events** | `~/.trails/events.ndjson` | Agent lifecycle events |
| **planning sessions** | `~/.agents/plans/` | Planning outputs |
| **repo .agents/** | `~/Developer/*/.agents/` | Per-repo agent artifacts |
| **code changes** | git logs with Co-Authored-By | Commits by agents |

## decision tree: digest scope

```
What timeframe?
├── Daily → last 24h of agent activity
├── Weekly → last 7d across all agents
├── Session → specific Claude Code session
├── Loop → specific loop run (from trails)
├── Project → all activity for one repo
└── Custom → date range or filter
```

## workflow: generate digest

```
1. discover artifacts
   ├── query trails for agent events
   ├── scan ~/.agents/plans/ for recent plans
   ├── scan repos for .agents/ directories
   └── git log --grep="Co-Authored-By.*Claude\|Codex"

2. filter by scope
   ├── date range (since/until)
   ├── agent type (claude, codex, copilot)
   ├── project (repo name)
   └── confidence threshold (>= 7)

3. build narrative
   ├── group by project or session
   ├── chronological or thematic ordering
   ├── include: task, decisions, code snippets, outcomes
   ├── exclude: raw command output, verbose traces
   └── format as DocBlock[] (NormalizedDocument)

4. render to epub
   ├── use eink-style (narrative profile)
   ├── syntax highlighting for code snippets
   ├── internal links for cross-references
   └── output to ~/.epub/library/ (source: agents-digest)

5. sync to X4
   ├── place in /agents/ folder
   ├── filename: agents-{date}.epub
   └── metadata: agent, project, confidence
```

## narrative structure

### Daily Digest

```markdown
# Agent Activity — January 22, 2026

## arbor (Claude Code)

**Session:** 3h 15m
**Confidence:** 9/10

### Task: Implement auth flow

Added Clerk integration with session persistence. Key decisions:
- JWT over session cookies (mobile compatibility)
- 15-minute access tokens with refresh rotation

Code highlights:
```typescript
export const auth = new ClerkAuth({ ... });
```

Verification: All tests pass, deployed to staging.

---

## kumori (Codex)

**Session:** 45m
**Confidence:** 8/10

### Task: Fix image upload

...
```

### Weekly Roundup

Group by project, summarize activity:

```markdown
# Weekly Agent Activity — Week of Jan 15-22

## arbor
- 5 sessions, 12h total
- Features: auth flow, profile page, settings
- Tests: 15 new, all passing
- Confidence: avg 8.5/10

## kumori
- 2 sessions, 3h total
- Fixes: image upload, style rendering
- Confidence: avg 8/10
```

## discovery patterns

### Trails Query

```bash
# Agent events last 24h
trails trail replay --since 24h --format json | \
  jq '.[] | select(.agent == "claude" or .agent == "codex")'

# Completed tasks with high confidence
trails trail sieve --action completed --min-confidence 8 --since 7d
```

### Git Commits

```bash
# Commits by agents
git log --all --grep="Co-Authored-By.*Claude\|Codex" --since="7 days ago" --format="%H|%s|%an|%ad"
```

### Plans

```bash
# Recent planning sessions
find ~/.agents/plans/ -name "plan.md" -mtime -7
```

### Repo Artifacts

```bash
# Discover .agents/ directories
fd -t d "^\.agents$" ~/Developer/
```

## content extraction

### From Trails

```typescript
interface TrailEvent {
  agent: string;
  action: "started" | "completed" | "blocked";
  task: string;
  confidence?: number;
  summary?: string;
  artifacts?: string[];
  git?: { committed: boolean; pushed: boolean };
}

const extractNarrative = (events: TrailEvent[]): string => {
  const completed = events.filter(e => e.action === "completed");
  return completed.map(e => `
### ${e.task}

${e.summary}

Confidence: ${e.confidence}/10
  `.trim()).join("\n\n");
};
```

### From Git Commits

```typescript
const extractCodeChanges = async (commit: string): Promise<CodeSnippet[]> => {
  const diff = await execAsync(`git show ${commit} --stat`);
  const files = parseDiffStat(diff);

  return files.map(f => ({
    path: f.path,
    linesAdded: f.added,
    linesRemoved: f.removed,
    snippet: extractRelevantLines(f.path, commit),
  }));
};
```

## tool integration

| tool | command | purpose |
|------|---------|---------|
| trails | `trails trail replay --since 24h` | query agent events |
| git | `git log --grep="Co-Authored-By"` | find agent commits |
| agents | `agents session list --json` | recent sessions |
| epub | `epub agents digest --since 24h` | generate digest |

### agents CLI integration

```bash
# Generate daily digest
agents digest --since 24h --output ~/.epub/library/agents-daily.epub

# Generate for specific project
agents digest --project arbor --since 7d --output arbor-weekly.epub

# Generate from session
agents digest --session hostagent-20241225-abc1 --output session-digest.epub
```

## narrative templates

### Session Summary

```markdown
# {Project} — {Date}

**Agent:** {agent}
**Duration:** {duration}
**Confidence:** {confidence}/10

## Task

{task description}

## Approach

{key decisions and reasoning}

## Implementation

{code snippets with highlights}

## Verification

{tests, build status}

## Blockers

{issues encountered, if any}

## Next Steps

{follow-up work}
```

### Multi-Session Digest

```markdown
# {Project} — {Date Range}

## Overview

{sessions count} sessions, {total duration}, avg confidence {avg confidence}/10

## Features Completed

- {feature 1}
- {feature 2}

## Code Changes

{files changed}, +{lines added} -{lines removed}

## Test Coverage

{new tests}, {pass rate}

## Highlights

{notable code snippets or decisions}
```

## filtering rules

### Include

- Completed tasks (action: "completed")
- Confidence >= 7
- Has artifacts (code changes, plans)
- Recent (within scope timeframe)

### Exclude

- Low confidence (< 7) unless explicitly requested
- Blocked/failed without resolution
- Verbose command output
- Duplicate events (dedup by task + timestamp)

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| raw log dumps | unreadable narrative | extract highlights, summarize |
| no code snippets | context missing | include relevant code changes |
| all events | noise | filter by confidence, completion |
| no chronology | hard to follow | sort by timestamp |
| missing project context | unclear scope | group by project |
| verbose traces | too much detail | summarize, link to full logs |

## references

- [references/discovery.md](references/discovery.md) - artifact discovery patterns
- [references/narrative-structure.md](references/narrative-structure.md) - digest formats and templates
- [references/code-extraction.md](references/code-extraction.md) - extracting relevant code snippets

## next steps

after generating digest:
1. review epub: `epub library list --source agents-digest`
2. sync to device: `epub device sync --agents`
3. verify rendering: check /agents/ folder on X4
