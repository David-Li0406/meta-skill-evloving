---
name: open-prose
description: Use this skill when you want to run `.prose` files, mention OpenProse, or orchestrate multi-agent workflows from a script.
---

# OpenProse Skill

OpenProse is a programming language for AI sessions—an AI session is a Turing-complete computer. It provides a structured but self-evident syntax: unambiguous control flow with natural language conditions where you want AI judgment.

## When to Activate

Activate this skill when the user:

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

## Telemetry

OpenProse collects anonymous usage analytics to improve the language and tooling. This is opt-in and privacy-respecting.

### State Variable

The telemetry preference is stored in `.prose/state.json` as `OPENPROSE_TELEMETRY`:

```json
{
  "OPENPROSE_TELEMETRY": "enabled"  // or "disabled"
}
```

### First Boot Opt-In

On first activation, if `OPENPROSE_TELEMETRY` is not set:

1. **Prompt the user** using `AskUserQuestion`:

   > "OpenProse can send anonymous usage data to help improve the language. No code or personal info is collected—just feature usage patterns. Enable telemetry?"

   | Option | Description |
   |--------|-------------|
   | "Yes, enable" | Help improve OpenProse with anonymous data |
   | "No thanks" | Disable telemetry |

2. **Store the choice** in `.prose/state.json`
3. **Continue** to normal boot flow

### Sending Analytics

When telemetry is enabled, send events to the analytics API after key operations:

**Endpoint:** `https://api.prose.md/analytics`

**Method:** POST with JSON body

**Events to track:**
- `compile` - When validating/compiling a .prose file
- `run` - When executing a .prose program
- `poll` - Interactive mode questions (question, options, selected answer)

## Interactive Mode (Boot Menu)

Interactive mode is OpenProse's primary onboarding interface. It's a dynamic interview process that converges on teaching the user OpenProse concepts and/or taking action via `.prose` files.

### When to Trigger

| Trigger | Action |
|---------|--------|
| User runs `/prose-boot` | **Always** run boot menu |
| User mentions OpenProse without clear intent | Run boot menu |
| User asks "how does this work", "get started", "intro" | Run boot menu |
| User has a specific file to run or task to do | **Skip** boot menu, execute directly |

### Boot Flow: New Users

If no `.prose` files exist in the current directory:

1. **Welcome + First Poll**: Ask one question using `AskUserQuestion`.
2. **Bridge Questions**: Based on the first answer, ask 1-3 additional questions to narrow toward an actionable example.
3. **Generate & Save .prose File**: Create a simple example and save it.
4. **Handoff**: Provide a concise summary of the created file.

### Boot Flow: Returning Users

If `.prose` files already exist in the current directory:

1. **Scan** existing files to understand what they've built.
2. **Assess** their current stage.
3. **Ask one tailored question** about their next goal.
4. **Guide** to an action that reinforces using the OpenProse VM.

## Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `prose.md` | Execution semantics | Always read for running programs |
| `docs.md` | Full language spec | For compilation, validation, or syntax questions |

### Typical Workflow

1. **Interpret**: Read `prose.md` to execute a valid program.
2. **Compile/Validate**: Read `docs.md` when asked to compile or when syntax is ambiguous.

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

The plugin ships with 37 example programs in the `examples/` directory:

- **01-08**: Basics (hello world, research, code review, debugging)
- **09-12**: Agents and skills
- **13-15**: Variables and composition
- **16-19**: Parallel execution
- **20-21**: Loops and pipelines
- **22-23**: Error handling
- **24-27**: Advanced (choice, conditionals, blocks, interpolation)
- **28**: Gas Town (multi-agent orchestration)
- **29-31**: Captain's chair pattern (persistent orchestrator)
- **33-36**: Production workflows (PR auto-fix, content pipeline, feature factory, bug hunter)
- **37**: The Forge (build a browser from scratch)

Start with `01-hello-world.prose` or try `37-the-forge.prose` to watch AI build a web browser.

## Execution

To execute a `.prose` file, you become the OpenProse VM:

1. **Read `prose.md`** — this document defines how you embody the VM.
2. **You ARE the VM** — your conversation is its memory, your tools are its instructions.
3. **Spawn sessions** — each `session` statement triggers a Task tool call.
4. **Narrate state** — use the emoji protocol to track execution (📍, 📦, ✅, etc.).
5. **Evaluate intelligently** — `**...**` markers require your judgment.

## Syntax at a Glance

```
session "prompt"              # Spawn subagent
agent name:                   # Define agent template
let x = session "..."         # Capture result
parallel:                     # Concurrent execution
repeat N:                     # Fixed loop
for x in items:               # Iteration
loop until **condition**:     # AI-evaluated loop
try: ... catch: ...           # Error handling
if **condition**: ...         # Conditional
choice **criteria**: option   # AI-selected branch
block name(params):           # Reusable block
do blockname(args)            # Invoke block
items | map: ...              # Pipeline
```

For complete syntax and validation rules, see `docs.md`.