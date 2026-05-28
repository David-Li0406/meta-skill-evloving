---
name: linear-audit
description: This skill should be used when auditing Linear projects to ensure optimal V1 state for agent execution. Triggers include "audit my linear", "are my issues ready", "prepare for V1", "what's missing in linear", or when starting a major development push. Conversation-first - uses ask-deep for collaborative discovery, then 4-specialist fanout for comprehensive analysis.
---

# linear-audit

collaborative thought partner for Linear workspace optimization. surfaces what matters through dialogue, brings creative edge to light, and orchestrates specialists for deep analysis.

## philosophy

> "thinking together about what deserves focus, not checking boxes"

| principle | application |
|-----------|-------------|
| conversation-first | ask-deep before any mechanical work - understand passion, priorities |
| creative edge surfacing | identify the sketchy/experimental - what excites you? what needs support? |
| interleaved HIL | decision points throughout, not just start/end |
| thought partnership | LLM as collaborator holding context, offering perspective |
| context as fuel | issues with rich context enable autonomous execution |

### the wattenberger insight

linear-audit is NOT a checklist runner. it's the **taking in → transforming → sending out** cycle:
- **taking in**: your priorities, passion points, codebase state, issue landscape
- **transforming**: synthesis against V1 patterns, gap detection, creative opportunity
- **sending out**: actionable state - enriched issues, disposition decisions, clear next steps

## when to use

| use | skip |
|-----|------|
| "audit my linear", "think through my issues with me" | creating new issues (use linear CLI directly) |
| preparing project for autonomous work | pure codebase analysis (use project-review) |
| "what deserves focus in $PROJECT" | researching codebase (use fanout/explore) |
| pre-V1 collaborative planning | quick question about an issue |
| "help me understand what matters" | |
| enriching issues with codebase context | |
| batch issue enrichment | |

## companion skills

| skill | relationship |
|-------|--------------|
| ask-deep | fundamental - entry point for collaborative discovery |
| project-review | codebase patterns - linear-audit focuses on Linear state |
| fanout | multi-perspective analysis - specialists use same pattern |
| pair | deep consultation on specific issues or decisions |
| loop | autonomous execution - linear-audit prepares the foundation |

**Note**: issue-context patterns are now integrated into linear-audit via `references/issue-enrichment-templates.md`. Use linear-audit for both auditing and per-issue enrichment.

---

## decision tree: conversation vs mechanical

```
What mode should I use?
├── First interaction with this project today?
│   └── ALWAYS: start with ask-deep (discover context)
├── User says "quick check" or "just counts"?
│   └── quick mode (skip ask-deep, return stats)
├── User provides rich context already?
│   └── confirm understanding, then proceed to specialists
├── User seems uncertain about priorities?
│   └── deeper ask-deep (explore mode)
└── Default
    └── ask-deep start mode → specialists → ask-deep review
```

## decision tree: ask-deep mode selection

```
Which ask-deep mode for this phase?
├── Session start / first audit?
│   └── start mode: project, goals, constraints
├── Scope unclear / multiple valid approaches?
│   └── scope mode: MVP, success criteria, exclusions
├── Exploring priorities / passion points?
│   └── explore mode: broad → narrow → edge cases
├── Decision point between options?
│   └── choose mode: options with trade-offs
├── Post-specialist validation?
│   └── review mode: validate findings, edge cases
└── Default
    └── start mode
```

## decision tree: creative edge detection

```
Should I surface creative edge?
├── User mentions "experimental", "sketchy", "not sure"?
│   └── YES: probe deeper - what makes it exciting? what support needed?
├── Issue references unfamiliar pattern/tech?
│   └── YES: "this looks interesting - tell me more"
├── Gap between issue description and codebase reality?
│   └── YES: "I notice a gap - is this intentional exploration?"
├── High energy/passion in user's description?
│   └── YES: follow the energy - this might be the valuable part
├── Multiple approaches mentioned?
│   └── YES: "which feels most alive to you?"
└── Default
    └── listen for signals, ask when curiosity peaks
```

