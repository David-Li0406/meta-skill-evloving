---
description: "03b) External research (agent-assisted): web-search best practices for plan-adjacent topics and write them into DOC_PATH with sources."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-external-research-agent — $ARGUMENTS
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

Documentation-only (planning + research):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code and run read-only searches to extract the plan’s technology surface area (frameworks, patterns, constraints).
- You MUST use web research for best-practices where it is applicable outside this repo.
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line gates (must pass before external web research)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the doc before proceeding.

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
  - Set `external_research_grounding: done <YYYY-MM-DD>`.
  - Do NOT clear other fields (especially deep dive passes).
  - Preserve any existing timestamps if present; update only the field you are completing now.

What this prompt does (external research, not project trivia):
- Goal: strengthen DOC_PATH by anchoring plan-adjacent, generalizable topics in best-in-class external references and practices.
- This is NOT for project-specific internals (our API names, our endpoint semantics, our internal folder layout).
- This IS for plan-adjacent topics with broadly-accepted solutions, e.g.:
  - Flutter animation patterns (including reduce motion / disableAnimations behavior)
  - State machine patterns (Flutter/Dart or generally)
  - CI/build best practices (Flutter iOS/Android, caching, determinism)
  - Reliable concurrency/cancellation patterns
  - Testing strategies (unit/integration/e2e) that are framework-idiomatic

Relevance filter (anti-noise):
- Only research topics that satisfy BOTH:
  1) The plan (DOC_PATH) touches this area or will be blocked by it.
  2) The topic has broadly reusable/idiomatic external guidance.
- Skip topics that are clearly unique to our repo/product unless the topic generalizes (e.g., “event semantics” does not; “analytics schema design” might).

Output budget (avoid “research sprawl”):
- Aim for 2–5 topics total.
- For each topic: 3–7 high-quality sources max.
- Prefer primary sources: official docs, language/framework authors, widely-used libraries.
- If sources disagree: summarize the disagreement and pick a default recommendation (do not ask the user).

Subagents (agent-assisted external research; parallel web searches when beneficial)
- Use subagents to keep web-search exploration and source harvesting out of the main agent’s context.
- Spawn subagents in parallel only when they are disjoint and read-only.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files.
  - No questions: subagents must decide from DOC_PATH + public sources.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Do not spam/poll subagents; wait for completion, then integrate.
  - Close subagents once their results are captured.
- Main agent writes DOC_PATH and owns all synthesis/decisions.

Spawn subagents as needed (disjoint scopes; read-only):
1) Subagent: Topic researcher (web) — <Topic A>
2) Subagent: Topic researcher (web) — <Topic B>
3) Subagent: Topic researcher (web) — <Topic C>

Each topic subagent MUST output (markdown, nested lists; no tables):
- Topic: <name>
- Why it applies to this plan:
  - <bullets>
- Best practices (synthesized):
  - <bullets>
- Common pitfalls:
  - <bullets>
- Recommended default (what we should do here):
  - <bullets>
- Sources (high quality; include direct links):
  - <source title> — <url> — <why it’s relevant/authoritative>

Main-agent procedure (do this in order):
1) Read DOC_PATH fully.
2) Extract 2–5 candidate external-research topics from the plan:
   - Prefer topics where the plan is currently vague or where correctness/idiomatic-ness depends on known best practices.
3) Spawn parallel topic subagents (read-only) for the selected topics.
4) Integrate: synthesize results into a single coherent “External Research” block in DOC_PATH:
   - Include sources (links) and a short “how we apply this” per topic.
   - Avoid cargo-cult: always connect best practice → why it matters for THIS plan.
5) If research implies a plan change (new constraint, new sequencing, new contract), update DOC_PATH (and Decision Log if it changes an earlier decision).

DOC UPDATE RULES (anti-fragile; do NOT assume section numbers match the template)
Placement rule (in order):
1) If block markers exist, replace the content inside them:
   - `<!-- arch_skill:block:external_research:start -->` … `<!-- arch_skill:block:external_research:end -->`
2) Else, if the doc already has a section whose heading contains "External Research" or "Best Practices" or "References" (case-insensitive), update it in place.
3) Else, insert a new top-level section:
   - Prefer inserting after Research Grounding,
   - otherwise after Target Architecture,
   - otherwise after TL;DR/North Star.
Numbering rule:
- If the doc uses numbered headings, preserve numbering; do not renumber the rest of the document.
Do not paste the full inserted block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:external_research:start -->
# External Research (best-in-class references; plan-adjacent)

> Goal: anchor the plan in idiomatic, broadly-accepted practices where applicable. This section intentionally avoids project-specific internals.

## Topics researched (and why)
- <topic> — <why it applies>

## Findings + how we apply them

### <Topic A>
- Best practices (synthesized):
  - <bullet>
- Recommended default for this plan:
  - <bullet>
- Pitfalls / footguns:
  - <bullet>
- Sources:
  - <title> — <url> — <why it’s authoritative>

### <Topic B>
- Best practices (synthesized):
  - <bullet>
- Recommended default for this plan:
  - <bullet>
- Pitfalls / footguns:
  - <bullet>
- Sources:
  - <title> — <url> — <why it’s authoritative>

## Adopt / Reject summary
- Adopt:
  - <what we will do + where it impacts the plan>
- Reject:
  - <what we will not do + why>

## Open questions (ONLY if truly not answerable)
- <question> — evidence needed: <what would settle it>
<!-- arch_skill:block:external_research:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
