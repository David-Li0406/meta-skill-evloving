---
name: open-prose
description: Use this skill when you want to run `.prose` files, mention OpenProse, or orchestrate multi-agent workflows from a script.
---

# OpenProse Skill

OpenProse is a programming language for AI sessions. LLMs are simulators—when given a detailed system description, they don't just describe it, they *simulate* it. The `prose.md` specification describes a virtual machine with enough fidelity that a Prose Complete system reading it *becomes* that VM. Simulation with sufficient fidelity is implementation.

## When to Activate

Activate this skill when the user:

- Uses any `prose` command (e.g., `prose boot`, `prose run`, `prose compile`, `prose update`, etc.)
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
| `prose compile <file>` | Load `compiler.md`, validate the program |
| `prose update` | Run migration |
| `prose examples` | Show or run example programs from `examples/` |
| Other | Intelligently interpret based on context |

### Important: Single Skill

There is only ONE skill: `open-prose`. All `prose` commands route through this single skill.

## Execution

To execute a `.prose` file, you become the OpenProse VM:

1. **Read `prose.md`** — this document defines how you embody the VM
2. **You ARE the VM** — your conversation is its memory, your tools are its instructions
3. **Spawn sessions** — each `session` statement triggers a Task tool call
4. **Narrate state** — use the emoji protocol to track execution (📍, 📦, ✅, etc.)
5. **Evaluate intelligently** — `**...**` markers require your judgment

## Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `prose.md` | Execution semantics | Always read for running programs |
| `compiler.md` | Compiler/validator | Only when user asks to compile or validate |
| `help.md` | Help, FAQs, onboarding | Load for user assistance |
| `examples/` | Example programs | For reference and demonstration |

## Quick Reference

### Sessions

```prose
session "Do something"                    # Simple session
session: myAgent                          # With agent
  prompt: "Task prompt"
  context: previousResult                 # Pass context
```

### Agents

```prose
agent researcher:
  model: sonnet                           # sonnet | opus | haiku
  prompt: "You are a research assistant"
```

### Variables

```prose
let result = session "Get result"         # Mutable
const config = session "Get config"       # Immutable
session "Use both"
  context: [result, config]               # Array form
  context: { result, config }             # Object form
```

### Parallel

```prose
parallel:
  a = session "Task A"
  b = session "Task B"
session "Combine" context: { a, b }
```

### Loops

```prose
repeat 3:                                 # Fixed
  session "Generate idea"

for topic in ["AI", "ML"]:                # For-each
  session "Research" context: topic

loop until **done** (max: 10):            # AI-evaluated
  session "Keep working"
```

### Error Handling

```prose
try:
  session "Risky" retry: 3
catch as err:
  session "Handle" context: err
```

### Conditionals

```prose
if **has issues**:
  session "Fix"
else:
  session "Approve"

choice **best approach**:
  option "Quick": session "Quick fix"
  option "Full": session "Refactor"
```

## Examples

The skill includes numerous example programs in the `examples/` directory. Start with `01-hello-world.prose` to see the basic structure.

## Telemetry

OpenProse collects anonymous usage analytics to improve the language and tooling. Telemetry is **enabled by default** and is privacy-respecting.

### State File

Session state is stored in `.prose/state.json`:

```json
{
  "OPENPROSE_TELEMETRY": "enabled",
  "USER_ID": "user-a7b3c9d4e5f6",
  "SESSION_ID": "sess-1704326400000-x9y8z7"
}
```

### Sending Analytics

When telemetry is enabled, send events to the analytics API after key operations. Always include both `user_id` and `session_id` in every event.

## Interactive Mode (Boot Menu)

Interactive mode is OpenProse's primary onboarding interface. It guides users to a running `.prose` file as fast as possible.

### When to Trigger

| Trigger | Action |
|---------|--------|
| User runs `/prose-boot` | Always run boot menu |
| User mentions OpenProse without clear intent | Run boot menu |
| User asks "how does this work", "get started", "intro" | Run boot menu |

### Boot Flow

1. **Initialize Session**: Check for `.prose/` directory, read state file, generate IDs.
2. **Welcome + First Poll**: Ask what brings the user to OpenProse.
3. **Generate & Save .prose File**: Create a simple example based on user input.
4. **Handoff**: Provide instructions on how to run the created file.

For complete syntax and validation rules, see `docs.md`.