---
name: RoutineCapture
description: Save repeatable workflows as personal skills. USE WHEN save this routine, remember this workflow, save these steps, capture this procedure, make this repeatable, do this again later, save workflow.
---

# RoutineCapture

Capture repeatable workflows from conversations and save them as personal skills for future invocation.

## How It Works

1. **Complete a task** - Work through a multi-step workflow with corrections as needed
2. **Request capture** - Say "save this routine" or similar
3. **Review extraction** - Agent presents the captured steps and detected parameters
4. **Confirm and adjust** - Modify steps, parameters, or trigger phrases as needed
5. **Skill created** - A personal skill (`_RoutineName`) is generated
6. **Invoke later** - Use natural language to run the saved routine

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CaptureRoutine** | "save this routine", "remember this workflow" | `Workflows/CaptureRoutine.md` |

## Examples

**Example 1: Save after completing a task**
```
User: [completes multi-step class audit task]
User: "save this routine for later"
→ Agent extracts steps from conversation
→ Presents: "I found 5 steps with 2 parameters..."
→ User confirms
→ Creates: skills/_ClassScheduleAudit/
```

**Example 2: Natural language variations**
```
"remember this workflow"
"save these steps as a routine"
"I want to do this again, save it"
"make this a repeatable thing"
"capture this procedure"
```

## Output

Captured routines become personal skills:

```
skills/_RoutineName/
├── SKILL.md           # Triggers and parameters
└── Workflows/
    └── Execute.md     # The captured steps
```

Personal skills use `_` prefix (never shared) and can be invoked via natural language triggers defined during capture.

## Tools

| Tool | Purpose |
|------|---------|
| `ExtractWorkflow.ts` | Parse transcript, extract successful steps |
| `SynthesizeSkill.ts` | Generate skill files from extracted data |
