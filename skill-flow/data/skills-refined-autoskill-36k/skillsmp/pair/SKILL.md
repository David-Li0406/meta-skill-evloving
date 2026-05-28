---
name: pair
description: This skill should be used for all external AI collaboration - consulting, implementing, or reviewing with codex/copilot. Triggers include "pair with codex", "get a second opinion", "delegate this", "consult on", "review this work". Uses output contracts to return lean, structured responses that don't pollute the orchestrating agent's context.
---

# pair

unified external AI collaboration with **output contracts**. agents work internally, return structured JSON only.

> the orchestrating agent should never see 10K lines of reasoning. only the deliverable.

## philosophy

| principle | application |
|-----------|-------------|
| output contracts | every call returns predictable JSON, not prose |
| context hygiene | agent reasoning stays private, only results surface |
| metaprompt patterns | prompts use XML structure with baked-in schemas |
| confidence routing | low confidence escalates, high confidence proceeds |

## the architecture

```
WITHOUT OUTPUT CONTRACTS (bad):
┌────────────────────────────────────────────┐
│ claude code → pair → codex                 │
│                        ↓                   │
│                  30 min of work            │
│                  10-15K lines output       │
│                        ↓                   │
│                  TaskOutput pulls ALL      │
│                        ↓                   │
│                  context destroyed         │
└────────────────────────────────────────────┘

WITH OUTPUT CONTRACTS (good):
┌────────────────────────────────────────────┐
│ claude code → pair → build prompt          │
│                        ↓                   │
│                  inject output contract    │
│                        ↓                   │
│                  execute (codex -o file)   │
│                        ↓                   │
│                  read structured JSON      │
│                        ↓                   │
│                  ~200-500 tokens returned  │
└────────────────────────────────────────────┘
```

## when to use

| use | skip |
|-----|------|
| second opinion on approach | simple questions claude can answer |
| heavy implementation (10+ min) | quick changes claude can do directly |
| final review before PR | trivial fixes |
| architectural exploration | pure research (use fanout skill or `layer` → `outline`) |

## concrete values

| value | meaning | source |
|-------|---------|--------|
| quick tier threshold | tasks < 5 min or explicit "quick" | heuristic: copilot completes simple tasks in 30-90s |
| thorough tier threshold | tasks >= 10 min or complex | heuristic: codex excels at multi-file, reasoning-heavy work |
| copilot timeout | 120s | empirical: gemini-3-pro response times (see `rules/copilot.md`) |
| codex timeout | 600s (10 min) | empirical: gpt-5.2-codex xhigh reasoning needs 3-15 min (see `rules/codex.md`) |
| proceed confidence | >= 7 | convention: upper third of 1-10 scale indicates reliable signal |
| escalate confidence | < 7 | convention: below upper third warrants second opinion |
| auto-push confidence | >= 8 | heuristic: high bar for automated code changes to remote |
| HIL threshold | < 5 | convention: midpoint indicates agent uncertainty too high |
| output token target | 200-500 | empirical: well-structured JSON contracts fit this range |

**sourcing legend**: `heuristic` = practical experience; `empirical` = measured from tool usage; `convention` = standard practice

## decision tree: mode selection

```
What mode?
├── "what do you think", "should I", "is this right"
│   └── mode: CONSULT
├── "implement", "build", "create", "add"
│   └── mode: DELEGATE
├── "review", "check", "audit", "verify"
│   └── mode: REVIEW
├── "multiple perspectives", "pair group"
│   └── mode: GROUP
└── ambiguous
    └── ask: "consult, delegate, or review?"
```

## decision tree: tier selection

```
Which tier?
├── "quick" keyword or <5 min estimate
│   └── tier: QUICK (copilot)
├── "thorough" keyword or complex task
│   └── tier: THOROUGH (codex)
├── high-risk signals (infra, security, migrations)
│   └── tier: THOROUGH + confirm
└── default
    └── tier: QUICK, escalate if confidence < 7
```

## output contract

**every external agent call returns this structure:**

