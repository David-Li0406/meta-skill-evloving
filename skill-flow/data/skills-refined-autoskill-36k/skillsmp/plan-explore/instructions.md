# Plan Exploration Implementation Instructions

This document provides detailed implementation steps for the plan-explore skill.

## High-Level Workflow

1. Parse command-line arguments
2. Load configuration from design.config.json
3. Discover all plan files
4. Parse plan frontmatter (with caching)
5. Apply filters
6. Perform health analysis
7. Generate output in requested format
8. Display results

## Step-by-Step Implementation

### Step 1: Parse Arguments

Parse all command-line arguments and flags:

```bash
# Initialize defaults
MODULE=""
STATUS_FILTER=""
DESIGN_DOC=""
OWNER=""
FORMAT="summary"
SHOW_PHASES=false
SHOW_HEALTH=true
ORPHANS_ONLY=false
STALE_ONLY=false
BLOCKED_ONLY=false
AGE_THRESHOLD=30
```

**Argument patterns:**

- Positional argument: module name (e.g., `effect-type-registry`)
- `--status=value` or `--status=value1,value2`
- `--design-doc=path`
- `--owner=username`
- `--format=summary|detailed|timeline|json`
- Boolean flags: `--show-phases`, `--orphans`, `--stale`, `--blocked`
- `--age-threshold=days`

**Validation:**

- Format must be one of: summary, detailed, timeline, json
- Status values must be valid: ready, in-progress, blocked, completed, abandoned
- Age threshold must be positive integer

### Step 2: Load Configuration

Read `.claude/design/design.config.json`:

```bash
PLANS_DIR=$(jq -r '.paths.plans' .claude/design/design.config.json)
STALE_THRESHOLD=$(jq -r '.quality.plans.stalenessThresholdDays // 30' .claude/design/design.config.json)
```

**Configuration fields used:**

- `paths.plans` - Plan directory location
- `quality.plans.stalenessThresholdDays` - Default staleness threshold
- `modules` - Valid module names for filtering

### Step 3: Discover Plan Files

Find all plan markdown files:

```bash
# Find all .md files in plans directory (excluding _archive)
PLAN_FILES=$(find "$PLANS_DIR" -maxdepth 1 -name "*.md" -type f)
```

**Notes:**

- Exclude `_archive/` subdirectory
- Only include `.md` files
- Sort by modification time (newest first)

### Step 4: Parse Plan Frontmatter

For each plan file, extract YAML frontmatter:

```bash
# Extract frontmatter between --- delimiters
extract_frontmatter() {
  local file=$1
  sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d'
}

# Parse specific field
get_field() {
  local frontmatter=$1
  local field=$2
  echo "$frontmatter" | grep "^$field:" | cut -d':' -f2- | \
    sed 's/^ *//' | tr -d '"'
}
```

**Fields to extract:**

- name
- title
- status
- progress
- modules (array)
- implements (array)
- owner
- created
- updated
- started
- completed
- target-completion
- blocked-by (array)
- phases (array)

**Caching strategy:**

- Store parsed metadata in associative array
- Use file mtime as cache key
- Cache TTL: 5 minutes
- Cache location: `/tmp/plan-explore-cache-{user}`

### Step 5: Apply Filters

Filter plans based on provided criteria:

**Module filter:**

```bash
if [[ -n "$MODULE" ]]; then
  # Check if plan's modules array contains $MODULE
  modules=$(get_array_field "$frontmatter" "modules")
  if ! echo "$modules" | grep -q "$MODULE"; then
    continue  # Skip this plan
  fi
fi
```

**Status filter:**

```bash
if [[ -n "$STATUS_FILTER" ]]; then
  plan_status=$(get_field "$frontmatter" "status")
  # STATUS_FILTER can be comma-separated: "ready,in-progress"
  if ! echo "$STATUS_FILTER" | grep -q "$plan_status"; then
    continue  # Skip this plan
  fi
fi
```

**Design doc filter:**

