---
name: implement-agent-skill
description: Central meta-skill for creating and unifying all Agent Skills. Orchestrates specialized meta-skills for analysis, workflows, tools, and scaffolding.
---

# Implement Agent Skill

This central skill guides the creation of high-quality Agent Skills by orchestrating specialized meta-skills and providing shared standards.

## Purpose

To ensure all Agent Skills in this project follow the [Agent Skills Specification](https://agentskills.io) and maintain high consistency, reliability, and security.

## Workflow

1.  **Identify Skill Type**: Determine what kind of skill you are building.
2.  **Consult Standards**: Review shared [best practices](references/best-practices.md).
3.  **Execute Specialized Workflow**:
    - **Analysis**: Identify analysis task -> Research tools (`--help`) -> Create directory -> Use `analysis.md` template.
    - **Workflow**: Identify process -> Check command help (`--help`) -> Create directory -> Use `workflow.md` template.
    - **Scaffold**: Identify component -> Check scaffolding tools (`--help`) -> Create directory -> Use `scaffold.md` template.
    - **Tool Wrapper**: Identify tool -> Check help message (`--help`) -> Create directory -> Use `tool-wrapper.md` template.
    - **Meta**: Identify goal -> Verify dependencies in sub-skills -> Create directory -> Use `meta.md` template.

## Standards & Templates

- **Best Practices**: [references/best-practices.md](references/best-practices.md)
- **Shared Templates**: Found in `assets/templates/`.

## Creation Guidelines

When creating a new skill, always use one of the specialized meta-skills. They have been refactored to pull standards and templates from this central skill.