```json
{
  "mode": "consult | delegate | review",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 words",
  "confidence": 8,
  "inputs": {
    "task": "original task description",
    "constraints": ["any constraints"]
  },
  "artifacts": [
    {
      "type": "analysis | code | recommendation | decision | issues",
      "content": "the deliverable",
      "path": "optional/file.ts",
      "language": "typescript"
    }
  ],
  "sources": {
    "prompts": ["/tdd"],
    "files_read": ["src/auth.ts:10-50"]
  },
  "assumptions": ["assumption that could affect correctness"],
  "verification": {
    "commands_run": ["verify --format=summary"],
    "tests_passed": true
  },
  "next_steps": ["optional"],
  "blockers": ["if blocked"],
  "escalate": false,
  "escalate_reason": "only if escalate=true"
}
```

see [~/Developer/skills/.system/output-contract.md](../.system/output-contract.md) for full schema.

## workflow

### 1. detect mode and tier

```
Input: user request
Output: {mode, tier}

mode from intent signals
tier from complexity + keywords
```

### 2. build prompt with output contract

select template from [references/prompt-templates.md](references/prompt-templates.md):

```xml
<role>{role_for_mode}</role>

<context>
  {context_packet_json}
</context>

<task>{task_description}</task>

<output_contract>
  CRITICAL: Respond with ONLY this JSON.
  {schema}
</output_contract>
```

### 3. execute with structured capture

**RECOMMENDED: Use `agents session start --await` for unified management**

```bash
# Start lifecycle trace
export AGENTS_TRACE_ID=$(agents report start "$MODE: $TASK_SUMMARY" --json -q | jq -r '.traceId')

# copilot (quick tier) - --await blocks until done, returns result inline
RESULT=$(cat /tmp/prompt.md | agents session start -a copilot -p $PROJECT -g "$TASK" \
  --parent "$AGENTS_TRACE_ID" \
  --timeout 120 \
  --await \
  --json -q)
# Returns: { session_id, await: { status, output } }

# codex (thorough tier) - longer timeout for deep work
RESULT=$(cat /tmp/prompt.md | agents session start -a codex -p $PROJECT -g "$TASK" \
  --parent "$AGENTS_TRACE_ID" \
  --timeout 600 \
  --await \
  --json -q)
# Returns: { session_id, await: { status, output } }
```

**Parse await results:**
```bash
STATUS=$(echo "$RESULT" | jq -r '.await.status')  # completed | timeout | failed
OUTPUT=$(echo "$RESULT" | jq -r '.await.output')  # structured JSON from output contract
```

