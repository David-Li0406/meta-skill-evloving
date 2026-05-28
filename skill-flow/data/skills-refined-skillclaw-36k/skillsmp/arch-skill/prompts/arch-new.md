---
description: "01) New doc: create canonical plan doc + draft North Star from blurb, then confirm with user."
argument-hint: "<Paste the change request / symptoms / goal. This becomes the draft TL;DR + North Star. No structured args needed.>"
---
# /prompts:arch-new — $ARGUMENTS
# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Use the freeform blurb provided after the command ($ARGUMENTS) as the working intent.
Create a new architecture document in `docs/` using the template below.
Name the file yourself using this rule:
- `docs/<TITLE_SCREAMING_SNAKE>_<DATE>.md`
- TITLE_SCREAMING_SNAKE = derived from the blurb as a short 5–9 word title, uppercased, spaces → `_`, punctuation removed.
- DATE = today's date in YYYY-MM-DD (no user input required).
Example: blurb="Redesign replay phase machine to be SSOT"
→ `docs/REDESIGN_REPLAY_PHASE_MACHINE_TO_BE_SSOT_2026-01-16.md`
Apply the **single-document rule**: all planning and decisions live in this doc.
Do not create additional planning docs.
Documentation-only (planning):
- This prompt creates/edits docs only. DO NOT modify code.
- Do not commit/push unless explicitly requested in $ARGUMENTS.
CRITICAL: The North Star MUST be correct.
- Draft the TL;DR and Section 0 (Holistic North Star) from $ARGUMENTS (do not leave placeholders there).
- Then STOP and ask the user to confirm/correct the North Star before proceeding to research/architecture execution.
- If the user provides edits, update the doc and re-ask for confirmation until the user says “yes”.

Write the filled template into the new doc file. Do not paste the full document to the console (you may print only the drafted TL;DR + North Star for confirmation).

DOCUMENT CONTENT FORMAT (write to the new doc file):

---
title: "<PROJECT> — <CHANGE> — Architecture Plan"
date: <YYYY-MM-DD>
status: draft | active | complete
owners: [<name>, ...]
reviewers: [<name>, ...]
doc_type: architectural_change | parity_plan | phased_refactor | new_system
related:
  - <links to other docs, PRs, designs>
---

# TL;DR

- **Outcome:** <one sentence, falsifiable>
- **Problem:** <one sentence>
- **Approach:** <one sentence>
- **Plan:** <phases in 1–2 lines>
- **Non-negotiables:** <3–7 bullets>

---

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: not started
external_research_grounding: not started
deep_dive_pass_2: not started
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This is a warn-first checklist only. It should not hard-block execution.
-->
<!-- arch_skill:block:planning_passes:end -->

---

# 0) Holistic North Star

## 0.1 The claim (falsifiable)
> <If we do X, then Y is true, measured by Z, by date/condition W>

## 0.2 In scope
- UX surfaces (what users will see change):
  - <screen/state/flow>
- Technical scope (what code will change):
  - <module/contract/boundary>

## 0.3 Out of scope
- UX surfaces (what users must NOT see change):
  - <screen/state/flow>
- Technical scope (explicit exclusions):
  - <module/boundary we will not touch>

## 0.4 Definition of done (acceptance evidence)
- <observable acceptance criteria, not vibes>
- Evidence plan (common-sense; non-blocking):
  - Primary signal (keep it minimal; prefer existing tests/checks): <existing test/check OR instrumentation/log signature OR manual QA checklist> — <pass/fail signal>
  - Optional second signal (only if needed): <...> — <pass/fail signal>
  - Default: do NOT add bespoke screenshot harnesses / drift scripts unless they already exist in-repo or are explicitly requested.
- Metrics / thresholds (if relevant):
  - <metric>: <threshold> — measured via <dash/test/log>

## 0.5 Stop-the-line invariants
- <if these fail, we stop and fix before continuing>
- Example: “No silent fallbacks.” “No dual sources of truth.” “No undefined behavior.”

---

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)
1) <#1>
2) <#2>
3) <#3>

## 1.2 Constraints
- Correctness:
- Performance:
- Offline / latency:
- Compatibility / migration:
- Operational / observability:

## 1.3 Architectural principles (rules we will enforce)
- <e.g., fail-loud boundaries, DI rules, no business logic in UI, etc.>

## 1.4 Known tradeoffs (explicit)
- <tradeoff> → chosen direction + why
- Alternatives rejected + why

---

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today
- <system overview in 5–10 bullets>
- Primary flows / control paths:
  - <flow A>
  - <flow B>

