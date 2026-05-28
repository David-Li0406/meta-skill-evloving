# Linear Agent Patterns

Integration patterns for Linear AgentActivities and proper state management.

---

## Overview

Linear agents have specific behavioral expectations. linear-audit should follow these patterns when interacting with Linear programmatically.

**Key principle:** Use AgentActivities (frozen snapshots) instead of editable comments for audit trails.

---

## AgentActivity Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| `thought` | Show agent is working | Initial acknowledgment, progress updates |
| `response` | Deliver findings/results | Synthesis complete, audit finished |
| `elicitation` | Request human input | Disposition decisions, clarification |
| `error` | Report failure | Tool failures, timeouts, blocked states |

### Activity Timing Requirements

| Requirement | Value | Source |
|-------------|-------|--------|
| First response | <10 seconds | Linear docs: "shown as unresponsive" |
| Session staleness | 30 minutes | Linear docs: "recoverable by sending another activity" |
| Thought frequency | Every meaningful step | Best practice |

---

## State Management Protocol

### Starting Work on an Issue

```bash
# 1. Move issue to "started" state
linear issue edit $ISSUE --state "In Progress"

# 2. Set delegate to agent identity
linear issue edit $ISSUE --delegate "linear-audit-agent"

# 3. Emit thought activity
linear activity create $ISSUE --type thought --body "Analyzing issue context..."
```

### During Analysis

```bash
# Emit thought activities for progress
linear activity create $ISSUE --type thought --body "Gathering codebase context..."
linear activity create $ISSUE --type thought --body "Checking for staleness markers..."
linear activity create $ISSUE --type thought --body "Synthesizing findings..."
```

### Requesting Human Input

```bash
# Emit elicitation for HIL checkpoint
linear activity create $ISSUE --type elicitation --body "$(cat <<EOF
**Disposition Decision Needed**

This issue appears stale (45 days, no activity). Options:
1. Archive - remove from active work
2. Refresh - update context and keep
3. Keep as-is - retain without changes

Which approach?
EOF
)"
```

### Completing Work

```bash
# 1. Emit response with findings
linear activity create $ISSUE --type response --body "$(cat <<EOF
**Audit Complete**

- Context: Fresh (updated today)
- Status: Ready for V1
- Recommendation: None, issue is well-formed

See full audit: $GIST_URL
EOF
)"

# 2. Return to original state (if unchanged)
linear issue edit $ISSUE --state "$ORIGINAL_STATE"

# 3. Clear delegate
linear issue edit $ISSUE --delegate ""
```

### Handling Errors

```bash
# Emit error activity
linear activity create $ISSUE --type error --body "$(cat <<EOF
**Audit Failed**

Error: Unable to gather codebase context
Reason: Project path not found
Action: Verify project is accessible and retry

Trace: $TRACE_ID
EOF
)"
```

---

## Activity Content Patterns

### Thought Activity (progress)

```markdown
**Analyzing Issue Context**

- Checking for issue-context markers...
- Found: 2 markers (analysis + agent prompt)
- Freshness: 8 days (within threshold)

Proceeding to codebase analysis.
```

### Response Activity (findings)

```markdown
**Issue Audit Complete**

| Criterion | Status |
|-----------|--------|
| Context markers | ✅ Present |
| Freshness | ✅ 8 days |
| Description | ✅ Clear |
| Acceptance criteria | ⚠️ Missing |

**Recommendation:** Add acceptance criteria to complete V1 readiness.

*Trace: tr_arb20250122*
```

### Elicitation Activity (HIL)

```markdown
**Input Needed: Disposition**

ARB-234 "Refactor auth module" shows signs of staleness:
- Created: 6 months ago
- Last activity: 4 months ago
- References: Old Clerk patterns (already migrated)

**Options:**
1. **Archive** - Remove from active work, create fresh issue if needed
2. **Update** - Rewrite description to reflect current state
3. **Keep** - Retain as reminder even if imprecise

Which approach fits your intent?
```

### Error Activity (failure)

```markdown
**Audit Error**

Unable to complete analysis for ARB-401.

**Error:** Code state specialist timed out
**Cause:** `verify --coverage` exceeded 180s timeout
**Impact:** Coverage data unavailable for this audit

**Recovery options:**
1. Retry with extended timeout
2. Skip coverage, proceed with partial audit
3. Abort and investigate timeout cause

Trace: tr_arb20250122
```

