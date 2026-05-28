# Inbox Triage

Process inbox items systematically: analyze, categorize, and convert to specs/tasks.

## Workflow

### 1. Gather Context

```bash
kspec session start --full
kspec inbox list
```

### 2. Categorize Items

Group inbox items by type:
- **Bugs** - implementation issues, errors
- **Spec gaps** - missing or incomplete specs
- **Quick wins** - small, well-defined improvements
- **Larger features** - need plan mode to design
- **Process/workflow** - meta improvements
- **Delete candidates** - outdated, duplicates, already done

Present categories to user for alignment.

### 3. Process Each Item

Decision tree:

```
Is it still relevant?
├─ No → Delete: kspec inbox delete @ref --force
└─ Yes → Does spec cover this?
         ├─ No spec exists → Create spec first
         │   └─ Small: item add + ac add
         │   └─ Large: Enter plan mode
         ├─ Spec exists but incomplete → Update spec (add AC)
         └─ Spec complete → Promote to task
```

### 4. Spec-First Processing

For each behavior change:

1. **Check coverage**: `kspec item list | grep <relevant>`
2. **Identify gaps**: Does spec have description AND acceptance criteria?
3. **Update spec**:
   ```bash
   kspec item set @ref --description "..."
   kspec item ac add @ref --given "..." --when "..." --then "..."
   ```
4. **Derive or promote**:
   ```bash
   kspec derive @spec-ref           # If spec exists
   kspec inbox promote @ref --title "..." --spec-ref @spec  # If from inbox
   ```

### 5. Plan Mode for Larger Items

When an item needs design work:

1. Enter plan mode
2. Explore codebase for patterns/context
3. Design spec structure and implementation approach
4. Write plan, exit for approval
5. Execute: create spec, add AC, derive task

## Quick Commands

```bash
# Triage decisions
kspec inbox delete @ref --force     # Remove irrelevant
kspec inbox promote @ref --title "..." --spec-ref @spec  # Convert to task

# Spec updates
kspec item set @ref --description "..."
kspec item ac add @ref --given "..." --when "..." --then "..."

# Create spec for gap
kspec item add --under @parent --title "..." --type requirement --slug slug

# Derive task from spec
kspec derive @spec-ref
```

## Common Patterns

| Pattern | Action |
|---------|--------|
| Already implemented | Verify impl exists → check spec for gaps → fill gaps → delete inbox |
| Duplicate of existing | Verify original covers scope → reference it → delete inbox |
| Small flag/option | Update spec description + AC → derive task |
| New command | Plan mode → design spec → create spec + AC → derive task |
| Bug report | Check spec coverage → update spec if needed → promote with spec-ref |
| Vague idea | Ask for clarification or leave in inbox for later |

## Key Principles

- **Ask one question at a time** - Use AskUserQuestion for decisions
- **Spec before task** - Fill spec gaps before creating tasks
- **AC is required** - Specs without acceptance criteria are incomplete
- **Use CLI, not YAML** - All changes through kspec commands
- **Delete freely** - Outdated or duplicate items should go