## 2.2 What’s broken / missing (concrete)
- Symptoms:
- Root causes (hypotheses):
- Why now:

## 2.3 Constraints implied by the problem
- <constraints derived from reality, not preference>

---

# 3) Research Grounding (external + internal “ground truth”)

## 3.1 External anchors (papers, systems, prior art)
- <source> — <what we borrow / what we reject> — <why it applies>

## 3.2 Internal ground truth (code as spec)
- **Authoritative behavior anchors (do not reinvent):**
  - `<path>` — <what it defines>
- **Existing patterns we will reuse:**
  - `<path>` — <pattern>

## 3.3 Open questions from research
- Q1:
- Q2:
- What evidence would settle them:

---

# 4) Current Architecture (as-is)

## 4.1 On-disk structure
```text
<tree of relevant dirs/files>
```

## 4.2 Control paths (runtime)

* Flow A:

  * Step 1 → Step 2 → Step 3
* Flow B:

  * ...

## 4.3 Object model + key abstractions

* Key types:
* Ownership boundaries:
* Public APIs:

  * `Foo.doThing(args) -> Result`

## 4.4 Observability + failure behavior today

* Logs:
* Metrics:
* Failure surfaces:
* Common failure modes:

## 4.5 UI surfaces (ASCII mockups, if UI work)

```ascii
<ASCII mockups for current UI states, if relevant>
```

---

# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

```text
<new/changed tree>
```

## 5.2 Control paths (future)

* Flow A (new):
* Flow B (new):

## 5.3 Object model + abstractions (future)

* New types/modules:
* Explicit contracts:
* Public APIs (new/changed):

  * `Foo.doThingV2(args) -> Result`
  * Migration notes:

## 5.4 Invariants and boundaries

* Fail-loud boundaries:
* Single source of truth:
* Determinism contracts (time/randomness):
* Performance / allocation boundaries:

## 5.5 UI surfaces (ASCII mockups, if UI work)

```ascii
<ASCII mockups for target UI states, if relevant>
```

---

# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)

| Area     | File   | Symbol / Call site | Current behavior | Required change | Why         | New API / contract | Tests impacted |
| -------- | ------ | ------------------ | ---------------- | --------------- | ----------- | ------------------ | -------------- |
| <module> | <path> | <fn/cls>           | <today>          | <diff>          | <rationale> | <new usage>        | <tests>        |

## 6.2 Migration notes

* Deprecated APIs:
* Compatibility shims (if any):
* Delete list (what must be removed):

---

# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit test plan.

## Phase 0 — Baseline gates

* Goal:
* Work:
* Test plan (smallest signal):
* Exit criteria:
* Rollback:

## Phase 1 — <foundation>

* Goal:
* Work:
* Test plan (smallest signal):
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Test plan (smallest signal):
* Exit criteria:
* Rollback:

---

# 8) Test Strategy (common-sense; non-blocking)

> Principle: avoid verification bureaucracy. Prefer the smallest existing signal. If sim/video/screenshot capture is flaky or slow, rely on targeted instrumentation + a short manual QA checklist and keep moving.
> Default: 1–3 checks total. Do not invent new harnesses/frameworks/scripts unless they already exist in-repo and are the cheapest guardrail.

## 8.1 Unit tests (contracts)

* What invariants are unit-locked:

## 8.2 Integration tests (flows)

* Critical flows:
* Failure injection:

## 8.3 E2E / device tests (realistic)

* Scenarios:
* Evidence / artifacts (optional; do not block):

---

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

* Flags / gradual rollout:
* Backward compatibility:

## 9.2 Telemetry changes

* New events:
* New properties:
* Dashboards / alerting:

## 9.3 Operational runbook

* Debug checklist:
* Common failure modes + fixes:

---

# 10) Decision Log (append-only)

## <YYYY-MM-DD> — <decision title>

* Context:
* Options:
* Decision:
* Consequences:
* Follow-ups:


---

CONSOLE OUTPUT (Amir-style; north star confirmation):
<1 line north star reminder (what we’re trying to accomplish overall)>
<1 line punchline (what you need from Amir right now)>
- Doc created: <path>
- Draft TL;DR (high level):
  - Outcome: <one sentence>
  - Problem: <one sentence>
  - Approach: <one sentence>
  - Plan: <1–2 lines>
- Draft North Star (for confirmation):
  - Claim: <one sentence>
  - In scope: <tight bullets>
  - Out of scope: <tight bullets>
  - Definition of done: <observable acceptance evidence>
  - Stop-the-line invariants: <3–7 bullets>
- Need from Amir: confirm “yes/no”. If “no”, paste edits to the claim + scope + DoD + invariants.
