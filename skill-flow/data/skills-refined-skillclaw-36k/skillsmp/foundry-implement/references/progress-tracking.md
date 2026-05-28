# Progress Tracking

This reference describes how to track progress, update estimates, and record verification results.

## Tracking Progress

### Get Progress Summary

```bash
mcp__plugin_foundry_foundry-mcp__task action="progress" spec_id={spec-id}
```

Returns completed vs total tasks, percentage, and current phase.

### Update Phase Estimates

When actual work reveals that phase estimates need adjustment:

```bash
# Update estimated hours for a phase
mcp__plugin_foundry_foundry-mcp__authoring action="phase-update-metadata" spec_id={spec-id} phase_id="phase-2" estimated_hours=12.5

# Update phase description and purpose
mcp__plugin_foundry_foundry-mcp__authoring action="phase-update-metadata" spec_id={spec-id} phase_id="phase-2" description="Updated scope" purpose="Refined objective"

# Preview changes before applying
mcp__plugin_foundry_foundry-mcp__authoring action="phase-update-metadata" spec_id={spec-id} phase_id="phase-2" estimated_hours=8.0 dry_run=true
```

**Use cases:**
- Task completion reveals more/less work than estimated
- Scope changes during implementation
- Post-phase retrospective adjustments

## Verification Recording

### Manual Verification

Document verification results:

```bash
# Verification passed
mcp__plugin_foundry_foundry-mcp__verification action="add" spec_id={spec-id} verify_id={verify-id} result="PASSED" command="npm test" output="All tests passed"

# Verification failed
mcp__plugin_foundry_foundry-mcp__verification action="add" spec_id={spec-id} verify_id={verify-id} result="FAILED" command="npm test" output="3 tests failed" issues="List of issues"

# Partial success
mcp__plugin_foundry_foundry-mcp__verification action="add" spec_id={spec-id} verify_id={verify-id} result="PARTIAL" notes="Most checks passed, minor issues remain"
```

### Automatic Verification

If verification tasks have metadata specifying how to execute:

```bash
# Execute verification based on metadata
mcp__plugin_foundry_foundry-mcp__verification action="execute" spec_id={spec-id} verify_id={verify-id}

# Execute and automatically record result
mcp__plugin_foundry_foundry-mcp__verification action="execute" spec_id={spec-id} verify_id={verify-id} record=true
```

**Requirements:** Verification task must have `skill` or `command` in its metadata.

### Configurable Failure Handling

Verification tasks can specify custom failure behavior via `on_failure` metadata:

```json
{
  "verify-1-1": {
    "metadata": {
      "on_failure": {
        "consult": true,
        "revert_status": "in_progress",
        "max_retries": 2,
        "continue_on_failure": false
      }
    }
  }
}
```

**on_failure fields:**
- `consult` (boolean) - Recommend AI consultation for debugging
- `revert_status` (string) - Status to revert parent task to on failure
- `max_retries` (integer) - Number of automatic retry attempts (0-5)
- `continue_on_failure` (boolean) - Continue with other verifications if this fails

## Progress Metrics

Key metrics tracked:
- **Completed tasks** - Tasks marked as completed
- **Total tasks** - All tasks in spec
- **Percentage** - Completion percentage
- **Current phase** - Active phase being worked on
- **Blocked tasks** - Tasks that cannot proceed
