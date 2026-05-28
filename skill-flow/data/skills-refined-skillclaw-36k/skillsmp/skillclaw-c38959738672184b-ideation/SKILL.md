---
name: ideation
description: Use this skill to transform raw brain dumps into structured implementation artifacts when you have messy ideas, scattered thoughts, or dictated stream-of-consciousness about something you want to build.
---

# Skill body

Transform unstructured brain dumps into structured, actionable implementation artifacts through a confidence-gated workflow.

## Critical: Use AskUserQuestion Tool

**ALWAYS use the `AskUserQuestion` tool when asking clarifying questions.** Do not ask questions in plain text. The tool provides structured options and ensures the user can respond clearly.

## Workflow Pipeline

```
INTAKE → CONTRACT FORMATION → PRD GENERATION → SPEC GENERATION
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

Acknowledge receipt and begin analysis. Do not ask for clarification yet.

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
| >= 95 | Ready to generate contract. |