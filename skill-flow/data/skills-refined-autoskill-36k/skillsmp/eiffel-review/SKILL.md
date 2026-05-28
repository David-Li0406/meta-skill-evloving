---
name: eiffel-review
description: Phase 2 of Eiffel Spec Kit. Runs progressive AI review chain (Ollama → Claude → Grok → Gemini → Human). Generates approach.md and synopsis.md. BLOCKS until human approves. Use with /eiffel.review command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.review - Phase 2: Adversarial Review + Approach Sketch

**Purpose:** Multiple AI perspectives review contracts before implementation. Human manually submits prompts to each AI and brings results back.

## Usage

```
/eiffel.review <project-path>
```

**Example:**
```
/eiffel.review d:\prod\simple_cache
```

## Project Scoping

All files are created inside the PROJECT directory:
```
<project-path>/
├── .eiffel-workflow/
│   ├── approach.md                    (implementation sketch)
│   ├── synopsis.md                    (aggregated review findings)
│   ├── prompts/
│   │   ├── phase2-ollama-review.md    (READY TO SUBMIT - contracts pre-populated)
│   │   ├── phase2-claude-review.md    (needs Ollama response pasted)
│   │   ├── phase2-grok-review.md      (needs Ollama+Claude responses pasted)
│   │   └── phase2-gemini-review.md    (needs all previous responses pasted)
│   └── evidence/
│       ├── phase2-ollama-response.md  (placeholder for Ollama's review)
│       ├── phase2-claude-response.md  (placeholder for Claude's review)
│       ├── phase2-grok-response.md    (placeholder for Grok's review)
│       ├── phase2-gemini-response.md  (placeholder for Gemini's review)
│       └── phase2-chain.txt           (summary evidence)
├── src/
└── test/
```

## Prerequisites

- Phase 1 complete: contracts compile

Verify:
```bash
test -f <project-path>/.eiffel-workflow/evidence/phase1-compile.txt && echo "Phase 1 complete" || echo "ERROR: Run /eiffel.contracts first"
```

## Workflow

### Step 1: Generate Implementation Sketch

Create `<project-path>/.eiffel-workflow/approach.md` with actual implementation details.

### Step 2: Generate Progressive AI Review Prompts

**CRITICAL: Pre-populate prompts with actual file contents where possible.**