```bash
if [[ -n "$DESIGN_DOC" ]]; then
  implements=$(get_array_field "$frontmatter" "implements")
  if ! echo "$implements" | grep -q "$DESIGN_DOC"; then
    continue  # Skip this plan
  fi
fi
```

**Owner filter:**

```bash
if [[ -n "$OWNER" ]]; then
  plan_owner=$(get_field "$frontmatter" "owner")
  if [[ "$plan_owner" != "$OWNER" ]]; then
    continue  # Skip this plan
  fi
fi
```

**Special filters:**

- `--orphans`: Skip if implements array is non-empty
- `--stale`: Skip if updated within age threshold
- `--blocked`: Skip if status != "blocked"

### Step 6: Perform Health Analysis

For each filtered plan, analyze health:

**Staleness check:**

```bash
check_staleness() {
  local updated=$1
  local age_threshold=$2

  local updated_epoch=$(date -j -f "%Y-%m-%d" "$updated" +%s \
    2>/dev/null || echo 0)
  local now_epoch=$(date +%s)
  local days_old=$(( (now_epoch - updated_epoch) / 86400 ))

  if (( days_old > age_threshold )); then
    echo "stale"
  fi
}
```

**Orphan check:**

```bash
check_orphan() {
  local implements=$1

  if [[ -z "$implements" ]] || [[ "$implements" == "[]" ]]; then
    echo "orphan"
  fi
}
```

**Blocker analysis:**

```bash
check_blockers() {
  local blocked_by=$1

  # Parse blocked-by array
  # Check if blockers are other plans or external
  # Detect cascading blocks (blocker is also blocked)
  # Detect stale blockers (blocker is completed)
}
```

**Schedule analysis:**

```bash
check_schedule() {
  local target=$1
  local progress=$2
  local started=$3

  if [[ -z "$target" ]]; then
    return
  fi

  local target_epoch=$(date -j -f "%Y-%m-%d" "$target" +%s)
  local now_epoch=$(date +%s)

  if (( target_epoch < now_epoch )) && (( progress < 100 )); then
    echo "overdue"
  fi
}
```

**Progress validation:**

```bash
check_progress_alignment() {
  local status=$1
  local progress=$2

  case "$status" in
    ready)
      if (( progress != 0 )); then
        echo "misaligned: status=ready but progress=$progress%"
      fi
      ;;
    in-progress|blocked)
      if (( progress == 0 || progress == 100 )); then
        echo "misaligned: status=$status but progress=$progress%"
      fi
      ;;
    completed)
      if (( progress != 100 )); then
        echo "misaligned: status=completed but progress=$progress%"
      fi
      ;;
  esac
}
```

### Step 7: Generate Output

Format results based on `--format` flag:

#### Summary Format

```text
Implementation Plans Overview
============================

Status Summary:
  Ready: {count} plans
  In Progress: {count} plans (avg {pct}% complete)
  Blocked: {count} plans
  Completed: {count} plans
  Abandoned: {count} plans

Active Plans (In Progress):
  • {title} [{progress}%] - {age}
    Modules: {modules}
    Design: {design-docs}
    [Blocked by: {blockers}]

Health Insights:
  ⚠️  {count} plans stale (>30 days since update)
  ⚠️  {count} orphaned plans (no design docs)
  ✅ All blocked plans have clear dependencies

Next Actions:
  1. {recommendation}
  2. {recommendation}
```

**Algorithm:**

1. Count plans by status
2. Calculate average progress for in-progress plans
3. Show in-progress plans sorted by age (oldest first)
4. Collect health issues
5. Generate actionable recommendations

#### Detailed Format

