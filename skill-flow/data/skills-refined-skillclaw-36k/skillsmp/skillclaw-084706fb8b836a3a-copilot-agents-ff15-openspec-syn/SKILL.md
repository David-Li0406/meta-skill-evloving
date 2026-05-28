---
name: copilot-agents-ff15-openspec-sync
description: Use this skill to sync GitHub Copilot agents for an FF15-inspired OpenSpec workflow, optimizing team dynamics for efficient project management.
---

# FF15 Copilot Agents - OpenSpec Edition

Manages GitHub Copilot agent definitions and prompts based on Final Fantasy XV team dynamics, optimized for OpenSpec workflow.

## Quick Start

Sync all agents, prompts, and docs to a project:

```bash
python skills/copilot-agents-ff15-openspec-sync/scripts/sync_agents.py --target /path/to/project
```

## The FF15 Team (OpenSpec Edition)

| Agent | Role | Specialization |
|-------|------|----------------|
| **Noctis** | **Orchestrator + Spec Creator** | **OpenSpec creation, workflow coordination, user collaboration** |
| **Iris** | **Issue Management** | **GitHub Issue creation and management based on requirements** |
| **Gladiolus** | **Implementation** | **Code writing, feature building based on OpenSpec, executes to completion** |
| **Prompto** | **Code Quality** | **OpenSpec compliance, review-policy enforcement, refactoring** |
| **Ignis** | **Documentation** | **README, CHANGELOG, documentation updates** |
| **Lunafreya** | **PR Creation** | **Pull request creation and finalization** |

## Workflow

The new streamlined workflow minimizes user intervention:

1. **Noctis** collaborates with user to create OpenSpec documents.
2. ⏸️ **User approves specification.**
3. **Iris** creates GitHub Issue (if requested).
4. **Gladiolus** implements based on OpenSpec.
5. **Prompto** improves code quality (OpenSpec + review-policy).
6. **Ignis** updates documentation (without archiving).
7. **Noctis** verifies tasks completion and archives OpenSpec.
8. **Lunafreya** creates PR.
9. **Noctis** notifies user and requests verification.
10. ⏸️ **User verifies implementation.**

## Team Philosophy

The FF15 OpenSpec team focuses on **autonomous execution with minimal interruptions**:
- **Noctis** creates specifications collaboratively, orchestrates execution, and archives completed work.
- **Iris** manages the issue lifecycle.
- **Gladiolus** delivers solid implementations.
- **Prompto** ensures quality autonomously.
- **Ignis** keeps documentation current.
- **Lunafreya** completes the journey with pull request creation.

## Invocation Methods

### Slash Command

| Command | Description |
|---------|-------------|
| **/noctis** | Initiates the orchestration process. |