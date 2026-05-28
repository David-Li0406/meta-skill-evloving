---
name: ask-deep
description: This skill should be used for interactive clarification with smart HIL question flows. Triggers include "ask me questions", "help me think through", "what should we consider", session start ("what are we working on"), scope definition ("what's in/out"), or review checkpoints ("does this look right"). Auto-detects context and adapts question depth. Override with explicit mode (ask-deep start, ask-deep scope, ask-deep review).
---

# ask-deep

Context-first HIL questions using OARS technique. Auto-detects mode or accepts explicit override.

## when to use

| use | skip |
|-----|------|
| session start - "what are we working on" | obvious task with clear requirements |
| scope ambiguity - multiple valid approaches | single-file changes |
| requirements unclear - need to clarify intent | bug fixes with reproduction steps |
| pre-implementation - validate understanding | tasks where user gave detailed spec |
| design decisions - trade-offs to discuss | pure research/exploration |
| review checkpoints - "does this look right" | automated processes |

**Note**: This skill is for gathering human input when tools can't answer the question. If the answer is discoverable via `outline`, `layer`, `git log`, or Linear - use tools first.

## modes

| mode | trigger | behavior |
|------|---------|----------|
| **start** | session beginning, "what are we working on" | project, goal, constraints - 2-3 rounds |
| **scope** | "what's in/out", scope definition | MVP, success criteria, explicit exclusions - 2 rounds |
| **explore** | "ask me questions", "help me think" | broad → narrow → edge cases - 3-8 rounds |
| **choose** | decision point, "which approach" | options with trade-offs - 1 round |
| **review** | pre-completion, "does this look right" | validate behavior, edge cases - 1-2 rounds |

## auto-detection

```
What mode should I use?
├── User explicitly requests mode? ("ask-deep start", "use explore mode")
│   └── use requested mode (explicit override wins)
├── Session just started? (no prior context)
│   └── mode: start
├── User asks about scope/boundaries?
│   └── mode: scope
├── User asks "which" or presents options?
│   └── mode: choose
├── Task nearly complete?
│   └── mode: review
└── Default
    └── mode: explore
```

**Precedence**: explicit override > session state > keyword detection > default

## decision tree: depth calibration

```
How deep should questioning go?
├── User seems impatient? (short answers, "just do it")
│   └── shallow: 1-2 rounds, confirm and proceed
├── Simple/familiar task? (similar to past work)
│   └── shallow: 1-2 rounds, single question → confirm
├── New feature? (clear goal, some unknowns)
│   └── medium: 3-4 rounds, broad → narrow → edge cases → confirm
├── Architecture/design? (system-level, many stakeholders)
│   └── deep: 5-8 rounds, problem → constraints → options → trade-offs → meta
└── User explicitly requests depth?
    └── match requested depth
```

## decision tree: tool before question

```
Should I use a tool before asking?
├── Question is about preferences, priorities, or intent?
│   └── NO tools: ask directly (tools can't discover human intent)
├── User mentions a file/module?
│   └── YES: outline --callers=X or outline --search=X
├── User mentions "similar to" or "like before"?
│   └── YES: git log --oneline -10, outline --diff=HEAD~5
├── User mentions current work/task?
│   └── YES: linear issue list --assignee me
└── Could I discover the answer myself?
    └── YES: run tool first, then ask sharper question
```

**Note**: Intent questions (preferences, priorities, trade-offs) always go direct to user. Factual questions (what exists, what changed) go to tools first.

## decision tree: archetype selection

```
What question archetype fits?
├── Ambiguity in the request?
│   └── clarification
├── Multiple valid approaches?
│   └── preference or trade-off
├── Need to confirm an assumption?
│   └── confirmation
├── Scope is unclear or expanding?
│   └── scope
├── Multiple systems involved?
│   └── integration
├── Order of operations matters?
│   └── sequence
├── Core path known, need boundaries?
│   └── edge case
├── After 3-4 questions or drifting?
│   └── meta (synthesis)
└── Early-stage discovery?
    └── exploration
```

## decision tree: mode transition

```
Should I switch modes mid-conversation?
├── Started in explore, now have clear options?
│   └── transition to choose
├── Started in start, scope expanding?
│   └── transition to scope
├── Task implementation complete?
│   └── transition to review
├── User says "wait, let me think about..."?
│   └── pause, let them speak (OARS: affirm)
└── Confusion or frustration detected?
    └── meta question: "Should we step back?"
```

## OARS technique

Adapted from motivational interviewing (Miller & Rollnick, 2012):

