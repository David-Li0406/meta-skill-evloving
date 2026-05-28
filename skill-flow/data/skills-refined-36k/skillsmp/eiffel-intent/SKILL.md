---
name: eiffel-intent
description: Phase 0 of Eiffel Spec Kit. Generates intent.md capturing WHAT users need and WHY. Runs AI-assisted intent review with probing questions. Use with /eiffel.intent command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.intent - Phase 0: Intent Capture

**Purpose:** Capture WHAT users need and WHY before any code is written.

## Usage

```
/eiffel.intent <project-path>
```

**Example:**
```
/eiffel.intent d:\prod\simple_cache
```

If no path provided, ask user: "Which project? Provide the full path (e.g., d:\prod\simple_cache)"

## Project Scoping

All files are created inside the PROJECT directory:
```
<project-path>/
├── .eiffel-workflow/
│   ├── intent.md
│   ├── intent-v2.md (after review)
│   ├── prompts/
│   │   └── phase0-intent-review.md  (prompt for external AI)
│   └── evidence/
│       └── phase0-intent.txt
├── src/
├── test/
└── <project>.ecf
```

## Workflow

### Step 1: Create Directory Structure

```bash
mkdir -p <project-path>/.eiffel-workflow/prompts
mkdir -p <project-path>/.eiffel-workflow/evidence
```

### Step 2: Generate Initial intent.md

Ask the user to describe what they want to build. Create `<project-path>/.eiffel-workflow/intent.md`:

```markdown
# Intent: [Library/Feature Name]

## What
[Clear description of what this does]

## Why
[Business/technical reason this is needed]

## Users
[Who will use this and how]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Out of Scope
[What this explicitly does NOT do]

## Dependencies (REQUIRED - simple_* First Policy)

**RULE:** Always prefer simple_* libraries over ISE EiffelStudio stdlib and Gobo.

| Need | simple_* Library | AVOID |
|------|------------------|-------|
| JSON | simple_json | $ISE_LIBRARY/contrib/library/web/framework/ewf/text/json |
| HTTP | simple_http | Gobo HTTP, EiffelNet |
| XML | simple_xml | $ISE_LIBRARY/library/xml |
| Regex | simple_regex | Gobo regex |
| Process | simple_process | $ISE_LIBRARY/library/process |
| Encoding | simple_encoding | Gobo encoding |
| CSV | simple_csv | Custom parsing |
| Config | simple_config | Custom INI parsing |
| Math | simple_math | Custom math |
| MML | simple_mml | ETH base2 |

**Only ISE allowed (no simple_* equivalent):**
- `base` - fundamental types
- `time` - DATE, TIME, DATE_TIME
- `testing` - EQA_TEST_SET

**List your dependencies:**

| Need | Library | Justification |
|------|---------|---------------|
| [capability needed] | simple_* | [why this one] |
| [capability needed] | ISE only if no simple_* | [gap identified] |

**If ISE/Gobo required:** Document the gap for potential simple_* development.

## MML Decision (REQUIRED)

**Does this library need MML model queries for precise postconditions?**

| Answer | When to Choose |
|--------|----------------|
| **YES - Required** | Library has collections (HASH_TABLE, ARRAYED_LIST, etc.) that need frame conditions |
| **YES - Optional** | Users may add MML postconditions to their extensions |
| **NO** | Pure computation, no internal collections, simple value types |

**If YES:** simple_mml will be added in Phase 1. Model queries will be mandatory for collections.

**Decision:** [YES-Required / YES-Optional / NO]
**Rationale:** [Brief explanation]
```

### Step 3: Generate AI Review Prompt File (MANUAL CYCLE)

Create `<project-path>/.eiffel-workflow/prompts/phase0-intent-review.md`:

```markdown
# Intent Review Request

**Instructions:** Review the intent document below and generate probing questions
to clarify vague language, identify missing requirements, and surface implicit assumptions.

## Review Criteria

Look for:
1. **Vague language:** Words like "fast", "secure", "easy", "flexible" without concrete definitions
2. **Missing edge cases:** What happens with empty input? Maximum size? Invalid data?
3. **Untestable criteria:** Are acceptance criteria specific and measurable?
4. **Hidden dependencies:** What external systems or libraries are assumed?
5. **Scope ambiguity:** Is "out of scope" clearly defined?

## Output Format

Provide 5-10 probing questions. For each:
- Quote the vague phrase
- Explain why it's vague
- Offer 2-3 concrete alternatives the user can choose from

---

## Intent Document to Review

[PASTE CONTENTS OF intent.md HERE]
```

### Step 3b: Auto-Create Evidence Placeholder File

