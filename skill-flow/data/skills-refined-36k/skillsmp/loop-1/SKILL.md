---
name: loop
description: This skill should be used for autonomous work on complex tasks with ZERO context required. Triggers include "start a loop", "work autonomously", "before I sleep", "take this and run with it", or when claude detects a task requiring sustained focus. Self-bootstraps project type, trajectory, and standards. No hard dependencies.
---

# loop

zero-context autonomous work orchestrator. self-bootstraps project type, trajectory, and coding standards. works in ANY repo without prior setup.

## philosophy

> "work until blocked, then tell me why"

| principle | application |
|-----------|-------------|
| zero-context | works in fresh clone with no prior knowledge |
| self-bootstrapping | detects project type, patterns, trajectory |
| autonomous by default | proceed without asking unless truly blocked |
| platform-aware | detect project type, use appropriate flywheel |
| quality-gated | tests pass, types check, build succeeds |
| graceful degradation | works without optional CLIs (layer, outline, linear) |
| pair-backed | use pair skill for external AI decisions |

## when to use

| use | skip |
|-----|------|
| autonomous work on complex tasks | quick one-off fixes |
| fresh repo with no context | simple questions |
| "before I sleep" long runs | pure research (use fanout skill) |
| multi-step implementations | ambiguous tasks needing clarification first |
| any platform/language | fire-and-forget delegation (use pair skill) |

## decision tree: mode selection

```
What mode should I use?
├── Linear issue provided/detected?
│   ├── Issue ID in prompt → issue-mode
│   ├── git branch matches issue pattern → issue-mode
│   └── Path matches workspace → check for in-progress issues
├── Fresh repo with no context?
│   ├── No .loop.json → bootstrap-mode (Phase 0 first)
│   ├── .loop.json exists → task-mode with config
│   └── README/CONTRIBUTING exists → read first
├── Arbitrary task?
│   └── task-mode (pure autonomous execution)
└── Unclear?
    └── bootstrap-mode to gather context
```

## decision tree: flywheel selection

```
Which flywheel applies?
├── .xcodeproj or .xcworkspace present?
│   └── flywheel-xcode (iOS/macOS build-test)
├── package.json + playwright?
│   └── flywheel-web (E2E with Playwright)
├── convex/ directory present?
│   └── flywheel-convex (backend TDD)
├── Cargo.toml present?
│   └── cargo test cycle
├── go.mod present?
│   └── go test cycle
├── pyproject.toml present?
│   └── pytest cycle
└── Unknown project type?
    └── generic test-change-test cycle
```

## decision tree: pair routing

```
When to consult external agent?
├── Pre-flight (before starting work)?
│   ├── Complex architecture → pair thorough
│   └── Standard implementation → pair quick
├── Mid-work decision?
│   ├── Blocking issue → pair quick first
│   │   └── Confidence < 7 → auto-escalate to thorough
│   ├── Multiple valid approaches → pair thorough
│   └── Simple question → pair quick
├── Review (after work)?
│   ├── First-pass → pair quick (review mode)
│   ├── Issues found → pair thorough
│   └── PR ready → pair thorough (final review)
└── Truly blocked?
    └── HIL via AskUserQuestion
```

## decision tree: strategic check-ins

```
Should I check in with user?
├── Architectural decisions with trade-offs?
│   └── YES - let user choose direction
├── Ambiguous requirements discovered?
│   └── YES - clarify before proceeding
├── Approaches with real costs (complexity, perf, DX)?
│   └── YES - get sign-off
├── Blockers needing human context?
│   └── YES - user may have info I don't
├── Implementation details?
│   └── NO - proceed autonomously
├── Obvious choices?
│   └── NO - just do it
└── Things I can decide and document?
    └── NO - decide, document, continue
```

## decision tree: verification scope