| technique | application | example |
|-----------|-------------|---------|
| **Open questions** | start broad, invite elaboration | "What are you trying to achieve?" not "Do you want X?" |
| **Affirmations** | acknowledge what user shares | "That's a useful constraint" |
| **Reflective listening** | mirror back to confirm understanding | "So the priority is speed over flexibility?" |
| **Summarizing** | synthesize before proceeding | "So far: X, Y, Z. Does that capture it?" |

**Question stems to prefer** (NN/g):
- "Tell me about..."
- "What do you think about..."
- "How would you..."
- "What's the most important..."

**Question stems to avoid** (NN/g):
- Leading: "Don't you think..."
- Binary when open needed: "Is it X?" (vs "What is it?")
- Compound: "What about X and also Y?"

## mode: start

Session initiation - before loop or deep work.

```
round 1 (Open):
- "Which project?" (detect from cwd, offer recent)
- "What's the goal?" (detect from Linear in-progress)
- Affirmation: "That's a clear target."

round 2 (Reflective + Probe):
- "So the priority is [X] over [Y]?" (reflect back goal)
- "Is this the issue?" (if Linear detected)
- "Any constraints?" (time, scope, dependencies)
- "What does 'done' look like?" (definition of done)

round 3 (Summary + confirm):
- For monorepos: "Which package/subpath?" (e.g., packages/web vs packages/mobile)
- "Design considerations?" (trigger emil-kowalski if UI)
- Summary: "So we're doing X in Y with constraints Z. Ready to proceed?"
```

## mode: scope

Define boundaries - prevent scope creep.

```
round 1 (Open):
- "What's the minimum viable version?"
- "What's explicitly out of scope?"
- Affirmation: "Good boundary to draw."

round 2 (Reflective + Summary):
- "So the MVP is [X] and we're skipping [Y]?" (reflect back)
- "What's the success criteria?"
- "Any non-obvious constraints?"
```

## mode: explore

The classic deep-ask - Socratic elenchus pattern.

**Socratic structure** (Vlastos, 1983):
1. Elicit initial position
2. Probe with "what if" / edge cases
3. Surface contradictions or gaps
4. Guide toward refined understanding
5. Reach aporia (productive confusion) or clarity

**Depth based on complexity:**
- Simple: 1-2 rounds, single question → confirm
- Feature: 3-4 rounds, broad → narrow → edge cases → confirm
- Architecture: 5-8 rounds, problem → constraints → options → trade-offs → meta

**Funnel technique** (NN/g):
- Start broad: "What problem are you solving?"
- Narrow: "Which of these matters most?"
- Specific: "How should X handle Y?"

## decision tree: continue or stop

```
Should I keep asking?
├── User says "let's do it" or gives short answers?
│   └── stop and synthesize
├── Answers repeat the same theme?
│   └── stop and summarize
├── New dimensions or contradictions appear?
│   └── continue with targeted follow-up
├── 3-4 questions asked already?
│   └── ask a meta question, then decide
├── User engages deeply, long answers?
│   └── continue (change talk signal)
└── Otherwise
    └── continue one more round
```

## mode: choose

Quick decision between valid options.

```
single question:
- Present 2-4 options
- First is recommended (add "(Recommended)")
- Descriptions show trade-offs, not definitions
- Done in 1 round
```

## mode: review

Pre-completion validation.

```
round 1 (Open + Reflect):
- "Is this the behavior you expected?"
- Affirmation: "Good catch" or "Makes sense"
- "So you're seeing [X] and expecting [Y]?" (reflect discrepancy if any)
- "Any edge cases I should handle?"

round 2 (Closing):
- "Ready to commit/merge?"
- "Anything else before we ship?"
```

## context gathering (when applicable)

Before asking about **facts** (not preferences), understand the landscape:

```bash
layer .                           # architecture
outline --callers=X src/          # who uses X
git log --oneline -10             # recent activity
outline --diff=HEAD~3             # recent changes
linear issue list --assignee me   # current work
```

Never ask about things you could discover. But don't delay preference/priority questions waiting for tool output.

## tool → question mapping

Use tool output to sharpen questions:

```bash
# "auth module" mentioned
outline --callers=authenticate src/auth/

# "similar pattern" mentioned
outline --search=patternName src/

# "recent changes" mentioned
outline --diff=HEAD~5 --search=auth
```

## question design

- **headers**: 12 char max, tight chips ("auth method" not "authentication methodology")
- **options**: 2-4, first is recommended, describe implications not definitions
- **multi-select**: when choices aren't mutually exclusive
- **meta questions**: "does this feel right?", "what am I missing?"