**Alternative: Direct CLI (when session management overhead isn't needed)**

```bash
# copilot (quick) - use stdin (interactive mode, no -p)
cat > /tmp/prompt.txt << 'PROMPT'
{prompt_with_contract}
PROMPT
RESPONSE=$(cat /tmp/prompt.txt | copilot --model gemini-3-pro-preview --silent 2>&1 | head -1)

# codex (thorough) - always use -o flag
# For network/cross-repo tasks: --dangerously-bypass-approvals-and-sandbox
# For in-repo work: --full-auto
cat /tmp/prompt.md | codex exec - --full-auto -o /tmp/response.json --json
```

### 3b. wait for completion (CRITICAL)

**NEVER use TaskOutput to wait for codex.** It pulls 10-15K lines and destroys context.

**PREFERRED: Use --await (blocks until completion)**
```bash
# --await handles waiting internally, returns when done
RESULT=$(cat /tmp/prompt.md | agents session start -a codex -p $PROJECT -g "$TASK" \
  --timeout 600 --await --json -q)

# Check status and extract output
if [ "$(echo "$RESULT" | jq -r '.await.status')" = "completed" ]; then
  OUTPUT=$(echo "$RESULT" | jq -r '.await.output')
  # Use output directly (~200-500 tokens in structured JSON)
fi
```

**Alternative: Manual polling (when --await not suitable)**
```bash
# Session start returns output_path
SESSION=$(cat /tmp/prompt.md | agents session start -a codex -p $PROJECT -g "$TASK" --json -q)
OUTPUT_PATH=$(echo $SESSION | jq -r '.output_path')

# Wait for response file
while [ ! -f "$OUTPUT_PATH" ]; do sleep 10; done
# Use Read tool on $OUTPUT_PATH (~200-500 tokens)
```

| Method | Result |
|--------|--------|
| --await flag | Blocks until done, returns inline (~200-500 tokens) |
| Read -o file / output_path | Poll + read (~200-500 tokens) |
| TaskOutput | **NEVER** - 10,000-50,000 tokens, context destroyed |

### 4. validate and route

```
Parse JSON response
├── valid JSON?
│   ├── no → retry once with "respond with JSON only"
│   └── yes → continue
├── status == "blocked" or "failed"?
│   └── check escalate field, maybe HIL
├── confidence < 5?
│   └── escalate to codex or HIL
└── confidence >= 7?
    └── proceed with result
```

### 5. surface to orchestrating agent

return ONLY the structured response. the orchestrating agent should surface `summary` to the user.

**consult result (json):**
```json
{
  "mode": "consult",
  "status": "success",
  "summary": "Analyzed authentication options for mobile and web. JWT with refresh tokens is recommended because it supports stateless scaling, mobile clients, and short-lived access tokens with rotation. Session cookies are simpler but require sticky sessions and do not work well for mobile. Suggested 15-minute access tokens with refresh rotation and a revoke list.",
  "confidence": 9,
  "artifacts": [
    {
      "type": "analysis",
      "content": "## Options\n\n- JWT + refresh tokens\n- Session cookies\n\n## Recommendation\nJWT with refresh rotation and revocation list."
    }
  ],
  "next_steps": ["implement token refresh endpoint"],
  "blockers": [],
  "escalate": false
}
```

**delegate result (json):**
```json
{
  "mode": "delegate",
  "status": "success",
  "summary": "Implemented the user auth flow with Convex mutations, a React AuthProvider, and a protected route wrapper. Added login/logout handling, token refresh wiring, and Clerk session integration. Verified with tests and a local login/logout smoke test. All tests pass with no type errors. Next steps are OAuth provider integration and password reset.",
  "confidence": 9,
  "artifacts": [
    {
      "type": "code",
      "path": "convex/auth.ts",
      "language": "typescript",
      "content": "// auth mutations and helpers summary"
    },
    {
      "type": "code",
      "path": "packages/web/AuthProvider.tsx",
      "language": "typescript",
      "content": "// provider wiring and guards summary"
    }
  ],
  "next_steps": ["add OAuth providers", "implement password reset"],
  "blockers": [],
  "escalate": false
}
```

**review result (json):**
```json
{
  "mode": "review",
  "status": "success",
  "summary": "Reviewed PR #123 for correctness, security, performance, and tests. Found two blocking issues: an N+1 query in src/api/users.ts and a missing admin auth check in src/api/admin.ts. Suggested three non-blocking improvements around validation extraction, test coverage, and docs, including adding a regression test for the auth check and batching the user fetch to remove the N+1 pattern. Merge readiness is 6/10 pending fixes.",
  "confidence": 8,
  "artifacts": [
    {
      "type": "issues",
      "content": "## Blocking Issues\n1. N+1 query in src/api/users.ts\n2. Missing admin auth check in src/api/admin.ts\n\n## Suggestions\n- Extract validation\n- Add tests\n- Update docs\n\n## Merge Readiness: 6/10"
    }
  ],
  "next_steps": ["fix N+1 query", "add admin auth check", "add regression test"],
  "blockers": [],
  "escalate": false
}
```

## mode patterns

**See `~/.agents/skills/components/enriched-context-integration.md` for standard pattern.**

All modes now use:
- **Enriched context** (~250 tokens): git state, user prefs, execution constraints
- **Documentation grounding** (~500 tokens): zero CLI syntax errors
- **Output contracts**: structured JSON responses

### consult

```bash
# 1. Generate enriched context
CONTEXT=$(bash ~/.agents/lib/context-fetcher.sh \
  --project="${PROJECT}" \
  ${ISSUE:+--issue="${ISSUE}"})

# 2. Inject copilot docs
DOCS=$(bash ~/.agents/lib/inject-docs.sh copilot consult)

# 3. Build prompt with enriched context
PROMPT=$(cat <<PROMPT
${DOCS}

<context_packet>
${CONTEXT}
</context_packet>

<question>
${QUESTION}
</question>

<output_contract>
{
  "mode": "consult",
  "status": "success",
  "summary": "...",
  "confidence": 8,
  "next_steps": ["..."],
  "next_skills_recommended": []
}
</output_contract>
PROMPT
)

# 4. Invoke copilot (quick tier)
RESPONSE=$(echo "${PROMPT}" | copilot --model gemini-3-pro-preview --silent)
```

### delegate

```bash
# 1. Generate enriched context (with external flag for codex)
CONTEXT=$(bash ~/.agents/lib/context-fetcher.sh \
  --project="${PROJECT}" \
  ${ISSUE:+--issue="${ISSUE}"} \
  --allow-external)

# 2. Inject codex docs
DOCS=$(bash ~/.agents/lib/inject-docs.sh codex delegate)

# 3. Build comprehensive prompt
PROMPT=$(cat <<PROMPT
${DOCS}

<context_packet>
${CONTEXT}
</context_packet>

<task>
${TASK_DESCRIPTION}

Requirements enforced by context packet:
- tests_required: true
- lint_required: true
- push_requires_approval: true
</task>

<verification>
Run before committing:
1. verify --format=summary
2. pnpm typecheck
3. pnpm lint
4. pnpm build

Do NOT commit if any gate fails.
</verification>

<output_contract>
{
  "mode": "delegate",
  "status": "success|blocked",
  "summary": "...",
  "confidence": 8,
  "commits": [{"hash": "...", "msg": "...", "files_changed": 3}],
  "verification": {
    "tests": "pass",
    "types": "pass",
    "lint": "pass",
    "build": "pass"
  },
  "push_ready": true,
  "next_skills_recommended": []
}
</output_contract>
PROMPT
)

# 4. Invoke codex (thorough tier)
echo "${PROMPT}" | codex exec - --dangerously-bypass-approvals-and-sandbox -o /tmp/response.json

# 5. Wait for completion and read structured response
while [ ! -f /tmp/response.json ]; do sleep 10; done
cat /tmp/response.json
```

### commit checkpoint

after completing delegate work, agents SHOULD commit if:
- files were modified (not just analysis)
- changes are coherent (single purpose)
- task represents a logical unit

```bash
# commit with context (agent includes co-author)
git add -A && git commit -m "$(cat <<'EOF'
feat($ISSUE): $SHORT_DESCRIPTION

$WHAT_CHANGED

Co-Authored-By: codex <noreply@openai.com>
EOF
)"
```

| scenario | commit? |
|----------|---------|
| implemented feature | yes |
| fixed bug | yes |
| pure analysis/consult | no |
| partial work (blocked) | no |

### verification cascade

after committing, run verification gates before considering push:

```bash
# 1. run tests
VERIFY_RESULT=$(verify --format=summary 2>&1)
VERIFY_PASS=$?

# 2. run build (if applicable)
BUILD_RESULT=$(pnpm build 2>&1 || npm run build 2>&1 || echo "no build")
BUILD_PASS=$?

# 3. assess confidence (agent self-reports in output contract)
# confidence already in $CONFIDENCE from task completion
```

**gate status:**

| gate | pass condition |
|------|----------------|
| verify | exit code 0, no failures |
| build | exit code 0, no type errors |
| confidence | >= 8 for auto-push |

### push authority

push authority flows from **tier + verification status**:

```
Agent completes work → commits → runs verification
    ↓
All gates pass?
├── NO → report "blocked", include failures, DON'T PUSH
└── YES → check tier authority:
    ├── quick (copilot): report "push-ready", DON'T PUSH
    ├── thorough (codex): PUSH, report "pushed"
    └── orchestrator (claude): PUSH, report "pushed"
```

**tier authority table:**

| tier | agent | gates pass | action |
|------|-------|------------|--------|
| quick | copilot | yes | commit only, report push-ready |
| quick | copilot | no | commit only, report blocked |
| thorough | codex | yes | **push** + report pushed |
| thorough | codex | no | commit only, report blocked |
| orchestrator | claude | yes | **push** + report pushed |
| orchestrator | claude | no | commit only, report blocked |

**rationale:**
- quick tier is exploratory, orchestrator decides whether to keep
- thorough tier has high investment, well-verified work should ship
- orchestrator always has final authority

**push command:**

```bash
# only if tier authority allows and gates pass
git push origin $(git branch --show-current)
PUSHED=true
```

### nested hierarchy example

```
claude (orchestrator)
  → pair thorough → codex
    → pair quick → copilot
      commits "fix: helper function"
      verify passes, confidence 8
      reports push-ready (quick tier, doesn't push)
    codex reviews, integrates
    codex commits "feat: auth flow"
    verify passes, confidence 9
    codex PUSHES (thorough tier + gates pass)
  claude receives: pushed=true, deeplinks work immediately
```

### review

```bash
# 1. Generate enriched context
CONTEXT=$(bash ~/.agents/lib/context-fetcher.sh \
  --project="${PROJECT}" \
  ${ISSUE:+--issue="${ISSUE}"})

# 2. Inject docs (copilot for quick, codex for thorough)
DOCS=$(bash ~/.agents/lib/inject-docs.sh ${TIER:-copilot} review)

# 3. Build review prompt
PROMPT=$(cat <<PROMPT
${DOCS}

<context_packet>
${CONTEXT}
</context_packet>

<review_target>
${REVIEW_TARGET}  # could be: files changed, PR diff, commit range
</review_target>

<focus_areas>
- Security vulnerabilities
- Correctness (logic errors, edge cases)
- Performance issues
- Code quality (patterns, tests, docs)
</focus_areas>

<output_contract>
{
  "mode": "review",
  "status": "success",
  "summary": "...",
  "confidence": 8,
  "issues": [
    {"severity": "error|warning|info", "file": "...", "line": 42, "message": "..."}
  ],
  "recommendations": ["..."],
  "approve": true,
  "next_steps": ["..."]
}
</output_contract>
PROMPT
)

# 4. Invoke (copilot for quick, codex for thorough)
if [ "${TIER}" = "thorough" ]; then
  echo "${PROMPT}" | codex exec - --full-auto -o /tmp/response.json
  while [ ! -f /tmp/response.json ]; do sleep 10; done
  cat /tmp/response.json
else
  echo "${PROMPT}" | copilot --model gemini-3-pro-preview --silent
fi
```

## confidence routing

| confidence | action |
|------------|--------|
| 9-10 | proceed with result |
| 7-8 | proceed, note caveats |
| 5-6 | escalate quick → thorough |
| 1-4 | escalate to HIL |

## lifecycle reporting

**all pair invocations report via `agents report`** for unified trails + slack + optional DM.

### RECOMMENDED: agents report (unified)

```bash
# AGENT is auto-detected from session, or specify explicitly
AGENT=$( [ "$TIER" = "thorough" ] && echo "codex" || echo "copilot" )

# 1. START: begin trace (session start does this automatically if AGENTS_TRACE_ID not set)
export AGENTS_TRACE_ID=$(agents report start "$MODE: $TASK_SUMMARY" --agent $AGENT --json -q | jq -r '.traceId')

# 2. PROGRESS: optional mid-work updates
agents report progress "implementing $FEATURE" --confidence 7

# 3. COMPLETE: when done (gist for delegation handoffs)
agents report complete "$SUMMARY" --confidence $CONFIDENCE --artifacts "$FILES_CHANGED" --gist
# If PUSHED, include that info in summary

# 4. BLOCKED: on failure (DMs by default)
agents report blocked "$BLOCKER" --blocker-type error
```

**Benefits over manual slack agent post:**
- Single command handles trails + slack + optional DM
- Trace ID correlation across events
- Auto-detects agent from session environment
- Structured JSON output for programmatic use

### Alternative: Direct slack agent post (verbose, for custom formatting)

```bash
# AGENT is "codex" or "copilot" based on tier
AGENT=$( [ "$TIER" = "thorough" ] && echo "codex" || echo "copilot" )

# START
slack agent post --agent $AGENT --channel agents --text "$(cat <<EOF
starting: $MODE $TASK_SUMMARY
\`\`\`yaml
agent: $AGENT
action: started
task: "$TASK"
refs:
  issue: "$ISSUE"
\`\`\`
EOF
)" -w saya

# COMPLETE (with verification and push logic)
REPO_URL=$(git remote get-url origin | sed 's/\.git$//' | sed 's|git@github.com:|https://github.com/|')
COMMIT_HASH=$(git rev-parse --short HEAD)
BRANCH=$(git branch --show-current)

VERIFY_STATUS=$( verify --format=summary >/dev/null 2>&1 && echo "pass" || echo "fail" )
BUILD_STATUS=$( pnpm build >/dev/null 2>&1 && echo "pass" || echo "fail" )
PUSHED=false
if [ "$VERIFY_STATUS" = "pass" ] && [ "$BUILD_STATUS" = "pass" ] && [ "$CONFIDENCE" -ge 8 ]; then
  if [ "$TIER" = "thorough" ]; then
    git push origin $BRANCH && PUSHED=true
  fi
fi

slack agent post --agent $AGENT --channel agents --text "$(cat <<EOF
done: $SUMMARY (confidence: $CONFIDENCE/10)$([ "$PUSHED" = "true" ] && echo " [pushed]")
\`\`\`yaml
agent: $AGENT
action: completed
task: "$TASK"
confidence: $CONFIDENCE
tier: $TIER
repo:
  name: "$(basename $REPO_URL)"
  url: "$REPO_URL"
git:
  committed: true
  pushed: $PUSHED
  push_ready: $([ "$VERIFY_STATUS" = "pass" ] && [ "$BUILD_STATUS" = "pass" ] && echo "true" || echo "false")
  branch: "$BRANCH"
verification:
  verify: $VERIFY_STATUS
  build: $BUILD_STATUS
commits:
  - hash: "$COMMIT_HASH"
    msg: "$(git log -1 --format=%s)"
    url: "$REPO_URL/commit/$COMMIT_HASH"
files:
  - path: "$PRIMARY_FILE"
    lines: "$LINE_RANGE"
    url: "$REPO_URL/blob/$BRANCH/$PRIMARY_FILE#L$LINE_START-L$LINE_END"
refs:
  issue: "$ISSUE"
summary: |
  $BRIEF_SUMMARY
\`\`\`
EOF
)" -w saya

# BLOCKED
slack agent post --agent $AGENT --channel agents --text "$(cat <<EOF
blocked: $BLOCKER
\`\`\`yaml
agent: $AGENT
action: blocked
task: "$TASK"
blockers:
  - "$BLOCKER"
refs:
  issue: "$ISSUE"
\`\`\`
EOF
)" -w saya
```

### agent identity mapping

| tier | CLI | posts as | emoji |
|------|-----|----------|-------|
| quick | copilot | copilot | :chipmunk: |
| thorough | codex | codex | :owl: |

### context trail schema

see `slack` skill for full schema. key fields:

| field | when |
|-------|------|
| `commits` | after delegate with file changes |
| `files` | always for delegate, optional for review |
| `confidence` | on completion |
| `blockers` | when blocked |

## HIL escalation

when confidence < 5 or status == "blocked":

```bash
# create context for human
cat << EOF
## HIL Needed

**Task:** $TASK
**Agent:** $AGENT
**Confidence:** $CONFIDENCE/10

**Blocking issue:**
$BLOCKER

**Options considered:**
$OPTIONS
EOF

# notify via slack (agent posts its own escalation)
slack agent post --agent $AGENT --channel agents \
  --text "HIL needed: $SUMMARY (confidence: $CONFIDENCE/10)" -w saya
```

## group mode

run multiple models in parallel, synthesize:

**RECOMMENDED: Session spawning with --await for parallel agents**

```bash
# Generate parent ID for group correlation
GROUP_ID="group-$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 4)"

# same prompt for all agents
cat > /tmp/group-prompt.md << 'PROMPT'
{shared_prompt_with_output_contract}
PROMPT

# parallel session spawning with --await in background jobs
(
  RESULT=$(cat /tmp/group-prompt.md | agents session start -a copilot -p $PROJECT \
    -g "group: $TASK" --parent "$GROUP_ID" --timeout 120 --await --json -q)
  echo "$RESULT" >> /tmp/group-results.jsonl
) &

(
  RESULT=$(cat /tmp/group-prompt.md | agents session start -a codex -p $PROJECT \
    -g "group: $TASK" --parent "$GROUP_ID" --timeout 600 --await --json -q)
  echo "$RESULT" >> /tmp/group-results.jsonl
) &

# Wait for all background jobs
wait

# Filter successful results and synthesize
jq -c 'select(.await.status == "completed")' /tmp/group-results.jsonl > /tmp/valid.jsonl
# Each .await.output is ~200-500 tokens, synthesize best elements
```

**Query group hierarchy:**
```bash
# List all sessions in this group
agents session list --json -q | jq -r --arg parent "$GROUP_ID" \
  '.[] | select(.parent_session_id == $parent)'
```

**Alternative: Direct CLI (no session tracking)**

```bash
# parallel execution
cat /tmp/group-prompt.md | copilot --model gemini-3-pro-preview --silent > /tmp/gemini.txt &
cat /tmp/group-prompt.md | codex exec - --full-auto -o /tmp/gpt.json --json &

wait
```

## tool integration

| tool | command | purpose |
|------|---------|---------|
| copilot | `cat file \| copilot --model gemini-3-pro-preview --silent` | quick tier consult/review (stdin interactive mode) |
| codex | `codex exec - --full-auto -o /tmp/response.json` | thorough tier delegate/review (in-repo) |
| codex | `codex exec - --dangerously-bypass-approvals-and-sandbox -o /tmp/response.json` | network/cross-repo tasks |
| agents | `agents session start --await`, `agents report` | session management, lifecycle reporting |
| trails | `agents report` (unified) | persistence via agents CLI |
| slack | `slack agent post --agent X` | lifecycle notifications |

### trails integration

pair uses `agents report` which handles trails internally:

```bash
# Start trace (records to trails + posts to slack)
export AGENTS_TRACE_ID=$(agents report start "$MODE: $TASK" --agent $AGENT --json -q | jq -r '.traceId')

# Complete (records completion + posts summary + creates gist artifact)
agents report complete "$SUMMARY" --confidence $CONFIDENCE --gist

# Query pair history
trails trail replay --format json | jq '.[] | select(.task | contains("consult\|delegate\|review"))'
```

**trails enables**:
- tracking consultation patterns over time
- measuring delegate success rates
- confidence calibration across tiers

## references

### shared components (all skills)

- `~/.agents/skills/components/enriched-context-integration.md` - **standard integration pattern**
- `~/.agents/skills/components/output-contract.md` - response schemas, confidence routing
- `~/.agents/lib/context-fetcher.sh` - generates enriched context packets (~250 tokens)
- `~/.agents/lib/inject-docs.sh` - injects documentation grounding (~500 tokens)

### skill-specific references

- [references/output-contracts.md](references/output-contracts.md) - response schema, validation
- [references/prompt-templates.md](references/prompt-templates.md) - XML templates by mode
- [references/escalation-patterns.md](references/escalation-patterns.md) - when to escalate
- [references/context-examples.md](references/context-examples.md) - context packet examples

### external claude code rules

- `~/.claude/rules/codex.md` - codex flags, monitoring
- `~/.claude/rules/copilot.md` - copilot flags, models

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| **--full-auto for network tasks** | sandbox blocks network | use `--dangerously-bypass-approvals-and-sandbox` |
| **TaskOutput for codex** | **pulls 10K+ lines, DESTROYS context** | use `-o` flag + Read file directly |
| waiting with TaskOutput | same as above | poll for -o file, then Read tool |
| freeform prompts | unpredictable responses | use templates with contracts |
| no output contract | agent returns prose | always embed contract |
| ignoring confidence | miss escalation signals | route on confidence |
| surfacing raw output | pollutes context | return structured summary only |
| fire and forget | miss failures | always check status field |