## decision tree: HIL routing

```
When should I pause for human input?
├── Priority/disposition decision?
│   └── ALWAYS: "should we keep, enrich, or archive this?"
├── Creative edge detected?
│   └── ALWAYS: "tell me more about this direction"
├── Confidence < 7 on recommendation?
│   └── PAUSE: present options, get guidance
├── Gap between user expectation and findings?
│   └── PAUSE: "I expected X but found Y - does this match your sense?"
├── Batch operation (>5 items)?
│   └── CONFIRM: "I'll process these 12 issues - proceed?"
├── Delete/archive recommendation?
│   └── ALWAYS: "these look stale/duplicate - ok to archive?"
└── Proceeding with specialist fanout?
    └── CONFIRM: "ready to analyze code + linear state?"
```

## decision tree: disposition workflow

```
What should happen to this issue?
├── Has issue-context markers AND fresh (<14 days)?
│   └── status: ready for V1
├── Has markers but stale (>14 days)?
│   └── HIL: "context is stale - refresh or keep as-is?"
├── No markers, well-formed description?
│   └── action: enrich via issue-context
├── Vague (no description, generic title)?
│   └── HIL: "this seems vague - archive, clarify, or keep?"
├── Duplicate of another issue?
│   └── HIL: "duplicate detected - merge or keep separate?"
├── Outdated (old architecture/patterns)?
│   └── HIL: "this references old patterns - archive?"
├── Epic without children?
│   └── HIL: "epic needs breakdown - explore now or backlog?"
└── User says "delete" or "archive"?
    └── action: archive with confirmation
```

## decision tree: V1 template selection

```
What project type?
├── Convex + Next.js monorepo (arbor, kumori, koto, etc.)?
│   └── template: convex-next-v1
├── Library/utility package (utils)?
│   └── template: library-v1
├── Swift/iOS app (sine-apple)?
│   └── template: swift-v1
├── Slack bot (saya)?
│   └── template: slack-bot-v1
├── CLI tool (agents, layer, outline)?
│   └── template: cli-v1
└── Unknown?
    └── ask: "what does V1 look like for this project?"
```

## decision tree: failure recovery

```
Specialist returned failure/timeout/low-confidence?
├── Single specialist failed (<25% of roster)?
│   ├── Non-critical specialist (e.g., architecture)?
│   │   └── proceed without, note gap in synthesis
│   └── Critical specialist (e.g., linear-state)?
│       └── retry once with increased timeout
├── Multiple specialists failed (25-50%)?
│   ├── Common cause (e.g., tool unavailable)?
│   │   └── fix tool, retry all failed
│   └── Random failures?
│       └── partial synthesis, flag incomplete, continue
├── Majority failed (>50%)?
│   └── abort audit, report blocked, schedule retry
├── Low confidence (<7) across all?
│   └── escalate: "findings uncertain - want me to dig deeper?"
└── Mixed results (some success, some partial)?
    └── weight partial results at 0.7, include with caveats
```

## decision tree: cross-project coordination

Cross-project exploration is **pull-based, not push-based**. Stay focused on the current project unless the conversation naturally surfaces a cross-project connection.

```
Should I look at other projects?
├── User explicitly mentions another project?
│   │   "how does arbor handle this?" / "like in kumori"
│   └── YES: explore that specific project for the specific thing mentioned
│       └── ask first: "want me to look at how arbor handles this?"
├── User references a pattern that sounds familiar?
│   │   "I think we did something similar somewhere"
│   └── MENTION IT: "that sounds like the overlay pattern in saya - want me to check?"
│       └── wait for signal before exploring
├── Issue references shared code explicitly?
│   │   "update @repo/design" / "sync with kumori's approach"
│   └── YES: explore the referenced code
│       └── scope to what's mentioned, don't expand
├── Multi-project audit explicitly requested?
│   │   "audit all my apps" / "compare these projects"
│   └── ask-deep first: "what are you trying to understand across these?"
│       ├── specific pattern? → explore that pattern only
│       ├── general health? → quick stats, no deep dive
│       └── unclear? → "tell me more about what you're looking for"
└── Default
    └── STAY FOCUSED on current project
        └── don't assume cross-project context is useful
```

