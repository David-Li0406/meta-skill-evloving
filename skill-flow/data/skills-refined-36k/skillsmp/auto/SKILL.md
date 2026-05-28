---
name: auto
description: This skill should be used for autonomous single-repo orchestration. Triggers include "use auto", "autonomous mode", "work on this repo", or when starting a deep work session. LLM ideation discovers work, copilot swarm thinks, codex implements.
---

# auto

autonomous single-repo orchestration. LLM ideation discovers work, copilot swarm thinks, codex implements.

## philosophy

| principle | application |
|-----------|-------------|
| single repo context | one terminal per repo, auto works within cwd |
| git log as teacher | history is quality bar, trajectory, inspiration |
| separation of concerns | ideation discovers, copilot thinks, codex does |
| zero ambiguity for codex | all context resolved before implementation |
| verification grounded | real gates (codegen, types, tests, build) not vibes |
| skill orchestrates, CLI executes | skill decides WHAT and WHEN, `agents auto` handles HOW |

## when to use

| use | skip |
|-----|------|
| "use auto" | explicit single task ("fix this bug") |
| "autonomous mode" | research questions |
| "work on this repo" | cross-repo coordination (use multiple terminals) |
| starting deep work session | quick one-liner fixes |

## CLI integration

The `agents auto` command provides the execution layer. This skill orchestrates when and how to invoke it.

```bash
# Full autonomous mode: ideate + spawn + preview
agents auto --ideate --preview --project $REPO

# Dry run: see what would be spawned
agents auto --ideate --dry-run --project $REPO

# With specific ideation paths
agents auto --ideate --ideate-paths="src/,packages/web/" --project $REPO

# Quick mode: copilot only (no codex)
agents auto --quick --project $REPO

# Thorough mode: codex only
agents auto --thorough --limit=1 --project $REPO
```

### CLI capabilities

| flag | what it does |
|------|--------------|
| `--ideate` | LLM analyzes git trajectory + codebase → synthesizes work items |
| `--preview` | Creates git worktree + dev server + ngrok tunnel per work item |
| `--ideate-paths` | Focus ideation on specific directories |
| `--ideate-days` | Git history lookback (default: 14 days) |
| `--quick` | Route to copilot WITH commit authority (quick implementation) |
| `--quick-think` | Route to copilot WITHOUT commits (thinking only) |
| `--thorough` | Route all work to codex (commits + push) |
| `--limit N` | Cap spawned agents |
| `--dry-run` | Plan without executing |

**Quick mode distinction:**
- `--quick` = quick **implementation** → copilot writes code, verifies, commits
- `--quick-think` = quick **thinking** → copilot analyzes, plans, recommends (no commits)

## decision tree: work discovery

```
Where does work come from?
├── Linear team (from .loop.json)
│   ├── Ready issues (prioritized)
│   ├── In Progress (check for stale)
│   └── Blocked (surface for HIL)
├── CLAUDE.md TODOs
│   ├── grep -E "TODO|FIXME|HACK" in docs
│   └── Parse actionable items
├── Git status
│   ├── Uncommitted changes (finish or discard?)
│   ├── Stale branches (>7 days no commit)
│   └── Unmerged PRs
└── Git log (LEARNING SOURCE)
    ├── Quality bar: what do good commits look like?
    ├── Trajectory: what areas are hot?
    ├── Patterns: how did we solve similar problems?
    └── Velocity: how fast do we ship?
```

## decision tree: agent selection

```
Who does this work?
├── Thinking work (copilot, NO commits)
│   ├── Planning: "what should we prioritize?"
│   ├── Analysis: "what patterns exist in git log?"
│   ├── Review: "is this implementation good?"
│   ├── Group decision: multiple models weigh in
│   └── Prompt crafting: build perfect codex prompt
│
├── Quick implementation (copilot, WITH commits)
│   ├── Scope: < 3 files, low complexity
│   ├── Examples: add function, fix typo, update config
│   ├── Executes: write code, run verification, COMMIT
│   ├── Authority: commit only, report push-ready (no push)
│   └── Output contract: must include `commits` field
│
└── Thorough implementation (codex, commits + push)
    ├── Scope: 3+ files, high complexity, architectural
    ├── Receives: fully resolved prompt (ambiguity pre-resolved)
    ├── Executes: TDD cycle, verification, commit, PUSH
    └── Returns: structured output contract with `pushed: true`
```

