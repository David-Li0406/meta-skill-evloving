Below is a **copy-paste template** plus a **section playbook** (what goes in, why it exists, what “good” looks like, common failure modes).

---

## Architecture Planning Template (copy-paste)

````markdown
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
  - <test/harness OR instrumentation/log signature OR manual QA checklist> — <pass/fail signal>
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
````

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
* Test plan:
* Exit criteria:
* Rollback:

## Phase 1 — <foundation>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

---

# 8) Test Strategy (common-sense; non-blocking)

> Principle: avoid “proof ladders.” Prefer the smallest existing signal. If sim/video/screenshot capture is flaky or slow, rely on targeted instrumentation + a short manual QA checklist and keep moving.

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

````

---

## How to write each section (quality bar + examples)

### 0) Holistic North Star
**Why it matters:** This prevents “big doc, vague outcome.” Your plan becomes testable, and scope creep becomes visible.

**What good looks like**
- One falsifiable claim + crisp scope.
- “Done” is measurable via explicit evidence (tests/instrumentation/QA), not vibes.
- Stop-the-line invariants (fail fast on contract drift).

**Example pattern**
- A tight “prove/disprove the claim” north star with explicit scope and “treat failures as contract bugs, not tuning problems” is exactly what makes the rest of the plan coherent.

**Common failure modes**
- Outcome is a vibe (“make it better”).
- Scope includes everything (“and also…”) so no decision is irreversible.
- No stop-the-line rules → you end up tuning around a wiring bug.

---

### 1) Key Design Considerations
**Why it matters:** This is your “weighting function.” When tradeoffs appear (they will), you already know what wins.

**What good looks like**
- Ranked priorities (forced order).
- Constraints split into: correctness, perf, offline/latency, compatibility, ops.
- Explicit tradeoffs with rejected alternatives (so reviewers don’t relitigate).

**Example pattern**
- “Fail-loud boundaries,” “single source of truth,” and “no business logic in widgets” as non-negotiables make later refactors safe and reviewable.

---

### 2) Problem Statement with existing architecture
**Why it matters:** Forces you to articulate the real system you’re changing (and why).

**What good looks like**
- “What exists today” described in terms of: surfaces, flows, ownership, and known gaps.
- Problems stated as concrete symptoms and missing behaviors, not “this code is messy.”

**Example pattern**
- A problem statement that enumerates what’s present (files, screens, repositories) and what parity/behavior is missing keeps the work anchored.

---

### 3) Research Grounding (external + internal ground truth)
**Why it matters:** Prevents “inventing a new religion.” Also prevents wasting time re-debating decisions already settled in code.

**What good looks like**
- Two distinct lists:
  - **External anchors** (papers/systems/prior art) with a short “what we adopt / reject.”
  - **Internal ground truth**: file paths that are the spec (or the reference implementation).
- Open questions framed as “what evidence would settle this.”

**Example patterns**
- Parity plans that explicitly define *ground truth as the other runtime* and list the authoritative code anchors avoid endless subjective debate. 

---

### 4) Current Architecture (as-is)
**Why it matters:** Reviewers can’t validate a migration path unless the “before” is precise.

**What good looks like**
- **On-disk tree**: only the relevant subtree, not the whole repo.
- **Control paths**: the 2–4 flows that matter, written as step chains.
- **Object model**: what owns state, who calls whom, what is public API vs internal.
- **Failure behavior**: current logging, current fallbacks, current invariants (and where they’re violated).
- **UI work:** include ASCII mockups of current states (to anchor reality).

**Example snippet**
```text
apps/mobile/lib/features/<feature>/
  data/ ...
  domain/ ...
  presentation/ ...
````

That kind of “tree as contract” is what makes later call-site audits and phased plans deterministic.

---

### 5) Target Architecture (to-be)

**Why it matters:** If you can’t draw the destination, the “plan” becomes a pile of local diffs.

**What good looks like**

* Same structure as current architecture, but for the future:

  * future tree
  * future flows
  * new abstractions + explicit public API surfaces
  * invariants/boundaries
  * ASCII mockups for target UI states (if UI work)
* Migration notes: what changes for callers.

**Example pattern**

* “Centralized navigation API,” “pure policy modules,” “runner state machine,” “contracts decoupled from visuals/touch” are examples of target architecture that remain stable even as UI changes.

---

### 6) Call-Site Audit (exhaustive)

**Why it matters:** This is where plans stop being aspirational and start being executable.

**The required table**

| File | Symbol/call | What it does today | Change | Why | New API | Tests |
| ---- | ----------- | ------------------ | ------ | --- | ------- | ----- |

**What good looks like**

* Exhaustive inventory. No “we’ll find them later.”
* Every row references **ground truth** (link to file path, and ideally the exact function).
* Every row states the new contract it will consume.

**Example pattern**

* Plans that explicitly list touch points per phase and include “grep-style repo audits” to prove ghosts are gone dramatically reduce regressions.

---

### 7) Depth-First phased implementation plan (authoritative)

**Why it matters:** This is how you avoid boiling the ocean and how you keep correctness intact while moving fast.

**What good looks like**

* Many small phases > a few huge phases.
* Each phase has:

  * Goal (one sentence)
  * Work (concrete)
  * Test plan (commands + what they prove)
  * Exit criteria (objective)
  * Rollback story

**Example pattern**

* A phase list that starts with “baseline gates,” then “fail-loud routing/args,” then “strict loaders + schema validation,” then “single source of truth repository,” then “UI parity,” then “telemetry,” then “QA sweep + cleanup” is the canonical depth-first shape.

---

### 8) Test Strategy (beyond per-phase tests)

**Why it matters:** Per-phase tests prevent regressions; the global test strategy prevents *category* failures.

**What good looks like**

* Unit tests lock pure contracts (parsers, policies, planners).
* Integration tests lock flows and boundary wiring.
* Failure-injection / offline chaos tests exist as a first-class spec (not “we should test offline someday”).
* Artifacts captured on failure (logs/snapshots) so debugging doesn’t require reruns.

**Example pattern**

* A two-tier testing strategy (hermetic + full-stack) with a scenario DSL and artifact requirements is the cleanest way to make “offline-first correctness” real. 

---

### 9) Rollout / Ops / Telemetry

**Why it matters:** Most “architecture wins” die in rollout: silent drift, missing telemetry, no runbook.

**What good looks like**

* Explicit flagging strategy (if applicable).
* Telemetry events and schemas called out *before* you implement them.
* Debug runbook: “if metric X spikes, check Y, inspect Z.”

**Example pattern**

* Parity plans that treat telemetry as a phase (not an afterthought) avoid shipping “works locally” features with no observability. 

---

### 10) Decision Log (append-only)

**Why it matters:** It stops circular debate and preserves reasoning when future you forgets.

**What good looks like**

* Short ADR-style entries:

  * Context → Options → Decision → Consequences
* Dated and append-only.

**Example pattern**

* North-star docs that enforce “hypothesis / rationale / lever” before runs are basically decision logs for experimentation.

---

## (Optional) Reference examples from your existing docs

If you want concrete models of “great execution” of these sections:

* Puzzles phased parity plan (excellent phased plan + invariants + call-site discipline): 
* Skia UX fidelity parity plan (clear parity definition + verification pack idea): 
* Lessons parity alignment plan (delta tables + phased layers): 
* Offline-first failure testing plan (scenario DSL + hermetic/full-stack tiers): 
* Stack-domain north star (falsifiable claim + stop-the-line invariants): 
* Stack-session north star (contract strictness + runtime enforcement framing): 