### why pull-based matters

Some patterns ARE shared across Luke's repos (overlay system, email templates, hooks), but:
- **Auth is standardized** - Clerk + Convex everywhere, not interesting for cross-project
- **Design packages are copies** - each repo has its own @repo/design, intentionally
- **Patterns evolved differently** - that's often the point, not a gap to fix

Cross-project exploration is valuable when:
- User mentions it
- Issue explicitly references another repo
- User says "like in X" or "similar to Y"
- User asks for portfolio-wide view

### known shared patterns (reference, don't scan)

If conversation surfaces these, they exist - don't re-discover:

| Pattern | Repos | Notes |
|---------|-------|-------|
| @overlay system | saya, sine, squish, kumori, abbie, circle | OverlayPage + OverlayContent, class prefixes differ |
| Modals (world-class) | arbor | User mentioned as reusable reference |
| Motion primitives | koto | Framer Motion patterns, unique architecture |
| Email templates | kumori, koto, webs | Different implementations |
| useMediaQuery hook | arbor, koto, kumori | Nearly identical |

### cross-project subagent patterns (when triggered)

Only spawn these when user explicitly requests cross-project work:

**Pattern comparison (user asks "how does X do this?"):**
```bash
cat <<EOF | codex exec - --full-auto -o /tmp/pattern-analysis.json
Explore ~/Developer/arbor/arbor-xyz for modal patterns.

Focus on: how modals handle animation, backdrop, escape key
Compare to what we're doing in current project.

Output JSON: {patterns: [], differences: [], recommendations: []}
EOF
```

**Portfolio quick stats (user asks for overview):**
```bash
# Only when explicitly requested - don't do this automatically
for REPO in arbor kumori koto webs; do
  linear issue list --team ${REPO^^} --json -q | jq '{repo: "'$REPO'", count: length}'
done
```

### contextual flexibility

The key insight: **conversation drives exploration, not automation**.
- If user mentions arbor's modals → explore arbor's modals
- If user says "like in kumori" → look at kumori
- If user doesn't mention other projects → don't assume they're relevant
- When uncertain → ask: "want me to check how X handles this?"

## decision tree: escalation routing

```
Should I escalate to human?
├── Disposition affects other teams?
│   └── ALWAYS: "this touches {TEAM} - should I coordinate?"
├── Archiving high-priority issue?
│   └── ALWAYS: "P1/P2 issue flagged for archive - confirm?"
├── Conflicting specialist findings?
│   └── ALWAYS: present conflict, let human resolve
├── Resource conflict detected (same file in multiple issues)?
│   └── PAUSE: "ARB-123 and ARB-456 both touch auth.ts - sequence?"
├── User explicitly delegated authority?
│   └── proceed with lower threshold, report after
├── Confidence < 5 on any critical recommendation?
│   └── ESCALATE: "I'm uncertain about {X} - thoughts?"
└── Time constraint mentioned?
    └── summarize options, recommend, ask for quick approval
```

## decision tree: Linear agent state management

```
How should I manage Linear state?
├── Starting to work on issue?
│   ├── Move issue to "started" state
│   ├── Set delegate to agent identity
│   └── Emit thought activity: "analyzing {ISSUE}"
├── Analysis in progress?
│   └── Emit thought activities every 10s max
├── Synthesizing findings?
│   └── Emit response activity with AgentActivity (frozen snapshot)
├── Need human input?
│   └── Emit elicitation activity, wait for response
├── Error during processing?
│   └── Emit error activity with details
└── Audit complete?
    ├── Return issue to original state (unless disposition changed it)
    ├── Clear delegate
    └── Emit final response activity
```

---

## concrete values