**CRITICAL: The Consultant Trap**

When routing quick implementation to copilot, the prompt MUST:
1. Include commit instructions (not just "recommend changes")
2. Request `commits` field in output contract
3. Specify verification commands to run before commit

```bash
# BAD: Consultant Trap - copilot advises but doesn't commit
<output_contract>{"type": "recommendation", ...}</output_contract>

# GOOD: Quick implementation - copilot implements AND commits
<output_contract>{"commits": [{"hash": "...", "msg": "..."}], ...}</output_contract>
```

## decision tree: copilot model selection

```
Which model for this thinking task?
├── Quick synthesis / progress check
│   └── gemini-3-pro (fast, cheap)
├── Deep analysis / pattern extraction
│   └── gemini-3-ultra (thorough, moderate)
├── Nuanced review / quality assessment
│   └── sonnet-4 (balanced, good judgment)
├── Complex architecture / trade-offs
│   └── sonnet-4-thinking (extended reasoning)
└── Group decision (multiple perspectives)
    └── parallel: gemini-3-pro + sonnet-4 + gemini-3-ultra
```

## workflow

### orchestration (skill level)

When invoked, the skill decides which mode to use:

```
How should auto run?
├── User says "ideate" or "discover work"?
│   └── agents auto --ideate --preview
├── User says "quick pass" or time-constrained?
│   └── agents auto --quick --limit=3
├── Specific Linear issue mentioned?
│   └── agents auto --issue=$ISSUE --thorough
├── User says "autonomous" or "deep work"?
│   └── agents auto --ideate --preview --limit=5
└── Default exploration
    └── agents auto --ideate --dry-run (show plan first)
```

### execution (CLI level)

The CLI handles all the infrastructure:

```bash
# 1. Session management (automatic)
# CLI creates session, registers heartbeats, manages lifecycle

# 2. Work discovery
# --ideate triggers: git trajectory analysis + codebase signals → LLM synthesis
# Without --ideate: Linear issues + TODOs + git status

# 3. Agent routing
# Triage classifies each work item as quick or thorough
# quick → copilot, thorough → codex

# 4. Preview pipeline (with --preview)
# For each work item:
#   - Creates git worktree (isolated branch)
#   - Starts dev server on unique port
#   - Opens ngrok tunnel for live preview
#   - Agent prompt includes preview URL

# 5. Spawn with output contracts
# Prompts include verification commands and JSON output schema
# Response captured via -o flag (not TaskOutput)

# 6. Resource management
# ResourceManager prevents API contention
# Leases with TTL, automatic cleanup
```

### manual intervention points

When to use skill judgment vs CLI automation:

```
├── Ideation returns 0 items?
│   └── Skill asks: "No work found. Should I look deeper or is repo stable?"
├── All items classified as 'thorough'?
│   └── Skill confirms: "These are complex. Spawn codex for each?"
├── Preview tunnel fails?
│   └── Skill continues without preview, notes in output
├── Codex returns low confidence?
│   └── Skill escalates to copilot review or HIL
└── Multiple repos need coordination?
    └── Skill suggests: "Use loop skill for cross-repo work"
```

### copilot swarm (thinking layer)

For complex decisions, spawn parallel copilots via session management:

**RECOMMENDED: session spawning** (tracked, structured output):

```bash
# Build context from CLI output
DISCOVERY=$(agents auto --ideate --dry-run --json --project $REPO)

# Prepare swarm prompts
echo "$DISCOVERY" > /tmp/discovery.json

cat > /tmp/priority.md << 'EOF'
Prioritize by urgency.
<output_contract>{"order": [], "rationale": ""}</output_contract>
EOF

cat > /tmp/risk.md << 'EOF'
Assess risk and dependencies.
<output_contract>{"risks": [], "safe_first": ""}</output_contract>
EOF

cat > /tmp/synthesis.md << 'EOF'
Synthesize optimal execution plan.
<output_contract>{"plan": "", "confidence": 0}</output_contract>
EOF

# Generate parent ID for this swarm
SWARM_ID="swarm-$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 4)"

# Spawn parallel sessions with --await (all run simultaneously in background)
(
  R1=$(cat /tmp/discovery.json /tmp/priority.md | agents session start -a copilot -p $PROJECT \
    -g "priority analysis" --parent "$SWARM_ID" --timeout 120 --await --json -q)
  echo "$R1" > /tmp/result-priority.json
) &
(
  R2=$(cat /tmp/discovery.json /tmp/risk.md | agents session start -a copilot -p $PROJECT \
    -g "risk analysis" --parent "$SWARM_ID" --timeout 120 --await --json -q)
  echo "$R2" > /tmp/result-risk.json
) &
(
  R3=$(cat /tmp/discovery.json /tmp/synthesis.md | agents session start -a copilot -p $PROJECT \
    -g "synthesis" --parent "$SWARM_ID" --timeout 120 --await --json -q)
  echo "$R3" > /tmp/result-synthesis.json
) &

# Wait for all background jobs
wait

# Extract outputs (--await returns inline)
PRIORITY=$(cat /tmp/result-priority.json | jq -r '.await.output')
RISK=$(cat /tmp/result-risk.json | jq -r '.await.output')
SYNTHESIS=$(cat /tmp/result-synthesis.json | jq -r '.await.output')

# Then spawn via CLI with informed plan
agents auto --ideate --preview --limit=3 --project $REPO
```

