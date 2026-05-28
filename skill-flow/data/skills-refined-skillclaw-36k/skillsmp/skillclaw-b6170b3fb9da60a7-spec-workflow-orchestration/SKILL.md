---
name: spec-workflow-orchestration
description: Use this skill for comprehensive specification management using the EARS format, facilitating requirement clarification and Plan-Run-Sync integration in development methodologies.
---

# SPEC Workflow Management

## Quick Reference (30 seconds)

SPEC Workflow Orchestration - Comprehensive specification management using EARS format for systematic requirement definition and Plan-Run-Sync workflow integration.

### Core Capabilities:
- **EARS Format Specifications**: Five requirement patterns for clarity.
- **Requirement Clarification**: Four-step systematic process.
- **SPEC Document Templates**: Standardized structure for consistency.
- **Plan-Run-Sync Integration**: Seamless workflow connection.
- **Parallel Development**: Git Worktree-based SPEC isolation.
- **Quality Gates**: TRUST 5 framework validation.

### EARS Five Patterns:
- **Ubiquitous**: The system shall always perform action - Always active.
- **Event-Driven**: WHEN event occurs THEN action executes - Trigger-response.
- **State-Driven**: IF condition is true THEN action executes - Conditional behavior.
- **Unwanted**: The system shall not perform action - Prohibition.
- **Optional**: Where possible, provide feature - Nice-to-have.

### When to Use:
- Feature planning and requirement definition.
- SPEC document creation and maintenance.
- Parallel feature development coordination.
- Quality assurance and validation planning.

### Quick Commands:
- Create new SPEC: `/spec:1-plan "user authentication system"`
- Create SPEC with domain: `/spec:1-plan --domain AUTH "JWT login"`
- Create parallel SPECs with Worktrees: `/spec:1-plan "login feature" "signup feature" --worktree`
- Create SPEC with new branch: `/spec:1-plan "payment processing" --branch`
- Update existing SPEC: `/spec:1-plan SPEC-001 "add OAuth support"`

---

## Implementation Guide (5 minutes)

### Core Concepts

SPEC-First Development Philosophy:
- EARS format ensures unambiguous requirements.
- Requirement clarification prevents scope creep.
- Systematic validation through quality gates.