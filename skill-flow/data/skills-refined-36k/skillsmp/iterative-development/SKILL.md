---
name: iterative-development
description: |
  Load when adding deltas or analyzing impact on existing framework. Supports progressive development without requiring everything upfront. Used by /add-delta and /analyze-impact commands.
---

# Iterative Development Skill

Supports adding deltas and analyzing impact without full upfront planning.

## When to Load

Load this skill for:
- `/katachi:add-delta` - Add new delta on-the-go
- `/katachi:analyze-impact` - Analyze change impact

## Philosophy

The framework should support "add as you go" not "define everything upfront":

- Deltas can be added mid-project
- Dependencies are analyzed dynamically
- Quick-start mode for MVPs

## Add Delta Workflow

### 1. Capture Delta Description

Ask user to describe the delta:
- What does it do?
- Who uses it?
- Any known dependencies?

### 2. Assign ID

Deltas follow the pattern: `DLT-NNN`

**Process:**
1. Read existing deltas from DELTAS.md
2. Assign next available sequential ID
3. Confirm with user

```python
# Example categories (domain-oriented, organized by user capability area)
AUTH - Authentication flows (Login, Logout, Password Reset, Session Timeout)
USER - User management (Registration, Profile, Settings, Account Deletion)
ORDERS - Order management (Create Order, View Orders, Cancel Order)
PAYMENTS - Payment flows (Checkout, Refund, Payment Methods)
ADMIN - Admin capabilities (Manage Users, View Reports, System Settings)
CORE - Core infrastructure (when truly cross-cutting and not user-facing)
```

If new category needed, confirm with user before creating.

### 3. Assign ID

Find next available ID in category:

```bash
# Check existing IDs
python scripts/deltas.py status list --category CORE

# Result: CORE-001, CORE-002, CORE-003
# New ID: CORE-004
```

### 4. Capture Complexity

Ask user for complexity estimate:
- **Easy**: 1-2 hours, straightforward
- **Medium**: Half day, some complexity
- **Hard**: Full day+, significant complexity

### 5. Analyze Dependencies

**Option A: User knows dependencies**
- Ask: "Does this depend on any existing deltas?"
- Validate dependencies exist

**Option B: Agent analysis**
- Dispatch `katachi:impact-analyzer` with delta description
- Agent identifies likely dependencies based on description
- Present to user for confirmation

### 6. Update DELTAS.md

Add new delta entry:

```markdown
| CORE-004 | New delta description | Medium | ✗ Defined |
```

### 7. Update DEPENDENCIES.md

Add to dependency matrix:

```bash
python scripts/deltas.py deps add-delta CORE-004
python scripts/deltas.py deps add-dep CORE-004 CORE-001  # If depends on CORE-001
```

### 8. Offer Next Step

After adding:
- "CORE-004 added. Create spec now? [Y/N]"
- If yes, transition to `/katachi:spec-delta CORE-004`

## Impact Analysis Workflow

### 1. Capture Change Description

Ask user to describe the proposed change:
- What is being changed?
- Why is this change needed?
- What areas might be affected?

### 2. Dispatch Impact Analyzer

```python
Task(
    subagent_type="katachi:impact-analyzer",
    prompt=f"""
Analyze the impact of this proposed change:

## Change Description
{change_description}

## DELTAS.md
{deltas_content}

## DEPENDENCIES.md
{dependencies_content}

## Existing Specs
{list_of_spec_paths}

Trace dependencies and report affected deltas.
"""
)
```

### 3. Present Findings

Show user:
- Directly affected deltas
- Transitively affected deltas (dependency chain)
- Documents needing updates
- Risk assessment

### 4. Ask Next Steps

Based on impact level:

**Isolated:**
- "This change is isolated to X. Proceed with implementation?"

**Moderate:**
- "This affects N deltas. Review affected specs before proceeding?"

**Significant:**
- "This is a significant change. Create an ADR to document this decision?"

**Structural:**
- "This affects core architecture. Recommend detailed analysis before proceeding."

## Quick-Start Mode

For new projects, offer quick-start:

1. **Minimal VISION.md**
   - Problem statement
   - MVP scope (not full scope)
   - Key workflows (top 3)

2. **MVP Deltas Only**
   - Extract only deltas needed for MVP
   - Skip nice-to-haves
   - Aim for 5-10 deltas max

3. **Simple Dependencies**
   - Linear dependencies where possible
   - Skip complex dependency analysis

4. **First Delta Guidance**
   - Guide through first spec
   - Establish patterns early
   - User learns workflow on real work