## concrete values

| signal | value | grounding |
|--------|-------|-----------|
| options per question | 2-4 | NN/g: cognitive load research (primary) |
| header length | 12 chars max | heuristic: fits mobile UI chips |
| explore depth | 3-8 rounds | Socratic elenchus typical (primary) |
| meta checkpoint | after 3-4 questions | Vlastos: aporia checkpoint (primary) |
| funnel stages | 3 (broad→narrow→specific) | NN/g funnel technique (primary) |
| affirmation frequency | every 2-3 exchanges | heuristic: based on OARS guidance |
| async observation window | 5-10 min | heuristic: `references/conversation-patterns.md` |

**Legend**: "primary" = grounded in cited research; "heuristic" = practical guideline, adjust based on context

## synthesis checkpoint

After each round, summarize in 2-4 bullets and confirm (OARS: Summarizing):

```
so far:
- [signal 1]
- [signal 2]
- [constraint or preference]

ready to proceed, or dig deeper?
```

## handoff schema

When ask-deep completes, output structured context using the standard output contract:

```json
{
  "mode": "explore",
  "status": "success",
  "summary": "Clarified auth requirements through 3 rounds of questions. Key decisions: JWT with refresh tokens, offline-first, minimal dependencies.",
  "confidence": 8,
  "inputs": {
    "task": "clarify auth approach for mobile + web",
    "constraints": ["existing Clerk integration"]
  },
  "artifacts": [
    {
      "type": "analysis",
      "content": {
        "ask_deep_mode": "start",
        "rounds": 3,
        "signals": [
          "priority: speed over flexibility",
          "constraint: must work offline"
        ],
        "decisions": [
          {"question": "auth approach?", "answer": "JWT with refresh tokens"}
        ],
        "open_questions": ["exact error handling TBD"],
        "assumptions": ["user has network on first login"],
        "risks": ["offline-first may complicate sync"],
        "definition_of_done": "user can log in via email OTP and see dashboard",
        "repo_subpath": "packages/mobile"
      }
    }
  ],
  "sources": {
    "prompts": [],
    "files_read": ["convex/auth.ts"]
  },
  "assumptions": ["user has network on first login", "existing sessions remain valid"],
  "next_steps": ["loop skill for implementation"],
  "blockers": []
}
```

See `~/Developer/skills/.system/output-contract.md` for full schema.

Downstream skills should:
1. Check `open_questions` in artifact before proceeding
2. Validate `assumptions` early
3. Monitor `risks` during execution

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| asking blind | redundant questions | run tools first, then ask |
| wrong mode | mismatched depth | use auto-detection tree |
| ignoring signals | user frustration | stop and synthesize |
| shallow options | binary choices | offer 2-4 options with trade-offs |
| leading questions | biased responses | use open stems ("what" not "don't you think") |
| compound questions | cognitive overload | one topic per question |
| no affirmation | user feels unheard | acknowledge before next question |
| skipping synthesis | context drift | summarize every 2-3 rounds |
| tool-discoverable questions | wasted HIL | check if tool can answer first |
| premature closure | missed requirements | watch for engaged "change talk" signals |

## primary sources

| source | contribution | reference |
|--------|--------------|-----------|
| Vlastos (1983) | Socratic elenchus 5-step structure | "The Socratic Elenchus" |
| Miller & Rollnick (2012) | OARS technique, 4 processes | Motivational Interviewing, 3rd ed |
| Nielsen Norman Group | Funnel technique, question stems | "Open vs Closed Questions in UX Research" |

## tool integration

| tool | command | purpose |
|------|---------|---------|
| layer | `layer .` | understand architecture before asking |
| outline | `outline --callers=X`, `outline --search=X` | discover code context |
| git | `git log --oneline -10` | recent activity context |
| linear | `linear issue list --assignee me` | current work context |
| trails | `trails trail record` | question flow persistence |

### trails integration

persist question flows for pattern analysis:

```bash
# record ask-deep session
trails trail record --agent claude --new-trace --action completed \
  --task "ask-deep: $MODE - $TOPIC" --confidence $CONFIDENCE --json -q
```

**trails enables**:
- tracking question patterns over time
- identifying frequently unclear areas
- measuring clarification effectiveness

## references

- [references/question-archetypes.md](references/question-archetypes.md) - question types
- [references/conversation-patterns.md](references/conversation-patterns.md) - multi-turn flows
- [references/cli-context-gathering.md](references/cli-context-gathering.md) - tool integration