```
What verification should I run?
├── touching auth, data, infra, or core logic?
│   └── full verify: tests + lint + typecheck + build
├── config or tooling change?
│   └── full verify + restart tooling
├── UI-only or copy-only?
│   └── targeted tests or smoke + lint
├── docs-only?
│   └── skip tests, note not run
└── unsure?
    └── full verify
```

## concrete values (sourced)

| value | meaning | source |
|-------|---------|--------|
| pattern freshness window: < 7 days | treat patterns as fresh; skip rediscovery | `scripts/bootstrap-with-patterns.sh` |
| repo trajectory sample: last 10 commits | quick recent history scan | `scripts/bootstrap-with-patterns.sh` |
| hotspot window: last 20 commits | file hotspot sampling | `scripts/bootstrap-with-patterns.sh` |
| README gate: first 50 lines | initial project intent scan | `scripts/bootstrap-with-patterns.sh` |
| contributing gate: first 30 lines | contributor rules scan | `scripts/bootstrap-with-patterns.sh` |
| consult-light proceed threshold: confidence >= 8 | safe to proceed after quick review | `references/agentic-review.md` |
| consult-light escalate threshold: confidence < 7 | escalate to consult-deep | `references/agentic-review.md` |

## modes

| context | mode | behavior |
|---------|------|----------|
| Linear issue provided/detected | issue-mode | sync with Linear, update status |
| arbitrary task | task-mode | pure autonomous execution |
| fresh repo, no context | bootstrap-mode | Phase 0 first, then task-mode |

## workflow

### phase 0: bootstrap (zero-context)

self-bootstrap when entering unfamiliar repo:

```bash
#!/usr/bin/env bash
# Zero-context bootstrap - NO external CLI deps
# Enhanced with cross-project pattern discovery for Convex projects

echo "=== Project Detection ==="
PROJECT_TYPE="unknown"
[ -f "package.json" ] && PROJECT_TYPE="node"
[ -f "Cargo.toml" ] && PROJECT_TYPE="rust"
[ -f "pyproject.toml" ] && PROJECT_TYPE="python"
[ -f "go.mod" ] && PROJECT_TYPE="go"
{ ls -d *.xcodeproj *.xcworkspace 2>/dev/null | head -1 >/dev/null; } && PROJECT_TYPE="xcode"
[ -d "convex" ] && PROJECT_TYPE="convex"
echo "Project type: $PROJECT_TYPE"

# Pattern Discovery for Convex projects (graceful - never blocks)
if [[ "$PROJECT_TYPE" == "convex" ]]; then
  PATTERNS_DIR="${PATTERNS_DIR:-$HOME/.loop/patterns}"
  
  echo "=== Pattern Discovery Check ==="
  if [[ -d "$PATTERNS_DIR" ]]; then
    # Check pattern freshness (< 7 days)
    pattern_files=$(find "$PATTERNS_DIR" -name "*.md" -mtime -7 2>/dev/null | wc -l | tr -d ' ')
    if [[ $pattern_files -gt 0 ]]; then
      echo "✅ Fresh patterns available from mature projects"
      echo "Patterns: $(ls -1 "$PATTERNS_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ') types"
      
      # Show quick pattern summary
      [[ -f "$PATTERNS_DIR/commit-style.md" ]] && {
        echo ""
        echo "💬 Commit Style (from your mature projects):"
        grep -A 5 "#### Lowercase Style" "$PATTERNS_DIR/commit-style.md" | grep -v "^#" | head -4
      }
    else
      echo "⏰ Patterns stale, will refresh in background"
    fi
  else
    echo "📋 First run: discovering patterns from your Convex projects..."
    echo "Run: ~/Developer/skills/skills/loop/scripts/discover-projects.sh"
  fi
  echo ""
fi

# Optional: Full project alignment audit (invoke project-audit skill)
# For unfamiliar projects, consider running project-audit to surface:
# - Pattern gaps vs arbor/koto/kumori
# - Underutilized tool features (outline --unused, layer --check-cycles)
# - Org standards deviations

echo "=== Monorepo Detection ==="
[ -f "pnpm-workspace.yaml" ] && echo "Monorepo: pnpm workspaces"
[ -f "turbo.json" ] && echo "Monorepo: turborepo"
[ -f "nx.json" ] && echo "Monorepo: nx"
[ -f "lerna.json" ] && echo "Monorepo: lerna"

echo "=== Test Runner Discovery ==="
[ -f "package.json" ] && grep -qE "vitest|jest|mocha" package.json 2>/dev/null && echo "Test: vitest/jest/mocha"
[ -f "pyproject.toml" ] && grep -q "pytest" pyproject.toml 2>/dev/null && echo "Test: pytest"
[ -f "Cargo.toml" ] && echo "Test: cargo test"
[ -f "go.mod" ] && echo "Test: go test"

echo "=== Lint/Format Discovery ==="
ls .eslintrc* eslint.config.* 2>/dev/null && echo "Lint: eslint"
ls .prettierrc* prettier.config.* 2>/dev/null && echo "Format: prettier"
[ -f "biome.json" ] && echo "Lint/Format: biome"
ls .ruff.toml ruff.toml 2>/dev/null && echo "Lint: ruff"

echo "=== Personal Trajectory ==="
git log --author="$(git config user.name)" --oneline -10 2>/dev/null || echo "No personal commits"
git log --author="$(git config user.name)" --since=2.weeks --oneline 2>/dev/null | head -20

echo "=== Repo Trajectory ==="
git log --oneline -10 2>/dev/null
echo "File hotspots:"
git log -n 20 --name-only --format="" 2>/dev/null | sort | uniq -c | sort -rn | head -10

echo "=== Work In Progress ==="
git status --short 2>/dev/null
git branch --list 2>/dev/null | grep -iE "wip|feature|fix"
git stash list 2>/dev/null | head -5

echo "=== Code Style Patterns ==="
# Try rg, fall back to grep
if command -v rg &>/dev/null; then
  rg -n "^(export|class|interface|type|function|const) " --type ts 2>/dev/null | head -10
else
  grep -rn "^export\|^class\|^function" --include="*.ts" . 2>/dev/null | head -10
fi

echo "=== Test Conventions ==="
find . -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | head -10

echo "=== Import Patterns ==="
if command -v rg &>/dev/null; then
  rg -n "^import " --type ts 2>/dev/null | head -10
else
  grep -rn "^import" --include="*.ts" . 2>/dev/null | head -10
fi

echo "=== README Gate ==="
[ -f "README.md" ] && head -50 README.md
[ -f "CONTRIBUTING.md" ] && head -30 CONTRIBUTING.md

# Pattern Reference (if available)
if [[ "$PROJECT_TYPE" == "convex" ]] && [[ -d "$PATTERNS_DIR" ]]; then
  echo ""
  echo "=== Pattern Reference ==="
  echo "Available patterns from mature projects:"
  ls -1 "$PATTERNS_DIR"/*.md 2>/dev/null | xargs -n1 basename | sed 's/\.md$//' || echo "None yet"
  echo "View: cat ~/.loop/patterns/<pattern>.md"
fi
```

**optional config**: `.loop.json` (if present, skip detection):

```json
{
  "project_type": "convex",
  "test_command": "pnpm test",
  "build_command": "pnpm build",
  "lint_command": "pnpm lint"
}
```

### phase 1: context gathering

```bash
# understand architecture (graceful - use layer if available)
if command -v layer &>/dev/null; then
  layer .
else
  # fallback: directory structure
  find . -name "package.json" -exec dirname {} \; 2>/dev/null | head -20
  ls -la
fi

# code structure (graceful - use outline if available)
if command -v outline &>/dev/null; then
  fd -e ts . src 2>/dev/null | outline -c --stats
else
  # fallback: grep for exports
  grep -rn "^export" --include="*.ts" . 2>/dev/null | head -20
fi

# recent activity (git-native, always works)
git log --oneline -10 2>/dev/null
git diff --stat HEAD~3 2>/dev/null

# Linear sync (graceful - use linear if available)
if command -v linear &>/dev/null && [ -n "$ISSUE_ID" ]; then
  linear issue view $ISSUE_ID --json --quiet
fi
```