| value | meaning | source |
|-------|---------|--------|
| ask-deep rounds | 2-3 for start, 3-8 for explore | ask-deep skill |
| specialists | 4 (code, architecture, linear, gaps) | optimal coverage |
| context staleness | 14 days | markers older than this need refresh |
| HIL confidence threshold | 7 | below this, pause for guidance |
| batch confirm threshold | 5 | above this, confirm before proceeding |
| enrichment timeout | 120s per issue | issue-context typical duration |
| parallel enrichments | 3 | avoid rate limiting |

---

## modes

| mode | trigger | orchestration | output |
|------|---------|---------------|--------|
| **full** (default) | "audit ARB", "think through my issues" | ask-deep → specialists → ask-deep review | collaborative audit + enriched issues |
| **quick** | "quick check on ARB" | solo, skip ask-deep | issue count + top gaps |
| **enrich** | "enrich all todo issues" | batch issue-context | enrichment report |
| **report** | "show me audit status" | read-only | current state summary |

---

## workflow

### phase 0: collaborative discovery (ask-deep)

**this is where the magic happens** - understand the human before the mechanical.

```markdown
## ask-deep: start mode

round 1 (Open):
- "Which project are we thinking about today?" (detect from cwd, offer recent)
- "What's on your mind with {PROJECT}? What draws your attention?"
- Affirmation: acknowledge what they share

round 2 (Reflective + Probe):
- "So the energy is around {X}..." (reflect back)
- "What does 'done' look like for you right now?"
- "Anything feeling sketchy or experimental that excites you?"

round 3 (Summary + Creative Edge):
- "Let me make sure I have this..."
- "I'm curious about {thing they mentioned} - tell me more?"
- "Ready to look at the codebase + issues together?"
```

**key questions to surface:**
- What matters most right now?
- What's the creative edge - the experimental, the uncertain?
- What would make this project feel "alive"?
- What's blocking forward motion?

### phase 1: context gathering (tools before specialists)

```bash
# Codebase state
cd "$PROJECT_PATH"
layer . --format=json -q > /tmp/architecture.json
outline --stats --format=yaml > /tmp/code-structure.yaml
verify --format=summary 2>/dev/null || echo "no tests"
git log --oneline -10

# Linear state
linear issue list --team $TEAM --json -q > /tmp/issues.json
linear issue list --team $TEAM --json -q | jq 'group_by(.state.name) | map({state: .[0].state.name, count: length})'
```

### phase 2: spawn specialists (4-agent fanout)

spawn 4 specialists in parallel for deep analysis:

| Specialist | Type | Domain | Tools |
|------------|------|--------|-------|
| **Code State** | Copilot | Codebase | verify, outline, git |
| **Architecture** | Copilot | Structure | layer, outline --graph |
| **Linear State** | Copilot | Issues | linear CLI |
| **V1 Gaps** | Copilot | Synthesis | all findings |

```bash
# Generate parent ID
AUDIT_ID="linear-audit-$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 4)"

# Start trace
export AGENTS_TRACE_ID=$(trails trail record --agent claude --new-trace --action started --task "linear-audit: $TEAM" --json -q | jq -r '.trace_id')

# Spawn specialists with --await
for SPECIALIST in code-state architecture linear-state v1-gaps; do
  (
    RESULT=$(cat "$AUDIT_DIR/briefs/${SPECIALIST}.md" | \
      agents session start -a copilot -p $TEAM \
        -g "${SPECIALIST}: $TEAM audit" \
        --parent "$AUDIT_ID" \
        --timeout 180 \
        --await \
        --json -q)
    echo "$RESULT" >> "$AUDIT_DIR/results.jsonl"
  ) &
done
wait
```

### phase 3: synthesis + HIL checkpoint

after specialists return, synthesize and pause:

```markdown
## synthesis checkpoint

I've gathered findings from 4 specialists. Here's what emerged:

### code state
- coverage: {%}, build: {status}
- recent focus: {areas from git log}

### architecture
- {packages} packages, {cycles} cycles
- notable: {interesting patterns or concerns}

### linear state
- {total} issues: {with_context} enriched, {missing} need context
- distribution: {state breakdown}

### creative edge I noticed
- {anything that seemed experimental/exciting}
- {gaps that might be intentional}

**questions for you:**
1. Does this match your sense of where things are?
2. What surprised you? What feels off?
3. {specific question about creative edge}
```

### phase 4: disposition decisions (interleaved HIL)

for each category of issues, pause for guidance:

```markdown
## disposition decisions

### issues needing enrichment ({count})
{list top 5}
→ "proceed with issue-context enrichment?"

### potentially stale ({count})
{list}
→ "refresh, keep as-is, or archive?"

### vague/unclear ({count})
{list}
→ "clarify together, archive, or keep?"

### ready for V1 ({count})
{list}
→ "these look good - confirm?"
```

### phase 5: execute dispositions

```bash
# Enrich approved issues
for ISSUE in "${ENRICH_QUEUE[@]}"; do
  echo "Enriching $ISSUE..."
  # invoke issue-context skill
  sleep 2  # rate limit
done

# Archive approved issues
for ISSUE in "${ARCHIVE_QUEUE[@]}"; do
  linear issue edit $ISSUE --state "Canceled"
done

# Record completion
trails trail record --agent claude --trace-id $AGENTS_TRACE_ID \
  --action completed \
  --task "linear-audit: $TEAM - $ENRICHED enriched, $ARCHIVED archived" \
  --confidence $CONFIDENCE
```

### phase 6: closing synthesis (ask-deep review)

```markdown
## ask-deep: review mode

round 1:
- "Here's what we accomplished today..."
- "Does this feel like the right state?"
- "Anything we should have caught but didn't?"

round 2:
- "What's the next pull you feel - where to focus next?"
- "When should we revisit this?"
```

---

## orchestration: 4-specialist fanout

### specialist roster

| Specialist | Type | Domain | Primary Focus | Tools |
|------------|------|--------|---------------|-------|
| **Code State** | Copilot | Codebase | Test coverage, build health, recent commits | verify, outline, git |
| **Architecture** | Copilot | Structure | Package deps, cycles, patterns | layer, outline --graph |
| **Linear State** | Copilot | Issues | Issue quality, context markers, staleness | linear CLI |
| **V1 Gaps** | Copilot | Synthesis | Delta between current and V1 template | all findings |

### specialist execution patterns

**Code State Specialist**:
```bash
verify --coverage --json -q | jq '.summary'
pnpm build 2>&1 | tail -20
git log --oneline -20
outline --diff=HEAD~10 --format=yaml
```

**Architecture Specialist**:
```bash
layer . --format=json -q
layer . --check-cycles
outline --unused -r
layer . --mode=files --format=mermaid > /tmp/arch.mmd
```

**Linear State Specialist**:
```bash
linear issue list --team $TEAM --json -q
# Check context markers per issue
linear issue list --team $TEAM --json -q | jq 'group_by(.state.name) | map({state: .[0].state.name, count: length})'
```

**V1 Gaps Specialist**:
```bash
# Compare against V1 template
# Input: code, architecture, linear findings + V1 template
# Output: delta list with prioritized gaps
```

---

## tool integration

| tool | command | purpose |
|------|---------|---------|
| ask-deep | skill invocation | collaborative discovery + review |
| issue-context | skill invocation | per-issue enrichment |
| project-review | skill invocation | codebase pattern analysis |
| fanout | skill invocation | multi-perspective analysis |
| pair | skill invocation | deep consultation |
| linear | `linear issue list`, `linear comment list` | issue queries, context markers |
| outline | `outline --unused`, `outline --diff` | code structure, coverage |
| layer | `layer . --check-cycles` | architecture, cycles |
| verify | `verify --coverage` | test health |
| git | `git log`, `git diff --stat` | trajectory |
| agents | `agents session start --await` | specialist spawning |
| trails | `trails trail record` | audit persistence |
| gh | `gh gist create` | audit artifact |

