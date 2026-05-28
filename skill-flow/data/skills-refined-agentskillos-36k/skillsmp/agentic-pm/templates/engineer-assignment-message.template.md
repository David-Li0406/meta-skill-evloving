# Engineer Assignment: TASK-XXX

> **NON-NEGOTIABLE: AGENT ID CAPTURE REQUIRED**
>
> You MUST record your Agent ID immediately when this task starts. This is mandatory.
> - Record your **Agent ID** from the Task tool output
> - Metrics are auto-captured via SubagentStop hook
>
> **Agent ID:** _______________

---

## Summary

You are assigned to **TASK-XXX: <Title>**.

## Task File Location

```
.claude/plans/tasks/TASK-XXX-<slug>.md
```

Read the full task file before starting.

## Quick Context

- **Goal**: <1 sentence>
- **Phase**: Phase <N>
- **Dependencies**: <none / TASK-YYY must complete first>
- **Conflicts with**: <none / TASK-ZZZ - do not run in parallel>

## Key Points

1. **Non-goals**: Review the non-goals section carefully. Do not expand scope.
2. **Integration**: Your work will be used by <TASK-AAA, TASK-BBB>.
3. **Testing**: <specific testing requirements>
4. **Branch**: Create `feat/<ID>-<slug>` from `<base branch>`.

## Workflow

1. Read the full task file
2. Record your Agent ID immediately
3. Create your feature branch
4. Implement according to acceptance criteria
5. Complete the Implementation Summary section
6. Run all CI checks locally
7. Open PR targeting `<branch>` with Agent ID noted
8. Have senior-engineer-pr-lead agent review the PR

## Completion Reporting (REQUIRED)

After your task is complete and PR is merged, report:

```
## Task Completion Report: TASK-XXX

**Status:** Complete
**PR:** #<number>
**Engineer Agent ID:** <your_agent_id>

### Metrics (Auto-Captured)

Run: `grep "<your_agent_id>" .claude/metrics/tokens.jsonl | jq '.'`

| Metric | Value |
|--------|-------|
| Total Tokens | <from hook> |
| Duration | <from hook> seconds |
| API Calls | <from hook> |

### Variance Notes
(if significantly different from estimate of ~<X>K tokens)
<explanation>
```

Metrics are auto-captured via SubagentStop hook. The PM will lookup metrics using your Agent ID.

## Stop and Ask If

- You're unsure about acceptance criteria
- You discover work outside the defined scope
- You encounter blockers from dependencies
- You need to deviate from the implementation notes

## Communication

- Questions: Post in <channel/thread>
- Blockers: Escalate immediately
- Updates: <frequency/channel>

## Timeline

- **Start**: <date/time>
- **Integration checkpoint**: <date/time>
- **Phase deadline**: <date/time>

---

Good luck! Ping if you have questions.
