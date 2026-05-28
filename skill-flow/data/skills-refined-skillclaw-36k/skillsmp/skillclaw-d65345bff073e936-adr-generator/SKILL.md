---
name: adr-generator
description: Use this skill when you need automated assistance for generating architecture decision records (ADRs) and related technical documentation.
---

# Skill body

## Purpose

This skill provides automated assistance for architecture decision record (ADR) generation tasks within the Technical Documentation domain.

## When to Use

This skill activates automatically when you:
- Mention "adr generator" in your request
- Ask about ADR patterns or best practices
- Need help with technical documentation skills covering API docs, user guides, architecture docs, and documentation automation.

## Capabilities

1. Provides step-by-step guidance for ADR generation.
2. Follows industry best practices and patterns.
3. Generates production-ready code and configurations.
4. Validates outputs against common standards.

## Example Triggers

- "Help me with adr generator"
- "Set up adr generator"
- "How do I implement adr generator?"

## Prerequisites

- Relevant development environment configured.
- Access to necessary tools and services.
- Basic understanding of technical documentation concepts.

## Output

- Generated configurations and code.
- Best practice recommendations.
- Validation results.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Configuration invalid | Missing required fields | Check documentation for required parameters. |
| Tool not found | Dependency not installed | Install required tools per prerequisites. |
| Permission denied | Insufficient access | Verify credentials and permissions. |

## Related Skills

Part of the **Technical Documentation** skill category.  
Tags: documentation, markdown, api-docs, readme, technical-writing