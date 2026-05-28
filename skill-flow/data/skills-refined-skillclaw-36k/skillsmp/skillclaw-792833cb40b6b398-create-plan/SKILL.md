---
name: create-plan
description: Use this skill when planning new features or components to create structured implementation plans with requirements, design, and tasks, including explicit approval gates at each phase.
---

# Plan Generation Skill

When the user invokes this skill or asks to create a plan, follow a structured workflow with explicit approval gates. Generate three files following AWS and coding best practices:

## ⚠️ CRITICAL REQUIREMENT: Context Section Updates

**ALL three files (requirements.md, design.md, implementation.md) MUST:**
1. Include a Context section at the end with Timeline and Conversation Summary.
2. Have this Context section updated AUTOMATICALLY after EVERY significant interaction.
3. Updates happen WITHOUT asking for permission - just do it automatically.
4. This enables session recovery if the conversation dies.

**Update Context section automatically when:**
- User provides feedback, requests changes, or makes decisions.
- Requirements, design, or implementation is modified.
- Tasks are completed or progress is made.
- User asks questions or provides clarifications.
- Any iteration or approval gate is reached.

## File Structure
Store files in: `~/.{cli}/knowledge/plans/{YY}/{MM}/{component}/{feature}/` (replace `{cli}` with the appropriate CLI name).

Generate:
1. `requirements.md` - User stories and acceptance criteria.
2. `design.md` - Architecture and technical design.
3. `implementation.md` - Implementation steps with status tracking.

## Workflow Phases

### Phase 1: Requirements Gathering
1. Generate `requirements.md` based on user's feature idea.
2. Present requirements for review.
3. **GATE**: Get explicit user approval before proceeding.
4. Iterate based on feedback until approved.

### Phase 2: Design Creation
1. Generate `design.md` based on approved requirements.
2. Present design for review.
3. **GATE**: Get explicit user approval before proceeding.
4. Iterate based on feedback until approved.

### Phase 3: Implementation Planning
1. Generate `implementation.md` based on approved design.
2. Present implementation plan for review.
3. **GATE**: Get explicit user approval before proceeding.
4. Execute tasks with status tracking.

## requirements.md Format
```markdown
# Requirements: {Feature Name}

## Introduction
[Summary of the feature/system]

## Glossary
- **System/Term**: [Definition]
- **Another_Term**: [Definition]

## Requirements

### Requirement 1: [Requirement Name]

**User Story:** As a [role], I want [feature], so that [benefit]
```