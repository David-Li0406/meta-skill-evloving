---
name: requirements-clarity
description: Use this skill to clarify ambiguous requirements through focused dialogue before implementation, especially when features are complex or involve cross-team coordination.
---

# Requirements Clarity Skill

## Description

Automatically transforms vague requirements into actionable Product Requirement Documents (PRDs) through systematic clarification with a scoring system.

## Instructions

When invoked, detect vague requirements:

1. **Vague Feature Requests**
   - User says: "add login feature", "implement payment", "create dashboard"
   - Missing: How, with what technology, what constraints?

2. **Missing Technical Context**
   - No technology stack mentioned
   - No integration points identified
   - No performance/security constraints

3. **Incomplete Specifications**
   - No acceptance criteria
   - No success metrics
   - No edge cases considered
   - No error handling mentioned

4. **Ambiguous Scope**
   - Unclear boundaries (e.g., "user management" - what exactly?)
   - No distinction between MVP and future enhancements
   - Missing "what's NOT included"

**Do NOT activate when**:
- Specific file paths mentioned (e.g., "auth.go:45")
- Code snippets included
- Existing functions/classes referenced
- Bug fixes with clear reproduction steps

## Core Principles

1. **Systematic Questioning**
   - Ask focused, specific questions
   - One category at a time (2-3 questions per round)
   - Build on previous answers
   - Avoid overwhelming users

2. **Quality-Driven Iteration**
   - Continuously assess clarity score (0-100)
   - Identify gaps systematically
   - Iterate until clarity score is ≥ 90 points
   - Document all clarification rounds

3. **Actionable Output**
   - Generate concrete specifications
   - Include measurable acceptance criteria
   - Provide executable phases
   - Enable direct implementation

## Clarification Process

### Step 1: Initial Requirement Analysis

**Input**: User's requirement description

**Tasks**:
1. Parse and understand core requirement
2. Generate feature name (kebab-case format)
3. Determine document version (default `1.0` unless user specifies otherwise)
4. Ensure `./docs/prds/` exists for PRD output
5. Perform initial clarity assessment (0-100)

**Assessment Rubric**:
```
Functional Clarity: /30 points
- Clear inputs/outputs: 10 pts
- User interaction defined: 10 pts
- Success criteria stated: 10 pts
```