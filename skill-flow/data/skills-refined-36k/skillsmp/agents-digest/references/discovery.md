# Artifact Discovery

Patterns for discovering agent work artifacts across the filesystem.

## Discovery Sources

### Trails Events

Query structured agent lifecycle events:

```bash
# All completed events last 24h
trails trail replay --since 24h --format json | \
  jq '.[] | select(.action == "completed")'

# High confidence events
trails trail sieve --min-confidence 8 --since 7d --format json

# Specific agent
trails trail replay --agent claude --since 3d --format json

# By project (from git context)
trails trail replay --since 7d --format json | \
  jq '.[] | select(.git.repo | contains("arbor"))'
```

### Git Commits

Find commits co-authored by agents:

```bash
# All agent commits
git log --all --grep="Co-Authored-By.*Claude\|Codex\|Copilot" --since="7 days ago"

# With file stats
git log --all --grep="Co-Authored-By" --stat --since="7 days ago"

# Extract commit hashes
git log --all --grep="Co-Authored-By" --since="7 days ago" --format="%H"
```

### Planning Sessions

```bash
# Recent plans
find ~/.agents/plans/ -name "plan.md" -mtime -7 -type f

# By project
ls -1 ~/.agents/plans/arbor/*/plan.md

# Parse plan metadata
head -20 ~/.agents/plans/arbor/*/plan.md | grep "^#"
```

### Repo .agents/ Directories

```bash
# Discover all repos with .agents/
fd -t d "^\.agents$" ~/Developer/

# Recent session outputs
find ~/Developer/*/.agents/sessions/ -name "*.md" -mtime -7

# Context files
fd "context.md" ~/Developer/*/.agents/
```

### Claude Code Sessions

```bash
# List recent sessions
agents session list --json | jq '.[] | select(.status == "completed")'

# Session output files
find ~/.claude/projects/ -name "*.jsonl" -mtime -7
```

## Discovery Strategies

### Daily Digest

```bash
# Combine sources for last 24h
SINCE="24h"

# 1. Trails events
trails trail replay --since $SINCE --format json > /tmp/trails.json

# 2. Git commits
git log --all --grep="Co-Authored-By" --since="1 day ago" --format="%H|%s|%an|%ad" > /tmp/commits.txt

# 3. Sessions
agents session list --json | jq '.[] | select(.completed_at > (now - 86400))' > /tmp/sessions.json
```

### Project Digest

```bash
# All activity for one project
PROJECT="arbor"

# Trails events mentioning project
trails trail replay --since 30d --format json | \
  jq --arg proj "$PROJECT" '.[] | select(.task | contains($proj))' > /tmp/trails-$PROJECT.json

# Git commits in project repo
cd ~/Developer/$PROJECT/$PROJECT-xyz
git log --all --grep="Co-Authored-By" --since="30 days ago" --format="%H|%s" > /tmp/commits-$PROJECT.txt

# Plans for project
find ~/.agents/plans/$PROJECT/ -name "plan.md" > /tmp/plans-$PROJECT.txt
```

### Agent-Specific

```bash
# All Claude Code activity
trails trail replay --agent claude --since 7d --format json

# All Codex activity
trails trail replay --agent codex --since 7d --format json
```

## Parsing Artifacts

### Trail Event Structure

```typescript
interface TrailEvent {
  event_id: string;
  timestamp: string;
  agent: string;
  action: string;
  task: string;
  confidence?: number;
  summary?: string;
  git?: {
    committed: boolean;
    pushed: boolean;
    repo?: string;
  };
  artifacts?: string[];
}
```

### Git Commit Parsing

```bash
# Extract commit metadata
git show --stat --format="%H|%s|%an|%ad|%b" $COMMIT_HASH | \
  awk -F'|' '{print "Hash:", $1, "\nSubject:", $2, "\nAuthor:", $3, "\nDate:", $4}'
```

### Plan Parsing

```bash
# Extract plan sections
sed -n '/^## /,/^## /p' plan.md  # Extract sections

# Count tasks
grep -c "^- \[ \]" plan.md       # Pending
grep -c "^- \[x\]" plan.md       # Completed
```

## Discovery CLI

Proposed `agents discover` command:

```bash
# Discover all artifacts
agents discover --since 7d --format json

# By type
agents discover --type trails --since 24h
agents discover --type git --since 3d
agents discover --type plans --since 7d

# By project
agents discover --project arbor --since 30d

# Output
{
  "trails": [...],
  "commits": [...],
  "plans": [...],
  "sessions": [...]
}
```

## Deduplication

```typescript
const deduplicateEvents = (events: TrailEvent[]): TrailEvent[] => {
  const seen = new Set<string>();
  return events.filter(e => {
    const key = `${e.agent}-${e.task}-${e.timestamp.split('T')[0]}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
};
```