For each plan, show:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Plan: {name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: {title}
Status: {status} ({progress}%)
Module(s): {modules}

Timeline:
  Created: {created}
  Started: {started}
  Target: {target-completion}
  Completed: {completed}

Design Documents:
  - {doc1}
  - {doc2}

[Phases:
  • Phase 1: {name} - {status} ({completion}%)
  • Phase 2: {name} - {status} ({completion}%)
]

[Blocked By:
  - {blocker1}
  - {blocker2}
]

Health:
  {health issues if any}
```

#### Timeline Format

Group by month, show chronologically:

```text
Implementation Timeline
======================

{Month Year}
------------
✅ {date-range}: {title} (completed)
🚧 {date-range}: {title} ({progress}% - in progress)
⏸️  {date-range}: {title} (blocked)
📅 {date-range}: {title} (ready)

Health:
  {count} plans behind schedule
  {count} plans on track
  {count} plans ahead of schedule
```

**Algorithm:**

1. Sort plans by started date (or created if not started)
2. Group by year-month
3. Show in chronological order
4. Use emoji indicators for status
5. Show schedule health summary

#### JSON Format

```json
{
  "summary": {
    "total": 23,
    "by_status": {
      "ready": 3,
      "in-progress": 5,
      "blocked": 2,
      "completed": 12,
      "abandoned": 1
    },
    "average_progress": 45
  },
  "plans": [
    {
      "name": "plan-name",
      "title": "Plan Title",
      "status": "in-progress",
      "progress": 45,
      "modules": ["module1"],
      "implements": ["path/to/doc.md"],
      "health": {
        "is_stale": false,
        "is_orphan": false,
        "is_blocked": false,
        "issues": []
      }
    }
  ],
  "health": {
    "stale_count": 2,
    "orphan_count": 1,
    "blocked_count": 2,
    "issues": []
  },
  "recommendations": []
}
```

### Step 8: Generate Recommendations

Based on health analysis, generate actionable next steps:

**Stale plans:**

```text
Update stale plans: {plan1}, {plan2}
```

**Orphaned plans:**

```text
Link orphaned plan to design doc or archive: {plan}
```

**Blocked plans:**

```text
Review blocked plans for unblocking: {plan1}
```

**Overdue plans:**

```text
Reschedule or accelerate overdue plan: {plan}
```

**Misaligned progress:**

```text
Fix status-progress alignment for: {plan}
```

**Priority order:**

1. Overdue plans (high priority)
2. Blocked plans with stale blockers
3. Stale plans
4. Orphaned plans
5. Progress misalignments

## Performance Optimization

### Caching Strategy

**Metadata cache:**

```bash
CACHE_DIR="/tmp/plan-explore-cache-$(whoami)"
CACHE_TTL=300  # 5 minutes

get_cached_metadata() {
  local file=$1
  local cache_key=$(echo "$file" | md5)
  local cache_file="$CACHE_DIR/$cache_key"

  # Check if cache exists and is fresh
  if [[ -f "$cache_file" ]]; then
    local cache_age=$(( $(date +%s) - $(stat -f%m "$cache_file") ))
    if (( cache_age < CACHE_TTL )); then
      cat "$cache_file"
      return 0
    fi
  fi

  # Parse and cache
  local metadata=$(extract_frontmatter "$file")
  echo "$metadata" > "$cache_file"
  echo "$metadata"
}
```

### Lazy Loading

**Summary mode:**

- Load only frontmatter (no body parsing)
- Skip phase details unless `--show-phases`
- Minimal health checks

**Detailed mode:**

- Full frontmatter parsing
- Phase details
- Comprehensive health analysis

### Early Exit

**Filter early:**

- Apply filters during iteration, skip parsing if not needed
- Exit early if --orphans and implements is non-empty
- Exit early if --stale and updated is recent

## Error Handling

**Plan file not found:**

```text
No plans found in {directory}

Suggestion: Create a plan with /plan-create
```

**Invalid filter values:**

```text
Invalid status: {value}
Valid values: ready, in-progress, blocked, completed, abandoned
```

**Module not found:**

```text
Module '{module}' not found in design.config.json

Available modules:
  - effect-type-registry
  - rspress-plugin-api-extractor
  - design-doc-system
```

**No plans match filters:**

```text
No plans found matching filters:
  Module: {module}
  Status: {status}

Try:
  - Remove some filters
  - Check module name spelling
  - Use /plan-list to see all plans
```
