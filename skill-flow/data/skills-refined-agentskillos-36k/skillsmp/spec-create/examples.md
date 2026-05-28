# Spec Creation Examples

Example workflows for invoking the spec-create skill in different contexts.

---

## From ExitPlanMode

User accepts plan after planning phase:

```
User accepts plan for "Add Temporal Join Support"
→ Invoke spec-creation skill
→ Task name: add-temporal-joins
→ Gather context from codebase
→ Create ./specs/active/add-temporal-joins/
→ Generate 3 documents with actual code context
→ Extract first phase tasks to TodoWrite
→ Start implementation
```

**Flow**: Plan mode → ExitPlanMode → User approval → Automatic invocation

---

## From Command

Explicit command invocation:

```
/spec.create nested-view-refactor
→ Invoke spec-creation skill
→ Task name: nested-view-refactor
→ Follow workflow steps
```

**Flow**: User types command → Skill invoked with task name

---

## Autonomous Invocation

Claude recognizes need for spec based on task complexity:

```
User: "Let me start working on this, I need to track it properly"
Claude recognizes: Complex task, should create spec
→ Autonomously invokes spec-creation skill
→ Asks for task name if unclear
→ Creates documents
```

**Flow**: User indicates complex work → Claude assesses → Proactive skill invocation

---

## With Script Automation

Using helper script for quick scaffolding:

```bash
# Quick directory + template setup
uv run .claude/skills/spec-create/scripts/setup-spec.py --task-name add-temporal-joins

# Then fill in project-specific context manually
```

**Flow**: Script creates structure → Human adds details → Start working
