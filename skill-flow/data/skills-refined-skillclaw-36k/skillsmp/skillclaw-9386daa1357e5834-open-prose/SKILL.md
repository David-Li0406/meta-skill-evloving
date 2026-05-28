---
name: open-prose
description: Use this skill when you want to run `.prose` files, mention OpenProse, or orchestrate multi-agent workflows.
---

# OpenProse Skill

OpenProse is a programming language for AI sessions, enabling the simulation of Turing-complete systems through structured English control flow. It allows users to create and execute `.prose` files, facilitating complex interactions between multiple AI agents.

## When to Activate

Activate this skill when the user:

- Asks to run a `.prose` file
- Uses any `prose` command (e.g., `prose boot`, `prose run`, `prose compile`, `prose update`, etc.)
- Mentions "OpenProse" or "prose program"
- Wants to orchestrate multiple AI agents from a script
- Has a file with `session "..."` or `agent name:` syntax
- Wants to create a reusable workflow

## Command Routing

When a user invokes a `prose` command, intelligently route based on intent:

| Command | Action |
|---------|--------|
| `prose help` | Load `help.md`, guide user to what they need |
| `prose run <file>` | Load VM (`prose.md` + state backend), execute the program |
| `prose compile <file>` | Load `compiler.md`, validate the program |
| `prose update` | Run migration |
| `prose examples` | Show or run example programs from `examples/` |
| Other | Intelligently interpret based on context |

## Important Notes

- There is only one skill: `open-prose`. All `prose` commands route through this single skill.
- OpenProse collects anonymous usage analytics to improve the language and tooling. This is opt-in and privacy-respecting.

## Example Usage

To run a `.prose` file, simply use the command:

```
prose run your_file.prose
```

This will execute the program, managing state and interactions as defined within the file.