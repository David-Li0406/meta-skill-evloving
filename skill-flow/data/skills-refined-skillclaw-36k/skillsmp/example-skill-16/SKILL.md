---
name: example-skill
description: "Demonstrates all available skill frontmatter fields. Use when you need a reference for skill configuration, when learning about skill capabilities, or when creating new skills from scratch."
argument-hint: "[topic]"
allowed-tools: Read, Grep, Glob, WebFetch
model: sonnet
context: fork
agent: general-purpose
user-invocable: true
disable-model-invocation: false
hooks:
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "echo 'File was read'"
          timeout: 5
---

# Example Skill

This skill demonstrates all available frontmatter fields for Claude Code skills.

## Purpose

Use this as a reference when creating new skills. All fields shown above are valid skill frontmatter options.

## Field Descriptions

| Field                      | Purpose                                | Default         |
| -------------------------- | -------------------------------------- | --------------- |
| `name`                     | Display name (kebab-case)              | directory name  |
| `description`              | When to load this skill                | first paragraph |
| `argument-hint`            | Autocomplete hint                      | none            |
| `allowed-tools`            | Tools without permission prompts       | none            |
| `model`                    | Model when skill is active             | default         |
| `context`                  | Context behavior (`fork` for isolated) | none            |
| `agent`                    | Subagent type when `context: fork`     | general-purpose |
| `user-invocable`           | Show in `/` menu                       | true            |
| `disable-model-invocation` | Prevent Claude auto-loading            | false           |
| `hooks`                    | Scoped hooks for skill lifecycle       | none            |

## Usage

This skill is for demonstration purposes only. When creating real skills, include only the fields you need.

## Sources

- [Skills Documentation](https://code.claude.com/docs/en/skills) - Official skill format
