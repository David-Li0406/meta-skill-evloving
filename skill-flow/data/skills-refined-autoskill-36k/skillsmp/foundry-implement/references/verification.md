# Verification Task Workflow

**Entry:** Routed here from Task Type Dispatch when task has `type: "verify"`

## Mark Task In Progress

```bash
mcp__plugin_foundry_foundry-mcp__task action="start" spec_id={spec-id} task_id={task-id}
```

## Detect Verification Type

Read `verification_type` from task metadata (already available from `task action="prepare"` or `task action="info"`):

```bash
mcp__plugin_foundry_foundry-mcp__task action="info" spec_id={spec-id} task_id={task-id}
```

## Dispatch by Verification Type

| verification_type | Skill Invocation |
|-------------------|------------------|
| `"run-tests"` | `Skill(foundry:foundry-test)` |
| `"fidelity"` | `Skill(foundry:foundry-review)` |

**For fidelity reviews**, extract `scope` and `target` from task metadata to pass to the skill.

## Execute Verification Skill

**MANDATORY:** You MUST invoke the Skill. Do NOT perform manual verification by reading files.

**For fidelity review:**
```bash
Skill(foundry:foundry-review) "Review {scope} {target} in spec {spec-id}"
```

Example: `Skill(foundry:foundry-review) "Review phase phase-1 in spec my-spec-001"`

**For run-tests:**
```bash
Skill(foundry:foundry-test) "Run tests for spec {spec-id}"
```

## Present Results

After the skill returns:
1. Display the verdict (pass/fail/partial)
2. List any deviations or failures found
3. Show recommendations from the review

## Complete or Remediate

**If verdict = pass:**
```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id={spec-id} task_id={task-id} completion_note="Fidelity review passed with verdict: {verdict}."
```

**If verdict = fail or partial:**
- Do NOT mark the verify task complete
- Present failures to user via `AskUserQuestion`
- Options: "Fix Issues & Re-run", "Create Remediation Tasks", "Override & Complete"
- If user chooses to fix, address deviations then re-run verification skill

## Return to Main Workflow

After verification task is complete, go to **Surface Next Recommendation** to continue with the next task.
