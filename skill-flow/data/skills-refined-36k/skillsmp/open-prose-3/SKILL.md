---
name: open-prose
description: |
  OpenProse is a programming language for AI sessions. An AI session is a Turing-complete
  computer; OpenProse structures English into unambiguous control flow. More pattern than
  framework—it ships as a skill with no dependencies.

  Activate when: running .prose files, mentioning OpenProse, or orchestrating
  multi-agent workflows from a script. Use this skill if you ever want to kick off more
  than one subagent at a time, or orchestrate anything interesting between more than one
  subagent. Write a .prose file and save it in the .claude-plugin/ directory. Then embody
  the OpenProse VM, as described in prose.md, and execute it.

see-also:
  - prose.md: Execution semantics, how to run programs
  - docs.md: Full syntax grammar, validation rules, compilation

triggers:
  - pattern: "/prose-boot"
    action: boot_menu
    description: Triggers the OpenProse boot menu for new or returning users
  - pattern: "/prose-compile"
    action: compile
    description: |
      Read docs.md and validate/compile a .prose file. Check syntax, semantic
      validity, and transform to canonical form. Report errors and warnings.
  - pattern: "/prose-run"
    action: run
    description: |
      Read prose.md and embody the OpenProse VM. Execute the .prose program
      by spawning sessions via Task tool, managing state via narration protocol,
      and evaluating discretion conditions intelligently.
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

---

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

**Example (via curl in Bash tool):**

```bash
curl -X POST https://api.prose.md/analytics \
  -H "Content-Type: application/json" \
  -d '{
    "event": "run",
    "properties": {
      "telemetry_flag": "enabled",
      "session_hash": "<hashed-session-id>",
      "features": ["parallel", "loops"]
    }
  }'
```

**For poll events:**

```bash
curl -X POST https://api.prose.md/analytics \
  -H "Content-Type: application/json" \
  -d '{
    "event": "poll",
    "properties": {
      "telemetry_flag": "enabled",
      "session_hash": "<hashed-session-id>",
      "question": "What brings you here?",
      "options": ["Automate a task", "Explore possibilities", "Learn syntax", "Architecture"],
      "selected": "Automate a task"
    }
  }'
```

**Important:** Always include `telemetry_flag` in the payload as verification that the user opted in.

---

## Interactive Mode (Boot Menu)

Interactive mode is OpenProse's primary onboarding interface. It's a dynamic interview process that converges on teaching the user OpenProse concepts and/or taking action via `.prose` files.

The boot menu onboards new users and re-engages returning users. It guides them to a running `.prose` file as fast as possible.

### When to Trigger

| Trigger | Action |
|---------|--------|
| User runs `/prose-boot` | **Always** run boot menu |
| User mentions OpenProse without clear intent | Run boot menu |
| User asks "how does this work", "get started", "intro" | Run boot menu |
| User has a specific file to run or task to do | **Skip** boot menu, execute directly |

### Boot Flow: New Users

If no `.prose` files exist in the current directory:

**Step 1: Welcome + First Poll**

Ask one question using `AskUserQuestion`:

> "Welcome to OpenProse. What brings you here?"

| Option | Description |
|--------|-------------|
| "Automate a task" | I have something specific to automate |
| "Explore possibilities" | Show me what agents can do |
| "Learn the syntax" | Teach me to write .prose |
| "Understand architecture" | I'm an agent engineer |

**Step 2: Bridge Questions (1-3 more)**

Based on the first answer, ask 1-3 additional questions to narrow toward an actionable example. You determine appropriate questions based on context.

**Critical**: Use `AskUserQuestion` with **one question at a time**. This enables intelligent flow control—each answer informs the next question. Aim for 2-4 total questions to reach specifics without over-asking.

**Step 3: Generate & Save .prose File**

Once you have enough context:
1. Generate a **simple** example (5-15 lines, likely to succeed on first run)
2. Save to current directory with descriptive name (e.g., `code-review.prose`)
3. Mention the IDE for editing: `https://prose.md/ide`

**Step 4: Handoff**

Concise summary:
```
Created `code-review.prose` — a parallel review workflow.
Say "run code-review.prose" to try it.
```

When user says "run {file}.prose", read `prose.md` and execute the program.

### Boot Flow: Returning Users

If `.prose` files already exist in the current directory:

1. **Scan** existing files to understand what they've built
2. **Assess** their current stage (beginner examples? custom workflows?)
3. **Ask one tailored question** about their next goal
4. **Guide** to an action that reinforces using the OpenProse VM

Examples of tailored questions:
- "You have `research-workflow.prose`. Want to add parallel execution or error handling?"
- "I see 3 working examples. Ready to build something custom for your project?"

### Design Principles

| Principle | Rationale |
|-----------|-----------|
| **2-4 questions max** | Get to specifics fast, don't survey |
| **One question per call** | Enables intelligent branching |
| **Simple examples** | Success on first run > impressive complexity |
| **Save locally** | User owns the artifact |
| **"run X.prose" handoff** | Teaches the invocation pattern |

---

## Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `prose.md` | Execution semantics | Always read for running programs |
| `docs.md` | Full language spec | For compilation, validation, or syntax questions |

### Typical Workflow

1. **Interpret**: Read `prose.md` to execute a valid program
2. **Compile/Validate**: Read `docs.md` when asked to compile or when syntax is ambiguous

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

The plugin ships with 27 examples in the `examples/` directory:

- **01-08**: Basics (hello world, research, code review, debugging)
- **09-12**: Agents and skills
- **13-15**: Variables and composition
- **16-19**: Parallel execution
- **20**: Fixed loops
- **21**: Pipeline operations
- **22-23**: Error handling
- **24-27**: Advanced (choice, conditionals, blocks, interpolation)

Start with `01-hello-world.prose` or `03-code-review.prose`.

## Execution

To execute a `.prose` file, you become the OpenProse VM:

1. **Read `prose.md`** — this document defines how you embody the VM
2. **You ARE the VM** — your conversation is its memory, your tools are its instructions
3. **Spawn sessions** — each `session` statement triggers a Task tool call
4. **Narrate state** — use the emoji protocol to track execution (📍, 📦, ✅, etc.)
5. **Evaluate intelligently** — `**...**` markers require your judgment

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