### trails integration

persist audit sessions for continuity:

```bash
# Start trace
export AGENTS_TRACE_ID=$(trails trail record --agent claude --new-trace --action started --task "linear-audit: $TEAM" --json -q | jq -r '.trace_id')

# Progress
trails trail record --agent claude --trace-id $AGENTS_TRACE_ID --action progress --task "specialists complete" --confidence 7

# Complete with gist
trails trail record --agent claude --trace-id $AGENTS_TRACE_ID --action completed --task "$TEAM: $READY ready, $GAPS gaps" --confidence 9 --gist

# Replay for Slack
trails trail replay --trace-id $AGENTS_TRACE_ID --format slack | slack agent post -a claude -c agents -w saya
```

---

## V1 templates

V1 = "ready for autonomous execution". templates define the bar.

### convex-next-v1

```yaml
name: convex-next-v1
applies_to: [arbor, kumori, koto, webs, squish, pal, saya]

code:
  test_coverage: 80%
  build: passing
  types: clean

architecture:
  cycles: none
  dead_code: <5%

linear:
  all_issues_have_context: true
  context_freshness: <14 days
  no_vague_issues: true

docs:
  agents_md: present and accurate
```

### library-v1

```yaml
name: library-v1
applies_to: [agents-cli, layer, outline, verify, trails]

code:
  test_coverage: 90%
  build: passing
  types: strict

docs:
  readme: comprehensive
  api_docs: generated
```

### cli-v1

```yaml
name: cli-v1
applies_to: [agents, layer, outline, verify, slack, linear]

code:
  test_coverage: 85%
  build: passing

cli:
  help_text: comprehensive
  error_messages: actionable
  json_output: all commands

docs:
  rules_md: present in ~/.agents/rules/
```

---

## team mapping

**Note**: Use full team name with linear CLI (e.g., `--team ARBOR` not `--team ARB`).

| Linear Team | Short Key | Project | Path | Type |
|-------------|-----------|---------|------|------|
| ARBOR | ARB | arbor | ~/Developer/arbor/arbor-xyz | convex-next |
| KUMORI | KUM | kumori | ~/Developer/kumori/kumori-xyz | convex-next |
| KOTO | KOT | koto | ~/Developer/koto/koto-xyz | convex-next |
| SINE | SIN | sine | ~/Developer/sine/sine-xyz | convex-next |
| WEBS | WEB | webs | ~/Developer/webs/webs-xyz | convex-next |
| SAYA | SAY | saya | ~/Developer/saya/saya-xyz | convex-next |
| SQUISH | SQU | squish | ~/Developer/squish/squish-xyz | convex-next |
| PAL | PAL | pal | ~/Developer/pal/pal-xyz | convex-next |
| UTILS | UTI | utils | ~/Developer/utils | library |
| SPOTS | SIP | spottedinprod | ~/Developer/spottedinprod/sip | convex-next |

---

## output contract

```json
{
  "mode": "full | quick | enrich | report",
  "status": "success | partial | blocked",
  "summary": "collaborated on ARB linear state - 12 enriched, 3 archived, creative edge on ACP protocol surfaced",
  "confidence": 8,
  "inputs": {
    "team": "ARB",
    "project_path": "~/Developer/arbor/arbor-xyz",
    "project_type": "convex-next",
    "ask_deep_rounds": 3
  },
  "artifacts": [
    { "type": "file", "path": "~/.agents/audits/ARB-20250122/AUDIT.md", "status": "created" }
  ],
  "sources": {
    "prompts": [],
    "files_read": ["issues.json", "architecture.json"]
  },
  "findings": {
    "code_state": { "coverage": 82, "build": "passing" },
    "architecture": { "cycles": 0, "dead_code_pct": 3 },
    "linear_state": { "total": 45, "with_context": 32, "stale": 8, "none": 5 },
    "v1_gaps": { "blockers": 2, "gaps": 5 },
    "creative_edge": ["ACP protocol exploration", "gen-ui experiments"]
  },
  "disposition": {
    "enriched": ["ARB-123", "ARB-456"],
    "archived": ["ARB-789"],
    "kept": ["ARB-101"]
  },
  "ask_deep_synthesis": {
    "priorities": ["ACP agent integration", "test coverage"],
    "passion_points": ["real-time collaboration", "daemon integration"],
    "creative_edge": "ACP protocol feels most alive",
    "next_pull": "focus on agent spawning E2E"
  },
  "v1_ready": false,
  "blockers": ["5 issues missing context"],
  "next_steps": ["run issue-context on queue", "revisit in 1 week"],
  "gist_url": "https://gist.github.com/...",
  "trace_id": "tr_abc123"
}
```