**documentation grounding** (always):

```bash
ref_search_documentation "{framework} {feature} guide"
ref_read_url "https://docs.example.com/path#section"
```

### phase 2: plan + track

```bash
# create plan
agents plan --project {name} --title "{task}" --json --quiet

# initialize TodoWrite with phases
```

phases:
1. exploration + understanding
2. test scaffolding (when applicable)
3. implementation
4. verification
5. cleanup

### phase 3: pair preflight

use pair skill with `consult-light` mode for quick sanity check:

**RECOMMENDED: Session spawning with --await and lifecycle reporting**

```bash
# Start loop trace (all subsequent events correlate)
export AGENTS_TRACE_ID=$(agents report start "loop: $TASK_SUMMARY" --agent claude --json -q | jq -r '.traceId')

# Build preflight prompt
cat > /tmp/preflight.md << 'PROMPT'
Context synthesis.

Issue/Task: {description}
Project: {PROJECT_TYPE from bootstrap}
Recent work: {trajectory summary}
Code patterns: {patterns from bootstrap}

Question: What's the recommended approach?
Output JSON: {"approach":"...", "files_to_modify":[], "risks":[], "confidence":1-10, "escalate":false}
PROMPT

# Spawn copilot session with --await (blocks until done)
RESULT=$(cat /tmp/preflight.md | agents session start -a copilot -p $PROJECT \
  -g "preflight: $TASK" \
  --parent "$AGENTS_TRACE_ID" \
  --timeout 120 \
  --await \
  --json -q)

# Extract preflight response from await output
PREFLIGHT=$(echo "$RESULT" | jq -r '.await.output')
STATUS=$(echo "$RESULT" | jq -r '.await.status')

# Check status before using
if [ "$STATUS" != "completed" ]; then
  echo "Preflight failed: $STATUS"
fi
```

**Alternative: Direct CLI (for quick one-off checks)**

```bash
PREFLIGHT=$(cat <<'EOF' | copilot --model gemini-3-pro-preview --silent 2>&1 | head -1
Context synthesis.

Issue/Task: {description}
Project: {PROJECT_TYPE from bootstrap}
Recent work: {trajectory summary}
Code patterns: {patterns from bootstrap}

Question: What's the recommended approach?
Output JSON: {"approach":"...", "files_to_modify":[], "risks":[], "confidence":1-10, "escalate":false}
EOF
)
```

if confidence >= 7, proceed. if < 7, escalate to codex (consult-deep) or HIL.

### phase 4: execute flywheel

the core loop: **scope → test → change → test → verify**

```
while not done:
  1. scope next piece (smallest valuable increment)
  2. write/update tests (when applicable)
  3. implement change
  4. run tests (verify --format=summary)
  5. commit if green
  6. update TodoWrite progress
  7. check: decision needed? → consult or ask user
```

**platform flywheels**:

| signal | type | flywheel |
|--------|------|----------|
| .xcodeproj, .xcworkspace | xcode | flywheel-xcode |
| package.json + playwright | web | flywheel-web |
| convex/ directory | convex | flywheel-convex |

### phase 5: strategic check-ins

**check in with user for**:
- architectural decisions with trade-offs
- ambiguous requirements discovered mid-work
- approaches with real costs (complexity, performance, DX)
- blockers that need human context

**don't check in for**:
- implementation details
- obvious choices
- things you can decide and document

### phase 6: quality gate

before agentic review:

```bash
# code verification
verify --format=summary
pnpm lint
pnpm build
pnpm typecheck

# review changes
git diff --stat HEAD~N
outline --diff=HEAD~N
```

**quality bar**:
- [ ] all tests pass
- [ ] no lint errors
- [ ] build succeeds
- [ ] types check
- [ ] commits are atomic and well-messaged
- [ ] code matches patterns from codebase

### phase 7: pair review

external AI validation before declaring done (via pair skill, review mode).

**step 1: pair quick review**

**RECOMMENDED: session spawning** (unified, tracked, output contracts):

```bash
# Prepare review prompt
cat > /tmp/review-prompt.md << 'PROMPT'
Work review.

Task: {description}
Work done: {summary}
Artifacts: {file_list}
Tests: {test_status}

Validate:
1. Requirements met?
2. Tests adequate?
3. Patterns followed?

<output_contract>
Respond with ONLY this JSON:
{"pass": bool, "issues": [], "confidence": 0-10, "escalate": bool}
</output_contract>
PROMPT

# Spawn copilot session for quick review with --await
RESULT=$(cat /tmp/review-prompt.md | agents session start -a copilot -p $PROJECT \
  -g "review: $TASK" \
  --parent "$AGENTS_TRACE_ID" \
  --timeout 120 \
  --await \
  --json -q)

# Extract result from await response
STATUS=$(echo "$RESULT" | jq -r '.await.status')
REVIEW=$(echo "$RESULT" | jq -r '.await.output')

# Handle timeout/failure
if [ "$STATUS" != "completed" ]; then
  agents report progress "quick review: $STATUS - proceeding with caution"
else
  agents report progress "quick review: confidence $(echo $REVIEW | jq -r '.confidence')"
fi
```

**Alternative: direct CLI** (quick one-offs, no session overhead):

```bash
cat <<'EOF' | copilot --model gemini-3-pro-preview --silent 2>&1 | head -1
Work review...
EOF
```

**routing** (handled by pair skill):

| confidence | action |
|------------|--------|
| >= 8 | proceed to completion |
| 5-7 | escalate to codex (automatic) |
| < 5 | iterate, don't proceed |

**step 2: pair deep review (if escalated)**

**RECOMMENDED: session spawning** (tracked, output file):

```bash
# Spawn codex session for deep review
cat > /tmp/deep-review-prompt.md << 'PROMPT'
Deep review.

Task: {description}
Work done: {summary}
Quick review: {copilot_assessment}

<output_contract>
Respond with ONLY this JSON:
{"status": "ready|needs_work|blocked", "missing": [], "recommendation": "...", "confidence": 0-10}
</output_contract>
PROMPT

# Spawn codex session for deep review with --await (longer timeout for codex)
RESULT=$(cat /tmp/deep-review-prompt.md | agents session start -a codex -p $PROJECT \
  -g "deep-review: $TASK" \
  --parent "$AGENTS_TRACE_ID" \
  --timeout 300 \
  --await \
  --json -q)

# Extract result from await response
STATUS=$(echo "$RESULT" | jq -r '.await.status')
DEEP_REVIEW=$(echo "$RESULT" | jq -r '.await.output')

# Handle timeout/failure
if [ "$STATUS" != "completed" ]; then
  agents report progress "deep review: $STATUS - manual review needed"
else
  agents report progress "deep review: $(echo $DEEP_REVIEW | jq -r '.status')"
fi
```

**Alternative: direct CLI** (one-off, raw output):

```bash
codex exec --model gpt-5.2-codex xhigh --approval-mode xhigh "Deep review..."
```

### completion

```
completed:
- [list of what was done]

verification:
- tests: ✅ passing
- lint: ✅ clean
- build: ✅ success
- types: ✅ clean

commits:
- [commit list]

ready for review. anything else?
```

## Linear integration

when in issue-mode:

