---
description: "04a) Deep dive (agent-assisted): current-target architecture + call-site audit with subagents."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-deep-dive-agent — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):

- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.

# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Subagents (agent-assisted deep dive; use when the repo surface is large)
- Use subagents when call-site inventory, current-architecture mapping, or consolidation sweep is large enough that doing it inline will blow up context.
- Do NOT use subagents for small/simple docs; do the work directly.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files or run destructive commands.
  - Shared environment: avoid commands that generate/overwrite artifacts; prefer pure read/search.
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Do not spam/poll subagents with “are you done?”; wait for completion, then integrate.
- Main agent owns all decisions + writes DOC_PATH. If subagents disagree, resolve by reading more code (do not ask the user).

Spawn subagents as needed (disjoint scopes):
1) Subagent: Call-Site Sweeper (read-only)
   - Task: enumerate ALL call sites for symbols/APIs named in DOC_PATH (and obvious near-neighbors discovered in code).
   - Output format (bullets only):
     - <path> — <symbol> — <why it is a call site> — <current behavior>
2) Subagent: Current Architecture Mapper (read-only)
   - Task: summarize as-is architecture from repo code (tree, control paths, ownership, failure behavior).
   - Output format (sections only):
     On-disk structure:
     <tree>
     Control paths:
     - <flow>
     Object model + key abstractions:
     - <item>
     Observability + failure behavior:
     - <item>
3) Subagent: Pattern Consolidation Sweep (read-only)
   - Task: find other areas that should adopt the new central pattern (SSOT/contract/etc.).
   - Output format (table only):
     | Area | File / Symbol | Pattern to adopt | Why | Scope impact |

Close subagents once their results are captured. If a subagent is mis-scoped, interrupt/redirect sparingly.


Documentation-only (planning):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code and run read-only searches to ground the architecture and call-site audit.
- If you discover code changes we likely need, capture them in DOC_PATH (call-site audit + phase plan), with file anchors (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line: North Star Gate (must pass before current/target architecture + call-site audit)
- Falsifiable + verifiable: the North Star states a concrete claim AND the smallest credible pass/fail signal (prefer existing tests/checks; otherwise minimal instrumentation/log signature; otherwise a short manual checklist). Do NOT invent new harnesses/screenshot frameworks or drift scripts by default.
- Bounded + coherent: the North Star clearly states in-scope + out-of-scope and does not contradict the TL;DR/plan.
If the North Star Gate does not pass, STOP and ask the user to fix/confirm the North Star in the doc before proceeding.

Stop-the-line: UX Scope Gate (must pass before current/target architecture + call-site audit)
- The doc explicitly states UX in-scope and UX out-of-scope: what screens/states/behaviors change vs do NOT change.
- UX scope is coherent with the North Star and does not silently expand.
If the UX Scope Gate does not pass, STOP and ask the user to fix/confirm scope in the doc before proceeding.

Warn-first planning passes (soft sequencing guard; do NOT hard-block)
- If DOC_PATH contains `<!-- arch_skill:block:planning_passes:start -->` … `<!-- arch_skill:block:planning_passes:end -->`, keep it updated.
- If missing, insert a new planning passes block near the top of the doc:
  - Prefer inserting after the TL;DR section if present,
  - otherwise after YAML front matter,
  - otherwise at the top of the document.
- Planning passes block format (use exactly this shape; update fields in-place):
  - `<!-- arch_skill:block:planning_passes:start -->`
  - `<!--`
  - `arch_skill:planning_passes`
  - `deep_dive_pass_1: <not started|done YYYY-MM-DD>`
  - `external_research_grounding: <not started|done YYYY-MM-DD>`
  - `deep_dive_pass_2: <not started|done YYYY-MM-DD>`
  - `recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement`
  - `-->`
  - `<!-- arch_skill:block:planning_passes:end -->`
- Update rules (additive; never wipe progress):
  - If external research grounding exists in DOC_PATH (block marker or an "External Research" section), set:
    - `deep_dive_pass_2: done <YYYY-MM-DD>`
  - Else set:
    - `deep_dive_pass_1: done <YYYY-MM-DD>`
  - Do NOT clear other fields (especially `external_research_grounding`).
  - Preserve any existing timestamps if present; update only the field(s) you are completing now.

You are designing architecture. Produce/update THREE artifacts in DOC_PATH:
1) Current architecture (as-is): on-disk tree, 2–4 primary control paths, ownership boundaries, failure behavior.
2) Target architecture (to-be): future tree, future flows, explicit new/changed contracts, invariants/boundaries.
3) Call-site audit: exhaustive inventory of what changes where (and why), grounded in code.

