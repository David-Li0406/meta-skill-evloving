# Beads Integration

## Automatic Task Creation

### create-beads-tasks.sh

```bash
#!/bin/bash
# create-beads-tasks.sh

# Parse requirements file
REQUIREMENTS_FILE=".claude/extracted-requirements.md"

# Create epic
EPIC_ID=$(bd create \
  --type epic \
  --title "$FEATURE_TITLE" \
  --description "$(cat $REQUIREMENTS_FILE)")

# Parse acceptance criteria (lines starting with - or numbers)
grep -E "^-|^[0-9]+\." "$REQUIREMENTS_FILE" | while read -r criterion; do
  # Clean criterion (remove leading markers)
  criterion=$(echo "$criterion" | sed 's/^[- 0-9.]*//')

  if [ -n "$criterion" ]; then
    # Create subtask
    TASK_ID=$(bd create \
      --type task \
      --title "$criterion" \
      --priority 2 \
      --deps "$EPIC_ID")

    echo "Created task: $TASK_ID - $criterion"
  fi
done

# Store epic ID
echo "$EPIC_ID" > .claude/current-epic.txt
```

---

## Workflow Routing

Based on extracted requirements, route to appropriate workflow:

```bash
# Complex feature with multiple components
if [ "$complexity" = "high" ] && [ "$component_count" -gt 3 ]; then
  workflow="/reactree-dev"
  create_beads_epic=true
fi

# Standard feature
if [ "$intent" = "feature" ] && [ "$complexity" = "medium" ]; then
  workflow="/reactree-feature"
  create_beads_tasks=true
fi

# Debugging
if [ "$intent" = "debug" ]; then
  workflow="/reactree-debug"
  create_beads_tasks=false
fi

# Refactoring
if [ "$intent" = "refactor" ]; then
  workflow="/reactree-dev --refactor"
  create_beads_tasks=true
fi
```

---

## Output Format

### Structured Requirements File

**Location**: `.claude/extracted-requirements.md`

```markdown
---
intent: feature
confidence: high
complexity: medium
components: 3
created_at: 2026-01-02T10:30:00Z
---

## User Story

**As a** [actor]
**I want** [feature]
**So that** [benefit]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Components

- Component 1
- Component 2
- Component 3

## Suggested Technology

- Technology A
- Technology B

## Task Breakdown

1. Task 1 (Database)
2. Task 2 (Models)
3. Task 3 (Services)
4. Task 4 (Controllers)
5. Task 5 (Testing)

## Beads Epic

Created: EPIC-ID
Tasks: TASK-001, TASK-002, TASK-003
```

---

## Smart Detection Integration

### detect-intent.sh Enhancement

```bash
# In detect-intent.sh (after intent scoring)

# Extract requirements
if extract_requirements "$USER_PROMPT"; then
  # Create beads tasks if enabled
  AUTO_CREATE=$(grep '^auto_create_beads_tasks:' .claude/reactree-rails-dev.local.md | sed 's/.*: *//')

  if [ "$AUTO_CREATE" = "true" ]; then
    bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/create-beads-tasks.sh "$USER_PROMPT"
  fi
fi
```