**Alternative: direct CLI** (one-off, background jobs):

```bash
cat /tmp/discovery.json /tmp/priority.md | copilot --model gemini-3-pro-preview --silent > /tmp/priority-result.txt &
wait
```

### post-execution (notifications)

**RECOMMENDED: `agents report`** (unified trails + slack + optional DM):

```bash
# Start trace at auto session begin
export AGENTS_TRACE_ID=$(agents report start "auto: $PROJECT" --agent claude --json -q | jq -r '.traceId')

# Progress on ideation complete
agents report progress "ideation: found $COUNT work items" --confidence 8

# Progress on execution phases
agents report progress "executed 2/3 tasks" --confidence 7

# Complete with summary (gist creates permanent artifact)
agents report complete "3 tasks executed via auto - 2 from git trajectory, 1 from Linear" --confidence 9 --dm --gist

# Or if blocked
agents report blocked "codex returned low confidence on complex refactor" --blocker-type error
```

**Alternative: direct slack** (custom formatting):

```bash
slack agent post --agent claude --channel agents --text "session complete: 3 tasks executed via auto" -w saya
```

## concrete values

| metric | value | source |
|--------|-------|--------|
| copilot quick timeout | 30s | gemini-3-pro typical |
| copilot thorough timeout | 120s | gemini-3-ultra typical |
| codex timeout | 600s (10 min) | complex task estimate |
| heartbeat interval | 60s | agents CLI default |
| stale session threshold | 5 min | agents CLI default |
| codex slots | 3 concurrent | ResourceManager default |
| copilot slots | 5 concurrent | ResourceManager default |

## tool integration

### agents CLI (primary interface)

```bash
# Auto command (this skill's main tool)
agents auto --ideate --preview --project $REPO    # full autonomous mode
agents auto --ideate --dry-run --json             # plan only, structured output
agents auto --quick --limit=3                     # fast pass, copilot only
agents auto --thorough --issue=ARB-123            # deep work, specific issue

# Session management (handled by auto internally)
agents session create --project $REPO --agent claude
agents session heartbeat $SESSION_ID --task "description"
agents session complete $SESSION_ID --summary "..."

# Resource management (handled by auto internally)
agents resource acquire codex_api $SESSION_ID
agents resource release codex_api $SESSION_ID
```

### copilot (thinking layer)

**RECOMMENDED: session spawning** (tracked, managed):

```bash
# Quick synthesis via session with --await
RESULT=$(cat /tmp/prompt.md | agents session start -a copilot -p $PROJECT \
  -g "synthesis" \
  --parent "$AGENTS_TRACE_ID" \
  --timeout 120 \
  --await \
  --json -q)

# Extract from await response
STATUS=$(echo "$RESULT" | jq -r '.await.status')
OUTPUT=$(echo "$RESULT" | jq -r '.await.output')
```

**Alternative: direct CLI** (quick one-offs):

```bash
cat <<'EOF' | copilot --model gemini-3-pro-preview --silent 2>&1 | head -1
prompt text here
EOF
```

### codex (implementation layer)

**RECOMMENDED: session spawning** (tracked, with --await):