Hard rules (drift-proof):
- Code is ground truth: every claim is anchored in file paths (include symbols when helpful).
- No competing sources of truth: prefer centralized contracts/primitives; delete/avoid parallel implementations.
- Do not ask the user technical questions you can answer by reading code; go look and decide.
- If multiple viable technical approaches exist, pick the most idiomatic default and note alternatives in the doc (do not ask “what do you want to do?”).

Pattern Consolidation Sweep (anti-blinders; scoped by the plan)
- If this design introduces/updates a central pattern (SSOT, lifecycle primitive, layout contract, policy resolver, etc.), look for other places that should adopt it.
- Capture candidates with file paths and your default recommendation: include in this plan vs defer (follow-up) vs exclude.
- Treat the plan’s scope as authoritative. Do NOT ask the user to re-decide scope here.
  - If a candidate is in-scope: mark it include and proceed.
  - If it expands scope: default to defer/exclude (and proceed). Do not block.
  - Only stop+ask if the plan’s scope/North Star is internally contradictory (i.e., required work is declared out-of-scope).

DOC UPDATE RULES (anti-fragile; do NOT assume section numbers match the template)
Placement rule (in order):
1) If block markers exist, replace the content inside them:
   - `<!-- arch_skill:block:current_architecture:start -->` … `<!-- arch_skill:block:current_architecture:end -->`
   - `<!-- arch_skill:block:target_architecture:start -->` … `<!-- arch_skill:block:target_architecture:end -->`
   - `<!-- arch_skill:block:call_site_audit:start -->` … `<!-- arch_skill:block:call_site_audit:end -->`
2) Else, update in place if semantically matching headings exist (case-insensitive match):
   - Current: "Current Architecture", "As-is"
   - Target: "Target Architecture", "To-be"
   - Audit: "Call-Site Audit", "Change map", "Change inventory"
3) Else, insert missing top-level sections:
   - Prefer inserting after research/problem sections,
   - and before phased plan / test strategy / rollout sections.
Numbering rule:
- If the doc uses numbered headings ("# 4) ..."), preserve existing numbering; do not renumber the rest of the document.
Do not paste the full inserted blocks to the console.

DOCUMENT CONTENT SKELETON (adapt to existing headings; do not blindly paste duplicates)
<!-- arch_skill:block:current_architecture:start -->
# Current Architecture (as-is)

## On-disk structure
```text
<tree of relevant dirs/files>
```

## Control paths (runtime)
* Flow A:
  * Step 1 → Step 2 → Step 3
* Flow B:
  * ...

## Object model + key abstractions
* Key types:
* Ownership boundaries:
* Public APIs:
  * `Foo.doThing(args) -> Result`

## Observability + failure behavior today
* Logs:
* Metrics:
* Failure surfaces:
* Common failure modes:

## UI surfaces (ASCII mockups, if UI work)
```ascii
<ASCII mockups for current UI states, if relevant>
```
<!-- arch_skill:block:current_architecture:end -->

---

<!-- arch_skill:block:target_architecture:start -->
# Target Architecture (to-be)

## On-disk structure (future)
```text
<new/changed tree>
```

## Control paths (future)
* Flow A (new):
* Flow B (new):

## Object model + abstractions (future)
* New types/modules:
* Explicit contracts:
* Public APIs (new/changed):
  * `Foo.doThingV2(args) -> Result`
  * Migration notes:

## Invariants and boundaries
* Fail-loud boundaries:
* Single source of truth:
* Determinism contracts (time/randomness):
* Performance / allocation boundaries:

## UI surfaces (ASCII mockups, if UI work)
```ascii
<ASCII mockups for target UI states, if relevant>
```
<!-- arch_skill:block:target_architecture:end -->

---

<!-- arch_skill:block:call_site_audit:start -->
# Call-Site Audit (exhaustive change inventory)

## Change map (table)
| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| <module> | <path> | <fn/cls> | <today> | <diff> | <rationale> | <new usage> | <tests> |

## Migration notes
* Deprecated APIs:
* Compatibility shims (if any):
* Delete list (what must be removed):

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)
| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| <area> | <path> | <pattern> | <reason> | <include/defer/exclude> |
<!-- arch_skill:block:call_site_audit:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