---

## primary sources

| source | contribution | reference |
|--------|--------------|-----------|
| Wattenberger (2024) | Taking in → transforming → sending out cycle | "LLMs as a Tool for Thought" |
| Miller & Rollnick (2012) | OARS technique for collaborative dialogue | Motivational Interviewing, 3rd ed |
| Schwarz (2002) | Skilled facilitator model for group process | The Skilled Facilitator |
| Kaner (2014) | Participatory decision-making, groan zone | Facilitator's Guide to Participatory Decision-Making |
| Csikszentmihalyi (1990) | Flow state, following energy | Flow: Psychology of Optimal Experience |
| Linear (2025) | AgentActivities, state management, 10s response | Linear Agent Best Practices |

---

## references

### audit workflow
- [references/v1-templates.md](references/v1-templates.md) - V1 definitions per project type
- [references/specialist-briefs.md](references/specialist-briefs.md) - full specialist prompts
- [references/audit-criteria.md](references/audit-criteria.md) - scoring rubrics
- [references/sample-audit-output.md](references/sample-audit-output.md) - complete AUDIT.md artifact
- [references/conversation-examples.md](references/conversation-examples.md) - annotated ask-deep transcripts

### issue enrichment (integrated from issue-context skill)
- [references/issue-enrichment-templates.md](references/issue-enrichment-templates.md) - comment templates, agent prompts, decision trees
- [references/diagram-generation.md](references/diagram-generation.md) - mermaid patterns for architecture visualization
- [references/cli-integration.md](references/cli-integration.md) - linear, outline, layer, git command patterns

### linear integration
- [references/linear-agent-patterns.md](references/linear-agent-patterns.md) - AgentActivities and state management
- [references/linear-patterns.md](references/linear-patterns.md) - Linear CLI patterns

## scripts

- [scripts/audit-project.sh](scripts/audit-project.sh) - single project audit
- [scripts/enrich-batch.sh](scripts/enrich-batch.sh) - batch issue-context enrichment

---

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| skipping ask-deep | mechanical audit misses priorities | ALWAYS start with conversation |
| no HIL checkpoints | decisions made without human input | pause at disposition, creative edge |
| ignoring creative edge | miss the most valuable parts | follow energy, ask about experimental |
| checklist mentality | treats audit as box-checking | think together, not at |
| no trails persistence | audit lost after session | trails record throughout |
| batch without confirm | archives without approval | HIL before any disposition |
| auditing without code access | context lacks file refs | cd to project first |
| single-pass approach | no synthesis or review | ask-deep review at end |
| rushing to specialists | mechanical before understanding | conversation first |
| ignoring passion points | optimize for metrics not meaning | what excites the human? |
| passive Linear state | not moving issues to started, not setting delegate | use Linear agent state management tree |
| context drift | running specialists on stale codebase state | re-gather context if audit spans multiple days |
| audit thrashing | re-auditing before issues addressed | minimum 1 week between full audits per project |
| automatic cross-project scanning | assumes cross-project context is always useful | pull-based: explore other projects only when user mentions them or conversation surfaces connection |
| over-discovering patterns | re-scanning for patterns already known | reference known shared patterns, don't re-discover |
