# Guardrail: Testing Sanity Check

## When to Run

Run this sanity check **before finalizing any project plan**.

## Checklist

Before approving a plan, verify ALL of the following:

### 1. Every Feature Has a Testing Plan

- [ ] Each task specifies what tests are required
- [ ] "Add tests" is not acceptable — must specify WHAT tests
- [ ] Testing ownership is assigned

### 2. Backend Changes Have Regression Tests

- [ ] Existing behaviors that must be preserved are listed
- [ ] Tests protecting critical paths are identified
- [ ] Behavior changes are explicitly documented

### 3. CI Gates Are Explicit

- [ ] Required CI checks are listed for each phase
- [ ] Coverage requirements are defined (or explicitly waived with reason)
- [ ] Integration test requirements are clear

### 4. Engineers Cannot Merge Without Tests

- [ ] Task files include testing requirements section
- [ ] PR rejection criteria are clear
- [ ] Testing expectations are binary (not "should have tests")

## Failure Handling

If any check fails:

1. **STOP** — do not finalize the plan
2. **IDENTIFY** — which tasks are missing testing requirements
3. **FIX** — add explicit testing requirements
4. **RE-RUN** — this sanity check

## Red Flags

Automatic failure if you see:

- "Add appropriate tests" (too vague)
- "Testing: TBD" (not defined)
- "Tests not required" without justification
- Backend changes with no regression protection
- New features with no unit test requirements

## Output

After passing this check, add to the plan:

```markdown
## Testing Sanity Check

✅ Passed on <date>

- Features with testing plans: <N>/<N>
- Backend changes with regression tests: <N>/<N>
- CI gates defined: Yes
- Merge requirements clear: Yes
```