| path pattern | workspace | default team |
|--------------|-----------|--------------|
| ~/Developer/arbor/* | luke-labs | ARB |
| ~/Developer/ascii/* | luke-labs | ASC |
| ~/Developer/koto/* | luke-labs | KOT |
| ~/Developer/kumori/* | luke-labs | KUM |
| ~/Developer/sine/* | luke-labs | SIN |
| ~/Developer/webs/* | luke-labs | WEB |
| */spottedinprod/* | spottedinprod | SIP |

```bash
# issue selection priority
# 1. in-progress issues assigned to me
# 2. highest priority unassigned in current sprint
# 3. backlog by priority

linear issue list --team $TEAM --state "In Progress" --assignee luke --json --quiet
```

## pair skill integration

| mode | when | agent |
|------|------|-------|
| consult quick | progress checks, quick decisions | copilot (gemini-3-pro) |
| consult thorough | architectural, blocking | codex (gpt-5.2-max) |
| review | code work validation, final review | auto-routed |
| implement | delegate heavy coding | codex for 10+ min tasks |
| HIL | truly blocked, scope questions | AskUserQuestion |

**references**:
- `@skills/pair` - unified external AI collaboration
- `@rules/copilot.md` - copilot syntax, models
- `@rules/codex.md` - codex exec syntax, monitoring

## confidence routing (loop-level)

| confidence | action | note |
|------------|--------|------|
| 9-10 | proceed and finalize | document caveats if any |
| 7-8 | proceed with caution | note follow-ups or gaps |
| 5-6 | pair quick, then decide | escalate to thorough if still unsure |
| 1-4 | pause and ask user | or HIL if blocked |

## progress tracking

three layers of persistence:

| layer | purpose | artifact |
|-------|---------|----------|
| agents CLI | plan + artifacts | `~/.agents/plans/{project}/{date}-{slug}/` |
| TodoWrite | in-session visibility | todo list in UI |
| git commits | permanent progress | atomic commits |

## failure modes

| failure mode | signal | mitigation | escalation |
|--------------|--------|------------|------------|
| missing tooling (layer/outline/linear) | command not found | use fallback commands, note missing tools | none |
| project type mis-detected | `PROJECT_TYPE=unknown` but repo is obvious | read README, set `.loop.json` override | ask user if still unclear |
| stale or missing patterns | bootstrap reports stale/missing patterns | run discovery scripts, proceed without patterns | check in if pattern alignment matters |
| flaky tests | fail then pass on rerun | isolate test, rerun targeted, document flake | check in if fix changes behavior |
| invalid external agent output | JSON parse fails or keys missing | retry with JSON-only prompt, switch model | HIL if still invalid |
| verification hangs | command stalls or times out | narrow scope, run targeted tests | ask user if full verify can't complete |

## decision tree: failure handling

```
What failed?
├── tests failing?
│   └── run verify --json --failures-only, trace callers, check design ambiguity
├── type errors?
│   └── run typecheck, find type root, avoid casts; check in if API change
├── lint or build errors?
│   └── fix config/deps first; if new deps needed -> check in
├── runtime error?
│   └── reproduce, add logging, check external deps
└── blocked?
    └── pair quick -> pair thorough -> HIL
```

## error handling

1. **test failure**: investigate root cause, don't just fix symptoms
2. **type error**: trace to source, may reveal design issue
3. **lint error**: auto-fix when possible, align with repo patterns
4. **build failure**: check deps and config before code changes
5. **runtime error**: reproduce, add logging, isolate external deps
6. **blocked**: pair quick first, then pair thorough, then HIL

see `references/error-handling.md` for investigation flows and prompts.

## tool integration

| tool | command | purpose |
|------|---------|---------|
| layer | `layer .`, `layer . --check-cycles` | architecture understanding, cycle detection |
| outline | `outline -c --stats`, `outline --diff=HEAD~N` | code structure, structural changes |
| verify | `verify --format=summary` | test execution, quality gate |
| git | `git log`, `git diff --stat` | trajectory, progress tracking |
| linear | `linear issue view`, `linear issue list` | issue sync (issue-mode) |
| agents | `agents session start --await`, `agents report`, `agents plan` | session spawning, lifecycle reporting, planning |
| trails | via `agents report` | persistence, trace correlation |
| slack | via `agents report` | lifecycle notifications |
| copilot | via pair skill | quick consults, preflight checks |
| codex | via pair skill | deep review, heavy implementation |

### trails integration

loop uses `agents report` which handles trails internally:

```bash
# Start trace (new loop run)
export AGENTS_TRACE_ID=$(agents report start "loop: $PROJECT" --agent claude --json -q | jq -r '.traceId')

# Progress updates (trace inherited from env)
agents report progress "phase 4: flywheel iteration 3/5" --confidence 7

# Completion (gist creates permanent handoff artifact)
agents report complete "implemented $FEATURE" --confidence 9 --dm --gist

# Query loop history
trails trail replay --trace-id $AGENTS_TRACE_ID --format summary
```

**trails enables**:
- correlating all loop events (preflight, flywheel iterations, review)
- tracking loop patterns over time
- measuring loop success rates and duration
- linking loop runs to Linear issues

## references

### flywheels
- [references/flywheel-xcode.md](references/flywheel-xcode.md) - iOS/macOS build-test loop
- [references/flywheel-web.md](references/flywheel-web.md) - Web E2E with Playwright
- [references/flywheel-convex.md](references/flywheel-convex.md) - Convex backend TDD
- [references/flywheel-patterns.md](references/flywheel-patterns.md) - scope/test/change/verify

### TDD
- [references/tdd-workflow.md](references/tdd-workflow.md) - red-green-refactor philosophy
- [references/vitest-config.md](references/vitest-config.md) - vitest configuration
- [references/convex-testing.md](references/convex-testing.md) - convex-test patterns
- [references/react-testing.md](references/react-testing.md) - react testing library
- [references/playwright.md](references/playwright.md) - E2E with Playwright

### pattern discovery
- [references/pattern-discovery.md](references/pattern-discovery.md) - cross-project pattern extraction

### integration
- [references/linear-sync.md](references/linear-sync.md) - Linear workspace patterns
- [references/cli-recipes.md](references/cli-recipes.md) - outline/layer/linear patterns
- [references/agentic-review.md](references/agentic-review.md) - pair skill integration
- [references/error-handling.md](references/error-handling.md) - when things break
- [references/context-handoff.md](references/context-handoff.md) - long sessions, resuming

### scripts
- [scripts/bootstrap-with-patterns.sh](scripts/bootstrap-with-patterns.sh) - phase 0 bootstrap and pattern freshness window
- [scripts/discover-projects.sh](scripts/discover-projects.sh) - pattern discovery across projects
- [scripts/extract-patterns.sh](scripts/extract-patterns.sh) - pattern extraction pipeline

### project alignment
- `@skills/project-audit` - audit against patterns, tools, org standards (invoke in Phase 0 for unfamiliar projects)

## metaprompts

- [metaprompts/synthesis.xml](metaprompts/synthesis.xml) - context synthesis
- [metaprompts/progress.xml](metaprompts/progress.xml) - progress tracking
- [metaprompts/preflight.xml](metaprompts/preflight.xml) - pre-flight validation

## lifecycle reporting

**all loop invocations persist to trails and notify #agents** with claude's identity (the orchestrator).

**RECOMMENDED: `agents report`** (unified trails + slack + optional DM):

```bash
# 1. START: when loop begins (new trace)
export AGENTS_TRACE_ID=$(agents report start "$TASK_SUMMARY" --agent claude --json -q | jq -r '.traceId')

# 2. PROGRESS: major phase transitions (inherits trace from env)
agents report progress "phase $PHASE complete" --confidence 8

# 3. COMPLETE: when loop finishes (with gist for handoff artifact)
agents report complete "$SUMMARY" --confidence 9 --dm --gist

# 4. BLOCKED: on failure or blocked (DM enabled by default)
agents report blocked "$BLOCKER" --blocker-type error
```

**Benefits of `agents report`**:
- Unified: trails record + slack post + optional DM in one command
- Trace correlation: `AGENTS_TRACE_ID` env var auto-inherited
- Error tiering: trails fails hard, slack/DM warn and continue
- Structured JSON output for programmatic consumption

### lifecycle events

```bash
# START: new trace, capture ID
export AGENTS_TRACE_ID=$(agents report start "loop: $PROJECT - $TASK" --agent claude --json -q | jq -r '.traceId')

# PROGRESS: phase transitions
agents report progress "phase 1: context gathered" --confidence 8
agents report progress "phase 2: planning complete" --confidence 8
agents report progress "phase 4: flywheel iteration 3/5" --confidence 7

# COMPLETE: final summary (gist creates permanent handoff artifact)
agents report complete "implemented $FEATURE, 5 commits, all tests pass" --confidence 9 --dm --gist

# BLOCKED: needs human (DM by default)
agents report blocked "need API credentials for $SERVICE" --blocker-type dependency
```

### trace management

```bash
# Start new trace and capture ID (sets AGENTS_TRACE_ID)
export AGENTS_TRACE_ID=$(agents report start "$TASK" --agent claude --json -q | jq -r '.traceId')

# All subsequent events auto-inherit from env
agents report progress "phase 1 complete"
agents report progress "phase 2 complete"
agents report complete "done"

# Query entire trace history
trails trail replay --trace-id $AGENTS_TRACE_ID --format summary
```

### examples

```bash
# loop starting issue mode
export AGENTS_TRACE_ID=$(agents report start "ARB-123: implement user auth" --agent claude --json -q | jq -r '.traceId')

# loop completing (with gist for handoff artifact)
agents report complete "ARB-123: user auth implemented, 3 commits" --confidence 9 --dm --gist

# loop blocked
agents report blocked "ARB-123: missing API credentials" --blocker-type dependency
```

**Alternative: manual trails + slack pipe** (custom formatting, advanced use):

```bash
# Direct trails record + slack post (for custom formatting needs)
trails trail record --agent claude --new-trace --action started --task "$TASK" && \
trails trail replay --last 1 --format slack -q | \
  slack agent post -a claude -c agents --stdin -w saya
```

### pair notifications (automatic)

when loop invokes pair skill, pair records + posts as the spawned agent:
- `pair quick` → copilot records + posts 🐿️
- `pair thorough` → codex records + posts 🦉

loop doesn't duplicate these notifications.

### querying loop history

```bash
# view all events from a loop run
trails trail replay --trace-id $TRACE_ID --format summary

# view recent loop activity
trails trail replay --since 24h --format summary | grep orchestrator

# trace tree (parent/child relationships)
trails trace tree --trace-id $TRACE_ID
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| asking without pair | skips external validation | use pair consult quick before HIL |
| skipping bootstrap | lacks context and patterns | run phase 0 or use `.loop.json` |
| skipping TDD | regressions and shallow changes | follow flywheel, add tests |
| skipping quality gate | incomplete verification | run verify, lint, build, typecheck |
| skipping pair review | blind spots remain | run pair review before completion |
| ignoring platform | wrong commands or assumptions | select correct flywheel |
| scope creep | exceeds requirements | restate scope, cut extras |
| silent failure | user unaware of blockers | report blockers with options |
| fire-and-forget | progress invisible | update TodoWrite + plan + commits |
| hard deps | tool missing breaks flow | use graceful fallback commands |
| direct slack without trails | no persistence, no trace correlation | use trails record + pipe to slack |
| no trace_id | events uncorrelated | use --new-trace at start, --trace-id after |
