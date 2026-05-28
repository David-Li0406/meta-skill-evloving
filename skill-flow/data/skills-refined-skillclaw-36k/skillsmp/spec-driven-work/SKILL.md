---
name: Spec-Driven Work
description: Work on projects through well-defined specs. Spec-first approach with no ambiguity.
version: 1.5.0
---

# spec-driven-work

## Overview

Work on projects through well-defined specs. Every process gets specced, cross-referenced, and followed. Spec-first approach - no jumping to action. No ambiguity - when executing a spec, follow it literally with zero creativity.

**Two modes:**
1. **Spec Development** - Collaborative discussion to create/refine specs
2. **Spec Execution** - Follow existing spec literally, flag gaps

Modes blend fluidly: you might execute, hit a gap, develop spec to fill it, resume execution.

**Announce at start:** "Using spec-driven-work. Is there an existing spec for this, or are we developing one?"

---

## Core Principles

### 1. Discussion by Default

When user input is ambiguous, assume they want to discuss, not act.

**User says:** "the screenshot process needs work"
- **Wrong:** Start editing the screenshot process
- **Right:** "What's not working? The steps, the naming, something else?"

**User says:** "add priority to the table"
- **Wrong:** Add a Priority column with your best guess
- **Right:** "How should priority be defined?"

### 2. Define Before Use

Never use vague or undefined terms. If a concept isn't defined, define it first.

**Wrong:** "High priority = significant market presence"
**Right:** "How is priority defined? Proposal: High = 3+ sources, Medium = 2, Low = 1"

### 3. Propose, Show, Confirm

Never make changes without showing exactly what will change and getting confirmation.

**Pattern:**
1. State what you propose
2. Show the exact change (the actual text/code)
3. Ask for confirmation
4. Only then execute

### 4. One Thing at a Time

Don't bundle multiple changes or questions. Each message should address one thing.

**Wrong:** "I'll add the template, update the criteria, and fix the naming convention"
**Right:** "First, let's define the template. Here's what I propose: [show]. Does this work?"

### 5. Trace Decisions

Document why decisions were made, not just what was decided.

In specs, include rationale:
```markdown
**Priority criteria:**
- High: 3+ sources
- Medium: 2 sources
- Low: 1 source

> Rationale: Based purely on mention frequency. Simple, concrete, measurable.
```

### 6. Don't Assume, Verify

Never guess or infer. Always research and check.

- Need a command? Check the docs
- API returns data? Check the actual response, don't assume structure
- Build succeeded? Check the output, don't assume
- File exists? Verify, don't assume from context
- User says X is broken? Reproduce before fixing

### 7. Cross-Reference, Don't Duplicate

Link to existing specs instead of restating. Keep specs DRY.

**Wrong:** Copy the criteria into every research doc
**Right:** `> **Spec**: [../README.md](../README.md)`

### 8. Template Everything

If a process will repeat, create a template in the spec.

Templates should include:
- Structure with placeholders
- Example of filled-in version
- Where the template lives (which spec doc)

### 9. Log Everything (With Permission)

Log what's defined, ask about the rest.

**Log without asking:**
- What the skill explicitly requires (step completion, test results, bugs, status updates)

**Ask before logging:**
- Any action, decision, or finding not explicitly required
- Investigations, design decisions, context, side discoveries

**Pattern:**
- Do the work
- Ask: "Should I log [this finding/decision/investigation]?"
- If yes, log it; if no, move on

**Wrong:** Assume everything should be logged and document without asking
**Wrong:** Skip logging something potentially valuable without asking
**Right:** "I checked for similar issues in other files and found none. Should I log this investigation?"

---

## Spec Development Mode

When creating or refining specs through discussion.

### Process

1. **Understand scope** - What is this spec for? What processes does it cover?
2. **Work from example** - Start with a concrete case, then generalize
3. **Define terms** - Every term used must be defined
4. **Document structure** - Clear sections, cross-references
5. **Create templates** - For any repeatable process
6. **Confirm each section** - Don't move on until current section is agreed

