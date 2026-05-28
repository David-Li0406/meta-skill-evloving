# DevOps

Deployment, CI/CD, infrastructure changes, and operational work.

## Mental Model

DevOps is about reliable delivery. Infrastructure changes are high-stakes.

```
Goal: Change to deployment, CI/CD, or infrastructure
         ↓
Plan: Detailed steps, rollback plan, verification steps
         ↓
Test: Validate plan in safe environment
         ↓
Execute: Implement with monitoring
         ↓
Verify: Confirm everything works
         ↓
Document: Record what was done
```

## Key Principles

### Plan Completely Before Executing
DevOps changes can be hard to reverse. Plan every step.
- What exactly will you do?
- In what order?
- What could go wrong at each step?
- How will you know each step succeeded?

### Always Have Rollback
Every change should be reversible.
- Document how to roll back
- Test rollback procedure if possible
- Know how to quickly recover if things go wrong

### Test Before Production
If possible, test in staging or similar environment first.
- Validate the procedure works
- Find problems in safe environment
- Build confidence before production

### Monitor During Execution
Watch metrics and logs while making changes.
- Know what normal looks like
- Watch for anomalies during changes
- Have alerts in place

### Stop on Problems
If something goes wrong, stop immediately.
- Don't push through
- Assess the situation
- Roll back if needed
- Get help if needed

### Document Everything
Future you (or someone else) needs to understand what was done.
- What was the goal?
- What was done?
- What issues occurred?
- How were they resolved?

## Agent Browser CLI Usage

Use browser to verify deployed changes.

**Verifying deployment:**
```bash
# After deployment, verify the site works
agent-browser open https://production-site.com
agent-browser snapshot -i
agent-browser click @key-element
agent-browser screenshot post-deploy.png
```

**Monitoring during rollout:**
```bash
# Check key pages work
agent-browser open https://production-site.com/login
agent-browser fill "[name='email']" "test@example.com"
agent-browser fill "[name='password']" "testpass"
agent-browser click "[type='submit']"
agent-browser screenshot login-verify.png
```

## What to Extract from Users

- Exact goal of the DevOps work
- Current state of infrastructure/deployment
- Risk tolerance and rollback requirements
- Testing environment availability
- Monitoring and alerting setup
- Human availability during execution
- Timeline and maintenance windows
- Success criteria

## Non-Negotiables

These are not optional:
- Rollback plan exists and is documented
- Rollback plan is tested (if possible)
- Monitoring is in place during execution
- Human can be reached if problems occur
- Changes are documented before and after

## Red Flags

You're doing it wrong if:
- "Let's just try it and see"
- No rollback plan
- No monitoring during execution
- Batching unrelated infrastructure changes
- Working on production without testing first
- Can't explain what each step does
- No one available to help if things go wrong
- Not documenting changes

## Story Structure for DevOps

Typical DevOps PRD structure:
1. Document goal and current state - what we're doing and why
2. Create detailed plan - step-by-step with rollback
3. Test in safe environment - validate plan works
4. Execute with monitoring - implement in production
5. Verify success - confirm everything works
6. Document completion - record what was done

## Risk Categories

| Risk Level | Characteristics | Approach |
|------------|-----------------|----------|
| Low | Reversible, no user impact | Standard process |
| Medium | Some user impact, reversible | Extra verification |
| High | User impact, harder to reverse | Maintenance window, full team |
| Critical | Data at risk, significant impact | Multiple approvals, extensive testing |
