---
name: stack-selection
description: Confirm final stack selection and document trade-offs. Use after stack-evaluation presents candidates, when user is ready to choose a stack.
---

# Final Stack Selection Confirmation

Confirm the user's final stack selection, document accepted trade-offs, and capture decision notes.

## Prerequisites

- Architecture brief from **architecture-refinement**
- Stack evaluation from **stack-evaluation**

## Process

### Step 1: Confirm Selection

Present top recommendations and ask user to confirm:

**Which stack would you like to proceed with?**

1. **[Top Recommendation]** - `<candidate>` (Score: X.X)
2. **[Runner-up]** - `<candidate>` (Score: X.X)
3. **[Other candidate]** - `<candidate>`
4. **Custom combination** - Define different stack

### Step 2: Acknowledge Trade-offs

Present known trade-offs for selected stack:

| Category | Trade-off | Impact |
|----------|-----------|--------|
| Cost | ... | low/medium/high |
| Ops Overhead | ... | low/medium/high |
| Vendor Lock-in | ... | low/medium/high |
| Learning Curve | ... | low/medium/high |

**Do you accept these trade-offs?**
- Yes, proceed
- No, reconsider (return to stack-evaluation)

### Step 3: Capture Decision Notes

Ask for additional context:
1. Why this stack over alternatives? (optional)
2. Specific concerns for implementation plan?
3. Timeline considerations?

### Step 4: Validate Local Dev Approach

Confirm local development approach works for the team.

## Output Contract

```yaml
selected_stack:
  stack_id: "<unique id>"
  name: "<name>"
  selected_at: "<ISO timestamp>"

  components:
    frontend:
      technology: "<tech>"
      hosting: "<hosting>"
    backend:
      technology: "<tech>"
      hosting: "<hosting>"
    database:
      technology: "<tech>"
      hosting: "<managed|self-hosted>"
    auth:
      provider: "<provider>"
    async:
      technology: "<tech>"
    storage:
      technology: "<tech>"

  local_dev:
    approach: "<docker-compose|local-k8s|hybrid|aspire>"
    time_to_first_run: "<estimate>"

  evaluation_summary:
    weighted_score: <score>
    rank: <rank>
    strongest_areas: []
    weakest_areas: []

  accepted_tradeoffs:
    - category: "<category>"
      description: "<trade-off>"
      mitigation: "<how to mitigate>"

  decision_notes:
    rationale: "<why chosen>"
    concerns: []
    timeline_considerations: "<notes>"

  references:
    architecture_brief_id: "<ref>"
    evaluation_id: "<ref>"
```

## Confirmation Summary

Present final confirmation:

---

### Stack Selection Confirmed

**Stack**: `<name>`

**Components**:
- Frontend: `<tech>` on `<hosting>`
- Backend: `<tech>` on `<hosting>`
- Database: `<tech>` (`<hosting>`)
- Auth: `<provider>`

**Local Development**: `<approach>` (Est. `<time>` to first run)

**Accepted Trade-offs**:
- `<trade-off 1>`
- `<trade-off 2>`

---

## Next Step

Proceed to **implementation-plan** skill to create execution-ready implementation plan.
