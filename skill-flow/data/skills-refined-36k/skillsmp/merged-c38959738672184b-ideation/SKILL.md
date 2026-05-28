---
name: ideation
description: Transform raw brain dumps into structured implementation artifacts. Use when the user has messy ideas, scattered thoughts, or dictated stream-of-consciousness about something they want to build. Produces contracts, phased PRDs, and implementation specs written to ./docs/ideation/{project-name}/.
---

# Ideation

Transform unstructured brain dumps into structured, actionable implementation artifacts through a confidence-gated workflow.

## Critical: Use AskUserQuestion Tool

**ALWAYS use the `AskUserQuestion` tool when asking clarifying questions.** Do not ask questions in plain text. The tool provides structured options and ensures the user can respond clearly.

## Workflow Pipeline

```
INTAKE → CONTRACT FORMATION → PRD GENERATION → SPEC GENERATION → EXECUTION HANDOFF
              ↓
         confidence < 95%?
              ↓
         ASK QUESTIONS
              ↓
         (loop until ≥95%)
```

## Phase 1: Intake

Accept whatever the user provides:

- Scattered thoughts and half-formed ideas
- Voice dictation transcripts (messy, stream-of-consciousness)
- Bullet points mixed with rambling
- Topic jumping and tangents
- Contradictions and unclear statements

**Don't require organization. The mess is the input.**

## Phase 2: Contract Formation

### 2.1 Analyze the Brain Dump

Extract from the raw input:

1. **Problem signals**: What pain point or need is being described?
2. **Goal signals**: What does the user want to achieve?
3. **Success signals**: How will they know it worked?
4. **Scope signals**: What's included? What's explicitly excluded?
5. **Contradictions**: Note any conflicting statements

### 2.2 Calculate Confidence Score

Score each dimension (0-20 points):

| Dimension | Question |
|-----------|----------|
| Problem Clarity | Do I understand what problem we're solving and why it matters? |
| Goal Definition | Are the goals specific and measurable? |
| Success Criteria | Can I write tests or validation steps for "done"? |
| Scope Boundaries | Do I know what's in and out of scope? |
| Consistency | Are there contradictions I need resolved? |

**Total: /100 points**

### 2.3 Confidence Thresholds

| Score | Action |
|-------|--------|
| < 70 | Major gaps. Ask 5+ questions targeting lowest dimensions. |
| 70-84 | Moderate gaps. Ask 3-5 targeted questions. |
| 85-94 | Minor gaps. Ask 1-2 specific questions. |
| ≥ 95 | Ready to generate contract. |

### 2.4 Ask Clarifying Questions

When confidence < 95%, **MUST use `AskUserQuestion` tool**. Structure questions with clear options when possible.

**Question templates by dimension**:

**Problem Clarity**:
- "What specific problem are you trying to solve?"
- "Who experiences this problem and how often?"

**Goal Definition**:
- "What does success look like for this project?"
- "What specific metrics should improve?"

**Success Criteria**:
- "How will you know when you're done?"
- "What tests would prove this feature works?"

**Scope Boundaries**:
- "What is explicitly NOT part of this project?"
- "What's the MVP vs. nice-to-have?"

**Consistency**:
- "You mentioned [X] but also [Y]. Which takes priority?"

### 2.5 Generate Contract

When confidence ≥ 95%:

1. Use `AskUserQuestion` to confirm project name if not obvious from context.
2. Convert to kebab-case for directory name.
3. Create output directory: `./docs/ideation/{project-name}/`.
4. Write `contract.md` using a contract template.
5. Get approval before proceeding to PRD generation.

## Phase 3: PRD Generation

After contract is approved:

### 3.1 Determine Phases

Break scope into logical implementation phases based on:
- Dependencies (what must be built first?)
- Risk (tackle high-risk items early)
- Value delivery (can users benefit after each phase?)

### 3.2 Generate PRDs

For each phase, generate `prd-phase-{n}.md` using a PRD template.

### 3.3 Present for Review

Show all PRDs to user. Use `AskUserQuestion` to gather feedback and iterate until user explicitly approves.

## Phase 4: Spec Generation

After PRDs are approved:

### 4.1 Generate Implementation Specs

For each approved phase, generate `spec-phase-{n}.md` using a spec template.

Include:
- Technical approach
- File changes (new and modified)
- Implementation details with code patterns
- Testing requirements
- Validation commands

## Phase 5: Execution Handoff

After specs are generated, create task list and hand off for implementation.

### 5.1 Create Task List

Generate a unique task list ID and create initial phase tasks.

### 5.2 Write Tasks Manifest

Create `./docs/ideation/{project-name}/tasks-manifest.md` with task list ID and coordination info.

### 5.3 Present Handoff Summary

Summarize artifacts and next steps for fresh-session execution.

## Output Artifacts

All artifacts written to `./docs/ideation/{project-name}/`:

```
contract.md              # Lean contract
prd-phase-1.md           # Phase 1 requirements
prd-phase-2.md           # Phase 2 requirements (if applicable)
spec-phase-1.md          # Phase 1 implementation spec
spec-phase-2.md          # Phase 2 implementation spec
tasks-manifest.md        # Task list ID and cross-session coordination info
```

## Important Notes

- **ALWAYS use `AskUserQuestion` tool for clarifications and approvals.**
- Never skip the confidence check.
- Always write artifacts to files.
- Each phase should be independently valuable.
- Specs should be detailed enough to implement without re-reading PRDs.