---

## Audit Session Flow

### Full Audit Sequence

```
1. [thought]  "Starting audit for ARB..."
2. [thought]  "Gathering codebase context..."
3. [thought]  "Spawning 4 specialists..."
4. [thought]  "Code state: complete (confidence 9)"
5. [thought]  "Architecture: complete (confidence 8)"
6. [thought]  "Linear state: complete (confidence 8)"
7. [thought]  "V1 gaps: complete (confidence 8)"
8. [response] "Synthesis complete. 2 blockers, 3 gaps..."
9. [elicitation] "Disposition needed for 3 issues..."
10. [response] "Audit complete. 8 enriched, 3 archived."
```

### Quick Audit Sequence

```
1. [thought]  "Quick audit for ARB..."
2. [thought]  "Checking issue counts and top gaps..."
3. [response] "Quick audit complete. 45 issues, 5 missing context."
```

---

## Integration with trails

Correlate Linear AgentActivities with trails events:

```bash
# Start audit trace
TRACE_ID=$(trails trail record --agent claude --new-trace --action started --task "linear-audit: ARB" --json -q | jq -r '.trace_id')

# Emit thought with trace reference
linear activity create $ISSUE --type thought --body "Starting audit... (trace: $TRACE_ID)"

# Record each phase
trails trail record --agent claude --trace-id $TRACE_ID --action progress --task "specialists complete"

# Complete with both systems
linear activity create $ISSUE --type response --body "Audit complete. Trace: $TRACE_ID"
trails trail record --agent claude --trace-id $TRACE_ID --action completed --task "ARB audit done" --confidence 9
```

---

## Best Practices

### DO

- ✅ Respond within 10 seconds of receiving audit trigger
- ✅ Use AgentActivities for all audit communication
- ✅ Move issues to "started" when beginning work
- ✅ Set delegate to make agent role explicit
- ✅ Emit thought activities for meaningful progress
- ✅ Use elicitation for disposition decisions
- ✅ Include trace IDs in all activities
- ✅ Return issues to original state when done

### DON'T

- ❌ Use editable comments for audit trails (use frozen activities)
- ❌ Leave issues in "started" state after audit
- ❌ Skip the initial thought activity (causes "unresponsive" state)
- ❌ Exceed 30 minutes without activity (session goes stale)
- ❌ Leave delegate set after completing audit
- ❌ Emit error without recovery options

---

## Webhook Triggers (future)

For automated audit triggers, listen to these webhooks:

| Webhook | Trigger Condition | Action |
|---------|-------------------|--------|
| Issue created | New issue without context | Queue for enrichment |
| Issue state changed | Moved to "Todo" | Check V1 readiness |
| Bulk import | Many issues created | Trigger batch audit |
| Timer | 14 days since last audit | Suggest re-audit |

### Example Webhook Handler

```typescript
// Future: automated audit triggers
webhooks.on("issue.created", async (issue) => {
  if (!hasContextMarkers(issue)) {
    await emitThought(issue.id, "New issue detected. Queuing for context enrichment...");
    await queueEnrichment(issue.id);
  }
});

webhooks.on("issue.state_changed", async (issue, from, to) => {
  if (to === "Todo" && !isV1Ready(issue)) {
    await emitElicitation(issue.id, "Issue moved to Todo but not V1 ready. Run audit?");
  }
});
```

---

## GraphQL Patterns

### Query AgentActivities for Session

```graphql
query AgentSession($agentSessionId: String!) {
  agentSession(id: $agentSessionId) {
    activities {
      edges {
        node {
          updatedAt
          content {
            ... on AgentActivityThoughtContent {
              body
            }
            ... on AgentActivityResponseContent {
              body
            }
            ... on AgentActivityElicitationContent {
              body
            }
            ... on AgentActivityErrorContent {
              body
            }
          }
        }
      }
    }
  }
}
```

### Get Team's Started State

```graphql
query TeamStartedStatuses($teamId: String!) {
  team(id: $teamId) {
    states(filter: { type: { eq: "started" } }) {
      nodes {
        id
        name
        position
      }
    }
  }
}
```

---

## References

- [Linear Agent Best Practices](https://linear.app/developers/agent-best-practices) - official docs
- [Linear GraphQL API](https://linear.app/developers/graphql) - API reference
- [Linear TypeScript SDK](https://linear.app/developers/sdk) - SDK patterns
