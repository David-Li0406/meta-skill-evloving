---
name: open-prose
description: Use this skill when you want to execute commands related to the OpenProse programming language, manage `.prose` files, or orchestrate multi-agent workflows.
---

# OpenProse Skill

OpenProse is a programming language for AI sessions. LLMs are simulators—when given a detailed system description, they don't just describe it, they _simulate_ it. The `prose.md` specification describes a virtual machine with enough fidelity that a Prose Complete system reading it _becomes_ that VM. Simulation with sufficient fidelity is implementation. **You are the Prose Complete system.**

## Clawdbot Runtime Mapping

- **Task tool** in the upstream spec == Clawdbot `sessions_spawn`
- **File I/O** == Clawdbot `read`/`write`
- **Remote fetch** == Clawdbot `web_fetch` (or `exec` with curl when POST is required)

## When to Activate

Activate this skill when the user:

- **Uses ANY `prose` command** (e.g., `prose boot`, `prose run`, `prose compile`, `prose update`, `prose help`, etc.)
- Asks to run a `.prose` file
- Mentions "OpenProse" or "prose program"
- Wants to orchestrate multiple AI agents from a script
- Has a file with `session "..."` or `agent name:` syntax
- Wants to create a reusable workflow

## Command Routing

When a user invokes `prose <command>`, intelligently route based on intent:

| Command | Action |
|---------|--------|
| `prose help` | Load `help.md`, guide user to what they need |
| `prose run <file>` | Load VM (`prose.md` + state backend), execute the program |
| `prose run handle/slug` | Fetch from registry, then execute (see Remote Programs below) |
| `prose compile <file>` | Load `compiler.md`, validate the program |
| `prose update` | Run migration (see Migration section below) |
| `prose examples` | Show or run example programs from `examples/` |
| Other | Intelligently interpret based on context |

### Important: Single Skill

There is only ONE skill: `open-prose`. There are NO separate skills like `prose-run`, `prose-compile`, or `prose-boot`. All `prose` commands route through this single skill.

### Resolving Example References

**Examples are bundled in `examples/` (same directory as this file).** When users reference examples by name (e.g., "run the gastown example"):

1. Read `examples/` to list available files
2. Match by partial name, keyword, or number
3. Run with: `prose run examples/28-gas-town.prose`

**Common examples by keyword:**
| Keyword | File |
|---------|--------|