### Spec Document Structure

```markdown
# [Spec Name]

[Brief description of what this spec covers]

## [Section 1]

### [Process/Concept Name]

[Definition or steps]

**Template** (if applicable):
```
[template here]
```

---

## [Section 2]
...
```

### Questions to Ask

When developing specs, actively ask:
- "How is [term] defined?"
- "What's the inclusion/exclusion criteria?"
- "Should this be a template?"
- "Where does this get documented?"
- "Is there an existing spec this should reference?"

### Research Tracking

When spec development requires research, track findings in a dedicated file.

**When to use:** Any spec development that involves investigation before the spec can be written.

**Before starting research:**
1. Ask the user where to track research (or propose a location)
2. Create the research file before starting any investigation
3. This is blocking - do not investigate until the file exists

**After each finding (not batched - immediately after each one):**

Update the research file with:
- **Finding** - Something you learned
- **Decision** - Something that was decided
- **Answer** - A question that got resolved

**Never batch updates.** Update the file immediately after each finding, not after multiple investigations.

**Research file format:**

```markdown
# Research Progress: [Project Name]

**Started:** [date]
**Status:** in-progress / complete

---

## Objective

[What is being researched and why. Capture the high-level goal and the key questions that need answering before the spec can be written. This ensures research can be resumed with full context if interrupted.]

---

## Defined Terms

| Term | Definition |
|------|------------|
| [term] | [definition] |

---

## Findings

### Finding 1: [Title]
**Date:** [date]

[What was discovered]

---

## Decisions

### Decision 1: [Title]
**Date:** [date]

**Decision:** [what was decided]
**Rationale:** [why]

---

## Open Questions

1. [Question still unanswered]
2. ~~[Answered question]~~ **ANSWERED:** [answer or reference to finding]
```

**Rules:**
- Update immediately, not in batches
- Strike through answered questions, add answer reference
- Link to research file from the final spec

---

## Spec Execution Mode

When following an existing spec to do work.

### Process

1. **Find the spec** - Locate relevant spec before starting work
2. **Follow literally** - Zero creativity, do exactly what spec says
3. **Flag gaps** - If spec doesn't cover something, stop and discuss
4. **Report in spec terms** - Use the spec's terminology and structure

### Progress Tracking

Document every completed step immediately after completion. This ensures execution state survives agent restarts and provides full visibility.

**Before starting execution:**
1. Check if the spec defines a progress file location
2. If not defined, ask the user where to track progress
3. Create the progress file before executing the first step

**After each step (not batched - immediately after each one):**

Update the progress file with:
- **Step** (required): Which step from the spec was completed
- **Status** (required): done / blocked / skipped
- **Result** (required): What happened (free text)
- **Files modified** (required if any): Work artifacts changed as deliverables of this step. Excludes the progress file itself, temp files, and logs.
- **Decisions made** (if any): Choices made during execution
- **Blockers/gaps** (if any): Why execution stopped

**Progress file format:**

```markdown
# Progress: [Spec Name]

**Spec:** [link to spec]
**Started:** [date]
**Status:** in-progress / completed / blocked

---

## Step 1: [Step name from spec]
- **Status:** done
- **Result:** [what happened]
- **Files modified:**
  - path/to/file.ts

## Step 2: [Step name from spec]
- **Status:** blocked
- **Result:** [what happened before blocking]
- **Blockers:** [why stopped]
```

**Rules:**
- Never batch updates - document immediately after each step
- Keep progress files permanently (do not delete on completion)
- Update status field at top when execution completes or blocks

### Verification Tracking

When the spec defines verification criteria (testing, review, validation), track results and issues in the progress file.

**After all steps complete, add a Verification section:**