Create `<project-path>/.eiffel-workflow/evidence/phase0-ai-review.md` with placeholder:

```markdown
# Phase 0: AI Review Response

**STATUS: INCOMPLETE** - Paste AI review response below this line and delete this section.

---

## Instructions

1. Open: `../.eiffel-workflow/prompts/phase0-intent-review.md`
2. Paste intent.md contents where indicated
3. Submit to an external AI (Ollama, Grok, Gemini, or another Claude session)
4. Replace this entire file with the AI's response
5. Return to Claude Code and say "review complete"

---

[AI RESPONSE GOES HERE]
```

### Step 4: Notify Human

Display:
```
PHASE 0: Intent document created.

FILES CREATED:
  - <project-path>/.eiffel-workflow/intent.md
  - <project-path>/.eiffel-workflow/prompts/phase0-intent-review.md
  - <project-path>/.eiffel-workflow/evidence/phase0-ai-review.md (placeholder - needs your input)

MANUAL ACTION REQUIRED:
  1. Open: <project-path>/.eiffel-workflow/prompts/phase0-intent-review.md
  2. Copy the intent.md content into the prompt where indicated
  3. Submit to an AI reviewer (Ollama, Grok, Gemini, or another Claude session)
  4. Replace contents of: <project-path>/.eiffel-workflow/evidence/phase0-ai-review.md with AI's response
  5. Return here and say "review complete" with any answers to the questions

Waiting for your input...
```

**BLOCK until user provides the review results.**

### Step 5: Process Review Results

When user returns with AI review:
1. Read the probing questions from the AI
2. Ask user to answer each question
3. Create `<project-path>/.eiffel-workflow/intent-v2.md` incorporating answers

### Step 5b: Dependency Audit (simple_* First)

**Before finalizing intent-v2.md, audit all dependencies:**

1. **Check each dependency against simple_* ecosystem:**
   ```
   Task(subagent_type=Explore) → "List all simple_* libraries and their purposes"
   ```

2. **For each ISE/Gobo dependency identified:**
   - Research if a simple_* equivalent exists
   - If no equivalent: document the gap
   - Add to intent-v2.md under "Gaps for Future simple_* Libraries"

3. **If gap identified, create recommendation:**
   ```markdown
   ## Gaps Identified (Potential simple_* Libraries)

   | Gap | Current Workaround | Proposed simple_* |
   |-----|-------------------|-------------------|
   | [capability] | ISE/Gobo [library] | simple_[name] |

   **Recommendation:** After shipping this library, consider creating simple_[name] to fill this gap.
   ```

**This ensures:**
- No ISE/Gobo usage without explicit justification
- Gaps are documented for future ecosystem growth
- simple_* ecosystem expands based on real needs

### Step 6: Final Approval

Ask: **"Intent document refined. Approve to proceed to Phase 1 (Contracts)?"**

**BLOCK until user explicitly approves.**

### Step 7: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase0-intent.txt`:
```
# Phase 0 Intent Evidence
# Project: <project-path>
# Date: [timestamp]

Intent document: .eiffel-workflow/intent-v2.md
AI review conducted: [yes/no]
AI used for review: [Ollama/Grok/Gemini/Claude/other]
Questions answered: [count]
User approved: [yes/no]

# Status: APPROVED
```

## Completion

When user approves:
```
Phase 0 COMPLETE: Intent captured and approved.
Project: <project-path>

Next: Run /eiffel.contracts <project-path> to generate contract skeletons.
```

## Context Management (RLM Pattern)

This skill focuses ONLY on: `<project-path>`

**DO NOT:**
- Read files outside this project directory
- Load entire ecosystem or multiple libraries into context
- Keep large file contents in working memory

**DO:**
- Use Task tool with Explore agent for ecosystem questions
- Ask targeted questions: "What does simple_mml provide?" not "Show me all files"
- Release context after getting answers

**Example - Ecosystem Query:**
```
Need to know about a dependency? Don't read all its files.
Instead: Task(subagent_type=Explore) → "What are simple_mml's main classes and key features?"
```

The sub-agent searches, summarizes, and returns ONLY what you need. Your context stays focused on this project.

## Anti-Drift

- Prompt files are artifacts (can't claim review happened without them)
- Human manually submits to AI (forced engagement)
- Evidence file documents what AI was used
- **MML decision is front-loaded** - no "we'll add it later" drift
- **simple_* first policy declared** - dependencies audited before Phase 1
- **Gaps documented upfront** - ISE/Gobo usage creates future simple_* recommendations
- **Skill Version Lock:** If you discover skill improvements during workflow, queue them in `<project-path>/.eiffel-workflow/skill-improvements.md` - do NOT modify skills mid-workflow