Claude has access to the project files. The prompts should contain:
- **Contracts**: Actual content of all src/*.e files (Claude reads and embeds)
- **Approach**: Actual content of approach.md (Claude reads and embeds)
- **Previous AI responses**: Placeholder - user must paste after receiving

#### 3a. Ollama Prompt (FULLY READY TO SUBMIT)

Create `<project-path>/.eiffel-workflow/prompts/phase2-ollama-review.md` with:
- Full contracts embedded (read all src/*.e files and include content)
- Full approach.md embedded
- User can copy this file directly to Ollama with zero modifications

Template:
```markdown
# Eiffel Contract Review Request (Ollama)

You are reviewing Eiffel contracts for a library. Find obvious problems.

## Review Checklist
- [ ] Preconditions that are just `True` (too weak)
- [ ] Postconditions that don't constrain anything
- [ ] Missing invariants
- [ ] Obvious edge cases not handled
- [ ] Missing MML model queries for collection attributes
- [ ] Missing frame conditions (what did NOT change)

## Contracts to Review

[ACTUALLY EMBED THE FULL CONTENT OF EACH src/*.e FILE HERE]

## Implementation Approach

[ACTUALLY EMBED THE FULL CONTENT OF approach.md HERE]

## Output Format

List issues found as:
- **ISSUE**: [description]
- **LOCATION**: [class.feature]
- **SUGGESTION**: [how to fix]
```

#### 3b. Claude Prompt (Contracts pre-populated, needs Ollama response)

Create `<project-path>/.eiffel-workflow/prompts/phase2-claude-review.md` with:
- Full contracts embedded
- Full approach.md embedded
- Placeholder for Ollama's response (user pastes after Step 1)

**Claude-specific MML review checklist:**
- [ ] MML model queries correctly represent collection semantics
- [ ] Frame conditions use `|=|` for model equality
- [ ] Postconditions use `old` expressions correctly
- [ ] Model queries are pure (no side effects)

#### 3c. Grok Prompt (Contracts pre-populated, needs previous responses)

Create `<project-path>/.eiffel-workflow/prompts/phase2-grok-review.md` with:
- Full contracts embedded
- Full approach.md embedded
- Placeholders for Ollama + Claude responses

#### 3d. Gemini Prompt (Contracts pre-populated, needs all previous responses)

Create `<project-path>/.eiffel-workflow/prompts/phase2-gemini-review.md` with:
- Full contracts embedded
- Full approach.md embedded
- Placeholders for all three previous responses

### Step 3: Auto-Create Evidence Placeholder Files

Create placeholder files in `<project-path>/.eiffel-workflow/evidence/` with STATUS: INCOMPLETE markers.

### Step 4: Notify Human - Start Manual Cycle

Display:
```
PHASE 2: Review prompts generated.

READY TO SUBMIT (contracts pre-populated):
  - phase2-ollama-review.md → Copy entire file to Ollama

NEED PREVIOUS RESPONSES PASTED:
  - phase2-claude-review.md → Paste Ollama's response first
  - phase2-grok-review.md → Paste Ollama + Claude responses first
  - phase2-gemini-review.md → Paste all previous responses first

EVIDENCE PLACEHOLDERS (save AI responses here):
  - evidence/phase2-ollama-response.md
  - evidence/phase2-claude-response.md
  - evidence/phase2-grok-response.md
  - evidence/phase2-gemini-response.md

MANUAL REVIEW CHAIN:

Step 1: OLLAMA
  a. Copy entire contents of: prompts/phase2-ollama-review.md
  b. Paste to Ollama
  c. Save response to: evidence/phase2-ollama-response.md

Step 2: CLAUDE
  a. Open: prompts/phase2-claude-review.md
  b. Paste Ollama's response where indicated
  c. Copy entire file to a different Claude session
  d. Save response to: evidence/phase2-claude-response.md

Step 3: GROK
  a. Open: prompts/phase2-grok-review.md
  b. Paste Ollama + Claude responses where indicated
  c. Copy entire file to Grok
  d. Save response to: evidence/phase2-grok-response.md

Step 4: GEMINI
  a. Open: prompts/phase2-gemini-review.md
  b. Paste all previous responses where indicated
  c. Copy entire file to Gemini
  d. Save response to: evidence/phase2-gemini-response.md

When complete, say "reviews complete" and I will generate the synopsis.

NOTE: You may skip AIs or change the order. At minimum, use ONE external AI.
```

**BLOCK until user confirms reviews are complete.**

### Step 5: Generate Synopsis

When user returns, read all response files and create synopsis.md.

### Step 6: Human Approval

**DO NOT PROCEED until user explicitly approves.**

### Step 7: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase2-chain.txt`.

## Completion

When user approves:
```
Phase 2 COMPLETE: Adversarial review passed.
Project: <project-path>

Next: Run /eiffel.tasks <project-path> to break contracts into implementation tasks.
```

## Context Management (RLM Pattern)

This skill focuses ONLY on: `<project-path>`

**DO NOT:**
- Read files outside this project directory
- Load entire ecosystem or multiple libraries into context

**DO:**
- Use Task tool with Explore agent for ecosystem questions
- Pre-populate prompts with actual file contents (contracts, approach)
- Only use placeholders for content that doesn't exist yet (AI responses)

## Anti-Drift

- Ollama prompt is FULLY ready to submit (no user pasting of contracts)
- Subsequent prompts only need previous AI responses pasted
- Human effort is minimized to: copy prompt → submit to AI → save response