```markdown
---

## Verification

### [Verification Type] (per spec)

**Date:** [date]

| Check | Result | Notes |
|-------|--------|-------|
| [check from spec] | PASSED / FAILED / - | [notes, issue reference if failed] |

### Issues Found

#### Issue 1: [Short description]
- **Status:** [see statuses below]
- **Found during:** [which check]
- **Symptom:** [what was observed]
- **Root cause:** [why it happened - after investigation]
- **Resolution:** [what was changed]
- **Artifacts modified:** [if applicable]
  - [list of files, documents, data, etc.]
```

**Issue statuses:**
- `investigating` - Issue identified, looking into root cause
- `resolution applied, pending verification` - Changes made, awaiting confirmation
- `resolved` - Verified after fix (ONLY after confirmed)
- `wont fix` - Intentional behavior or out of scope

**Rules:**
- Log issues immediately when identified (even before root cause is known)
- Update issue status as investigation progresses
- NEVER mark as "resolved" until verified - no inferring
- Use "resolution applied, pending verification" after applying a fix
- Update check results after issues are resolved and re-verified

### Executing Steps Directly

When executing steps directly (not via subagent):

1. Invoke the `spec-step-execution` skill
2. Execute the step following that skill
3. Re-invoke `spec-driven-work` skill to restore orchestration context

Re-invoking ensures this skill is fresh in context (not compacted) before continuing to next step.

### Orchestration with Subagents

Delegate step execution to `spec-step-executor` agents by default. The main process orchestrates; subagents execute.

**When to execute directly (exceptions):**

| Situation | Why |
|-----------|-----|
| Step requires user interaction mid-execution | Subagent can't interact with user |
| High ambiguity / gaps likely | Main process handles gaps with user |

**Parallel execution:**

The spec MUST explicitly define what can run in parallel:

```markdown
## Execution Mode

### Sequential
Steps 1-3 must execute in order.

### Parallel
Steps 4a, 4b, 4c can run in parallel (no shared state).
Wait for all before Step 5.
```

To launch parallel agents, use multiple Task tool calls in a single message:

```
[Task: spec-step-executor for step 4a]
[Task: spec-step-executor for step 4b]
[Task: spec-step-executor for step 4c]
```

**What to pass to subagents:**
- Spec file path
- Step number/name to execute
- Progress file path (if exists)
- Research file path (if exists)

**Main process responsibilities:**
- Decide subagent vs direct execution
- Launch subagents (parallel when spec allows)
- Update progress file with results (single writer)
- Handle gap responses from subagents

**Subagent result format:**

| Result | Meaning | Action |
|--------|---------|--------|
| SUCCESS | Step completed, verification passed | Update progress file, proceed to next step |
| FAILED | Step attempted but errored | Investigate error, retry or escalate to user |
| GAP | Spec doesn't cover this situation | Discuss with user, update spec if needed, re-dispatch or execute directly |

---

## Mode Transitions

| Situation | Mode | Action |
|-----------|------|--------|
| User gives clear action + spec exists | Execution | Follow spec |
| User gives clear action + no spec | Development | Create spec first |
| User asks question | Discussion | Discuss, don't act |
| User makes statement | Discussion | Clarify intent before acting |
| Gap found during execution | Development | Pause, fill gap, resume |
| Spec change needed during execution | Development | Propose change, confirm, update spec, resume |

---

## Anti-Patterns

**Don't do these:**

| Anti-Pattern | Instead |
|--------------|---------|
| Jump to editing when user mentions a file | Ask what they want to change |
| Use undefined terms ("market presence") | Define terms first |
| Bundle multiple changes | One change at a time |
| Assume file contents | Read the file |
| Guess at commands | Check documentation |
| Fill spec gaps silently | Flag gaps, discuss |
| Say "I'll do X, Y, and Z" | "First, let's address X. [details]. OK?" |

---

## Checklist

Before taking any action:
- [ ] Is there a spec for this? If yes, am I following it?
- [ ] If no spec, should I create one first?
- [ ] Have I defined all terms I'm using?
- [ ] Have I shown exactly what I'll change?
- [ ] Have I confirmed with user?
- [ ] Am I doing one thing, not multiple things?