```bash
# Spawn codex session with --await (longer timeout for codex)
RESULT=$(cat /tmp/prompt.md | agents session start -a codex -p $PROJECT \
  -g "$TASK" \
  --parent "$AGENTS_TRACE_ID" \
  --timeout 600 \
  --await \
  --json -q)

# Extract from await response
STATUS=$(echo "$RESULT" | jq -r '.await.status')
OUTPUT=$(echo "$RESULT" | jq -r '.await.output')
```

**Alternative: direct CLI** (with -o flag):

```bash
# CRITICAL: Always use -o for structured capture
cat prompt.md | codex exec - --full-auto -o /tmp/response.json --json

# NEVER use TaskOutput - destroys context
# Poll for file, then Read directly
```

### supporting CLIs

```bash
# Linear
linear issue list --team $TEAM --state "Ready" --json --quiet
linear issue edit $ISSUE_ID --state "In Progress"

# Slack
slack agent post --agent claude --channel agents --text "..." -w saya

# Verification
verify --format=summary
pnpm typecheck
```

## coordination (global)

Even with single-repo context, agents coordinate globally:

```
~/.agents/
├── events/           # EventStore (append-only logs)
│   ├── arbor/events.jsonl
│   ├── kumori/events.jsonl
│   └── ...
├── sessions/         # HeartbeatManager (liveness)
│   ├── arbor/session-id.json
│   └── ...
└── resources/        # ResourceManager (semaphores)
    ├── codex_api/lease-id.json
    ├── copilot_api/lease-id.json
    └── ...
```

Multiple auto sessions (different terminals) see each other via:
- Slack #agents posts
- Shared EventStore
- ResourceManager preventing API contention

## git log learning patterns

The key insight: git log isn't just status, it's a teacher.

```bash
# Quality bar: what coverage do we maintain?
git log --stat -20 | grep -E "test.*\+" | wc -l

# Trajectory: what files are hot?
git log --name-only -50 | sort | uniq -c | sort -rn | head -10

# Patterns: how did we solve auth before?
git log --all --oneline --grep="auth" | head -10

# Commit style: what do good messages look like?
git log --format="%s" -20

# Velocity: how many commits per day?
git log --since="7 days ago" --oneline | wc -l
```

copilot extracts these patterns and bakes them into codex prompts.

## relationship to other skills

### auto vs loop

| aspect | auto | loop |
|--------|------|------|
| scope | single repo, single session | multi-repo, multi-hour |
| bootstrapping | requires context (cwd, project) | zero-context self-bootstrap |
| invocation | `agents auto --ideate` | user says "work autonomously" |
| duration | minutes to ~1 hour | hours to overnight |
| platform awareness | generic | flywheels (xcode, web, convex) |

**composition**: loop skill can invoke auto skill for per-repo execution within a multi-repo session.

```
loop (orchestrates across repos)
  → auto (executes in arbor)
  → auto (executes in kumori)
  → synthesizes results
```

### auto vs pair

| aspect | auto | pair |
|--------|------|------|
| purpose | discover and execute work | consult/delegate/review |
| work source | ideation + Linear + git | user provides task |
| output | completed tasks | structured JSON response |

**composition**: auto uses pair-like patterns internally (copilot for thinking, codex for doing).

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| TaskOutput for codex | pulls 10K+ tokens, destroys context | use -o flag + Read file |
| vague codex prompts | codex can't ask questions | resolve all ambiguity with copilot first |
| skipping verification | vibes-based "it works" | always run all 4 gates |
| ignoring git log | miss quality patterns | treat history as learning source |
| single model thinking | limited perspective | use copilot swarm (multiple models) |
| fire-and-forget spawning | no visibility | heartbeats + Slack posts |
| manual bash in skill | duplicates CLI capabilities | invoke `agents auto` with flags |
| conflating skill with CLI | unclear responsibilities | skill orchestrates, CLI executes |
| **Consultant Trap** | copilot advises but doesn't commit | use `--quick` not `--quick-think` for implementation; require `commits` field in output contract |
| routing quick to thinking | simple tasks get analysis instead of execution | distinguish `--quick` (implementation) from `--quick-think` (analysis) |

## references

- [references/discovery-patterns.md](references/discovery-patterns.md) - work source extraction
- [references/prompt-templates.md](references/prompt-templates.md) - codex prompt structures
- [references/verification-cascade.md](references/verification-cascade.md) - gate definitions
- `~/Developer/utils/agents/src/lib/auto/` - CLI implementation
- `~/Developer/utils/agents/src/cli/commands/auto/` - CLI command
