---
name: health-dashboard
description: "Interactive Health OS dashboard using AskUserQuestion for profile selection, state initialization, and action menus. Invoke with /health-dashboard or at session start."
invocable: true
---

# Health Dashboard

Interactive entry point for Health OS that guides users through profile selection, state checking, and presents an actionable dashboard with next steps.

## When to Use This Skill

**Automatic triggers**:
- Session start (user initiates conversation)
- User types `/health-dashboard`
- User asks "show my health dashboard" or "health status"

**Manual invocation**:
```
/health-dashboard
```

## Health State System Overview

The health state system transforms health-agent from a reactive analysis tool into a proactive Health OS with persistent understanding across sessions.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 INTERACTIVE DASHBOARD                        │
│  /health-dashboard or session start                          │
│                                                              │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │ AskUserQuestion │───▶│ Profile Select  │                 │
│  └─────────────────┘    └────────┬────────┘                 │
│                                  ▼                           │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │ AskUserQuestion │───▶│ State Init?     │                 │
│  └─────────────────┘    └────────┬────────┘                 │
│                                  ▼                           │
│  ┌────────────────────────────────────────┐                 │
│  │        VISUAL DASHBOARD                 │                 │
│  │  • Conditions & confidence             │                 │
│  │  • Top actions (prioritized)           │                 │
│  │  • Medications / Supplements           │                 │
│  │  • Goals & progress                    │                 │
│  │  • Recent activity                     │                 │
│  └────────────────────┬───────────────────┘                 │
│                       ▼                                      │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │ AskUserQuestion │───▶│ Action Menu     │                 │
│  └─────────────────┘    │ • Review data   │                 │
│                         │ • Investigate   │                 │
│                         │ • Track labs    │                 │
│                         │ • Provider visit│                 │
│                         └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   .state/{profile}/           │
              │   health-state.yaml           │
              │                               │
              │   • Conditions & hypotheses   │
              │   • Biomarker baselines       │
              │   • Active actions            │
              │   • Intervention outcomes     │
              │   • Last sync timestamps      │
              └───────────────────────────────┘
```

### State File Location

State files are stored at `.state/{profile}/health-state.yaml`. The template at `.state/_template/health-state.yaml` documents the structure.

- **Schema Validation**: JSON Schema at `.state/_template/health-state.schema.json`
- **Atomic Updates**: Always use atomic write pattern (backup → temp → validate → rename)
- **Profile Caching**: Last selected profile cached at `.state/.last-profile`

### Key State Components

| Component | Purpose |
|-----------|---------|
| `conditions` | Active health conditions with hypotheses and confidence |
| `biomarker_baselines` | Personal "normal" values vs population reference |
| `genetics` | Key genetic findings cached from investigations |
| `medications` / `supplements` | Current medications with monitoring markers |
| `actions` | Prioritized next steps (recommended/accepted/in_progress) |
| `completed_actions` | What was tried and outcomes (keeps last 20) |
| `declined_actions` | Actions user declined (don't re-recommend) |
| `goals` | Health goals with progress tracking |
| `last_sync` | Timestamps of last processed data from each source |

### Relationship to current.yaml (health-log-parser output)

**These are complementary, not redundant:**

| Aspect | current.yaml (health-log) | health-state.yaml (agent state) |
|--------|---------------------------|--------------------------------|
| **Purpose** | User-maintained current state | Agent-synthesized understanding |
| **Content** | "What I'm taking/have" | "What it means + what to do" |
| **Maintained by** | User (via health-log-parser) | Agent |
| **Update pattern** | Direct edits | Revise based on analysis |
| **Time scope** | Current snapshot | Current snapshot + actions |

**Key distinction**:
- `{health_log_path}/current.yaml` = User's source of truth (conditions, medications, supplements)
- `.state/{profile}/health-state.yaml` = Agent's analysis layer (hypotheses, actions, confidence scores)

Data flows one direction:
```
current.yaml    ─┐
history.csv     ─┤
labs/all.csv    ─┼──→ Agent reasoning ──→ health-state.yaml
exams/*.md      ─┤
genetics        ─┘
```

### State Maintenance Behavior

The agent should **proactively offer** to update state, not wait for explicit requests:

- After discussion implies state change → "Should I update your health state to reflect [X]?"
- User says "I did X" → Offer to record it
- Investigation completes → "I'll add these actions to your health state"

**When to Update State**:

| Trigger | State Update |
|---------|--------------|
| Investigation completes | Add/update condition, generate actions |
| User reports completing action | Move to completed_actions with outcome |
| New lab results discussed | Update biomarker_baselines if significant |
| User starts/stops medication | Update medications/supplements |
| Goal progress changes | Update goals.progress |
| User declines an action | Add to declined_actions |

### Action Lifecycle

```
recommended → accepted → in_progress → completed
      │                                    │
      ▼                                    ▼
  declined                          outcome recorded
      │                                    │
      ▼                                    ▼
(don't re-recommend               confidence updated
 unless reconsider_if met)        new actions generated
```

### Biomarker Baselines

Personal baselines differ from population references when:
- Chronic condition causes stable deviation (e.g., elevated bilirubin in hemolysis)
- User has consistently different "normal" (e.g., naturally low BP)

Update baselines when pattern established over 3+ measurements or investigation confirms cause.

### State File Maintenance

Keep state file manageable:
- **completed_actions**: Keep last 20 entries
- **Archive annually**: Move completed_actions older than 1 year to `.state/{profile}/archive/`
- **Prune declined_actions**: Remove if `reconsider_if` conditions met, or after 2 years

## Workflow

### Phase 1: Profile Selection

Use AskUserQuestion to let the user select their profile:

```
First, list available profiles:
ls profiles/*.yaml (exclude _template.yaml)

Then use AskUserQuestion:
{
  "questions": [{
    "question": "Which health profile would you like to use?",
    "header": "Profile",
    "options": [
      // Dynamically populate from profiles/*.yaml
      {"label": "{profile_name}", "description": "Load {profile_name}'s health data"}
    ],
    "multiSelect": false
  }]
}
```

After selection, read the profile YAML and extract data source paths.

### Phase 2: State Check

Check if health state exists:

```bash
PROFILE="{selected_profile}"
test -f ".state/${PROFILE}/health-state.yaml" && echo "EXISTS" || echo "MISSING"
```

**If state MISSING**, use AskUserQuestion:
```json
{
  "questions": [{
    "question": "Your health state hasn't been initialized yet. Would you like to set it up now?",
    "header": "Setup",
    "options": [
      {"label": "Yes, initialize (Recommended)", "description": "Create health state from existing data (conditions, medications, actions)"},
      {"label": "Skip for now", "description": "Proceed without persistent state tracking"}
    ],
    "multiSelect": false
  }]
}
```

If user selects "Yes, initialize":
1. Run State Initialization Bootstrap (see CLAUDE.md "State Initialization" section)
2. Continue to Phase 3

If user selects "Skip":
1. Continue to Phase 3 without state features

### Phase 3: Data Freshness Check

If state exists, check for new data:

```bash
# Get last modified times
LABS_MOD=$(stat -f "%Sm" -t "%Y-%m-%d" "{labs_path}/all.csv" 2>/dev/null || echo "N/A")
CURRENT_MOD=$(stat -f "%Sm" -t "%Y-%m-%d" "{health_log_path}/current.yaml" 2>/dev/null || echo "N/A")
HISTORY_MOD=$(stat -f "%Sm" -t "%Y-%m-%d" "{health_log_path}/history.csv" 2>/dev/null || echo "N/A")

# Read last_sync from state
grep -A3 "last_sync:" ".state/${PROFILE}/health-state.yaml"
```

Compare timestamps. If new data detected, flag for dashboard display.

### Phase 4: Render Dashboard

Present a formatted dashboard to the user. Use this template:

```
┌─────────────────────────────────────────────────────────────┐
│                    HEALTH DASHBOARD                         │
│                    {Profile Name}                           │
│                    {Date}                                   │
└─────────────────────────────────────────────────────────────┘

{If new data detected}
📊 NEW DATA AVAILABLE
   • Labs updated: {labs_mod_date}
   • Health log updated: {log_mod_date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIVE CONDITIONS                                    CONFIDENCE
──────────────────────────────────────────────────────────────
{condition_1}                                        {XX%}
  └─ Primary: {hypothesis}
{condition_2}                                        {XX%}
  └─ Primary: {hypothesis}
{If no conditions: "No active conditions tracked"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP ACTIONS                                          PRIORITY
──────────────────────────────────────────────────────────────
{If actions exist}
1. {action_1}                                        {HIGH/MED/LOW}
   Status: {recommended/accepted/in_progress}
   {If due date: "Due: {date}"}
2. {action_2}                                        {priority}
3. {action_3}                                        {priority}

{If no actions: "No pending actions"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURRENT MEDICATIONS                 SUPPLEMENTS
─────────────────────────          ─────────────────────────
{med_1} ({dose})                   {supp_1} ({dose})
{med_2} ({dose})                   {supp_2} ({dose})
{If none: "None tracked"}          {If none: "None tracked"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GOALS                                                PROGRESS
──────────────────────────────────────────────────────────────
{goal_1}                                             {XX%}
{goal_2}                                             {XX%}
{If no goals: "No active goals"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECENT ACTIVITY (Last 7 days)
──────────────────────────────────────────────────────────────
{date}: {brief_event_summary}
{date}: {brief_event_summary}
{If none: "No recent activity logged"}
```

### Phase 5: Interactive Menu

After displaying dashboard, use AskUserQuestion to offer next actions:

```json
{
  "questions": [{
    "question": "What would you like to do?",
    "header": "Action",
    "options": [
      {"label": "Review new data", "description": "Analyze recent labs and health events"},
      {"label": "Investigate condition", "description": "Run root cause investigation on a condition"},
      {"label": "Check lab trends", "description": "Track specific biomarker over time"},
      {"label": "Prepare provider visit", "description": "Generate documentation for doctor appointment"}
    ],
    "multiSelect": false
  }]
}
```

**Option handlers**:

**"Review new data"**:
- Show new lab values with reference ranges
- Highlight out-of-range values
- Summarize new health log entries
- Ask: "Any of these need further investigation?"

**"Investigate condition"**:
- If conditions exist, ask which to investigate
- If no conditions, ask what symptom/concern to investigate
- Then invoke `investigate-root-cause` skill

**"Check lab trends"**:
- Ask which marker to track (common options + Other)
- Query and display trend data
- Calculate direction (improving/stable/worsening)

**"Prepare provider visit"**:
- Invoke `prepare-provider-visit` skill

After each action completes, loop back to Phase 5 (show menu again) unless user indicates they're done.

### Phase 6: Continuous Interaction

After each action, offer follow-up:

```json
{
  "questions": [{
    "question": "What's next?",
    "header": "Continue",
    "options": [
      {"label": "Back to dashboard", "description": "Return to main dashboard view"},
      {"label": "Another action", "description": "Choose a different action"},
      {"label": "I'm done", "description": "End this session"}
    ],
    "multiSelect": false
  }]
}
```

## Dashboard Data Extraction

### Extract Conditions from State

```bash
# If state exists
grep -A20 "^conditions:" ".state/${PROFILE}/health-state.yaml" | \
  grep -E "^\s+-\s+name:|confidence:|primary_hypothesis:"
```

### Extract Actions from State

```bash
grep -A30 "^actions:" ".state/${PROFILE}/health-state.yaml" | \
  grep -E "^\s+-\s+id:|action:|priority:|status:|due:"
```

### Extract Medications/Supplements

```bash
grep -A20 "^medications:" ".state/${PROFILE}/health-state.yaml"
grep -A20 "^supplements:" ".state/${PROFILE}/health-state.yaml"
```

### Extract Goals

```bash
grep -A15 "^goals:" ".state/${PROFILE}/health-state.yaml"
```

### Recent Activity (from history.csv)

```bash
# Last 7 days from history.csv
awk -F',' -v start="$(date -v-7d +%Y-%m-%d)" \
  'NR==1 || $1 >= start' "{health_log_path}/history.csv" | \
  tail -10
```

## State Update Triggers

During dashboard interactions, proactively offer state updates:

| User Action | Offer to Update |
|-------------|-----------------|
| Marks action complete | Move to completed_actions |
| Reports taking new medication | Add to medications |
| Mentions stopping supplement | Update supplement status |
| Discusses new symptom | Offer to add to health_log |
| Completes investigation | Update conditions, add actions |

Use pattern:
```json
{
  "questions": [{
    "question": "Should I update your health state to reflect this change?",
    "header": "Update",
    "options": [
      {"label": "Yes, update it", "description": "Add this to your persistent health state"},
      {"label": "No, skip", "description": "Don't record this change"}
    ],
    "multiSelect": false
  }]
}
```

## Profile Caching

To improve UX, the dashboard caches the last selected profile:

### Check for cached profile

```bash
LAST_PROFILE=""
if [ -f ".state/.last-profile" ]; then
    LAST_PROFILE=$(cat .state/.last-profile)
fi
```

### Phase 1 with caching

If a cached profile exists, offer it as the first option:

```json
{
  "questions": [{
    "question": "Which health profile would you like to use?",
    "header": "Profile",
    "options": [
      {"label": "{last_profile} (Recommended)", "description": "Continue with your last session's profile"},
      // Other profiles...
    ],
    "multiSelect": false
  }]
}
```

### Save selected profile

After profile selection:

```bash
mkdir -p .state
echo "{selected_profile}" > .state/.last-profile
```

## Atomic State Updates

When writing to health-state.yaml, use atomic operations to prevent corruption:

### Safe State Write Pattern

```bash
PROFILE="{selected_profile}"
STATE_FILE=".state/${PROFILE}/health-state.yaml"
BACKUP_FILE=".state/${PROFILE}/health-state.yaml.bak"
TEMP_FILE=".state/${PROFILE}/health-state.yaml.tmp"

# 1. Create backup of existing state
if [ -f "$STATE_FILE" ]; then
    cp "$STATE_FILE" "$BACKUP_FILE"
fi

# 2. Write to temp file first (use Write tool)
# Write tool writes to $TEMP_FILE

# 3. Validate the new file (basic YAML check)
if python3 -c "import yaml; yaml.safe_load(open('$TEMP_FILE'))" 2>/dev/null; then
    # 4. Atomic move (rename is atomic on most filesystems)
    mv "$TEMP_FILE" "$STATE_FILE"
    echo "State updated successfully"
else
    echo "ERROR: Invalid YAML in new state file"
    rm -f "$TEMP_FILE"
    # State file unchanged, backup still available
fi
```

### Rollback on Error

If state update fails mid-session:

```bash
if [ -f "$BACKUP_FILE" ]; then
    cp "$BACKUP_FILE" "$STATE_FILE"
    echo "Rolled back to previous state"
fi
```

## Data Source Validation

Before loading data, validate all paths exist:

```bash
# Source the helper functions
source .claude/skills/health-agent/references/data-access-helpers.sh

# Validate paths (will print warnings for missing sources)
if ! validate_data_sources "$labs_path" "$health_log_path" "$exams_path"; then
    echo "WARNING: Some data sources are missing"
fi
```

## Error Handling

**Profile not found**:
- List available profiles
- Offer to create new profile (link to _template.yaml)

**State file corrupted**:
- Offer to re-initialize from scratch
- Backup corrupted file first (to `.state/{profile}/health-state.corrupted.{timestamp}`)
- Validate new state with schema before saving

**Data sources missing**:
- Show which sources are unavailable
- Proceed with available data
- Note limitations in dashboard

---

## Detailed State File Corruption Handling

### Detection: When to Suspect Corruption

Check for corruption in these scenarios:

1. **Parse failure**: YAML parser throws error
2. **Schema violation**: Required fields missing or wrong type
3. **Inconsistent state**: References to non-existent IDs
4. **Truncation**: File size < 100 bytes or ends mid-line

### Pre-Use Validation Workflow

Before loading state file, always validate:

```bash
PROFILE="{selected_profile}"
STATE_FILE=".state/${PROFILE}/health-state.yaml"
SCHEMA_FILE=".state/_template/health-state.schema.json"

validate_state_file() {
    local state_file="$1"

    # Check 1: File exists and is readable
    if [ ! -f "$state_file" ]; then
        echo "STATE_MISSING"
        return 1
    fi

    if [ ! -r "$state_file" ]; then
        echo "STATE_UNREADABLE"
        return 2
    fi

    # Check 2: File size sanity (corrupt files often empty or tiny)
    local size=$(wc -c < "$state_file" 2>/dev/null | tr -d ' ')
    if [ -z "$size" ] || [ "$size" -lt 50 ]; then
        echo "STATE_TOO_SMALL:$size"
        return 3
    fi

    # Check 3: YAML syntax validation
    if ! python3 -c "import yaml; yaml.safe_load(open('$state_file'))" 2>/dev/null; then
        echo "STATE_INVALID_YAML"
        return 4
    fi

    # Check 4: Required fields present
    local required_check=$(python3 -c "
import yaml
with open('$state_file') as f:
    data = yaml.safe_load(f)

required = ['profile_name', 'last_updated']
missing = [r for r in required if r not in data]
if missing:
    print('MISSING:' + ','.join(missing))
else:
    print('OK')
" 2>/dev/null)

    if [ "${required_check:0:7}" = "MISSING" ]; then
        echo "STATE_MISSING_FIELDS:${required_check#MISSING:}"
        return 5
    fi

    # Check 5: JSON Schema validation (if schema exists)
    if [ -f "$SCHEMA_FILE" ]; then
        if command -v jsonschema >/dev/null 2>&1; then
            # Convert YAML to JSON and validate
            if ! python3 -c "
import yaml, json, sys
from jsonschema import validate, ValidationError
with open('$state_file') as f:
    data = yaml.safe_load(f)
with open('$SCHEMA_FILE') as f:
    schema = json.load(f)
try:
    validate(data, schema)
    print('SCHEMA_OK')
except ValidationError as e:
    print('SCHEMA_ERROR:' + str(e.message)[:100])
" 2>/dev/null | grep -q "SCHEMA_OK"; then
                echo "STATE_SCHEMA_VIOLATION"
                return 6
            fi
        fi
    fi

    echo "STATE_VALID"
    return 0
}

# Run validation
validation_result=$(validate_state_file "$STATE_FILE")
validation_code=$?

case $validation_code in
    0) echo "State file valid, proceeding..." ;;
    1) echo "State file not found - offer initialization" ;;
    2) echo "State file permission error" ;;
    3|4|5|6)
        echo "State file corrupted: $validation_result"
        echo "Initiating recovery..."
        # Proceed to recovery workflow
        ;;
esac
```

### Backup Procedure

Before any recovery attempt, create a timestamped backup:

```bash
create_corruption_backup() {
    local state_file="$1"
    local profile="$2"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir=".state/${profile}/backups"
    local backup_file="${backup_dir}/health-state.corrupted.${timestamp}"

    # Create backup directory
    mkdir -p "$backup_dir"

    # Copy corrupted file
    if [ -f "$state_file" ]; then
        cp "$state_file" "$backup_file"
        echo "Corrupted state backed up to: $backup_file"

        # Keep only last 10 corruption backups
        ls -t "${backup_dir}/health-state.corrupted."* 2>/dev/null | \
            tail -n +11 | xargs rm -f 2>/dev/null

        return 0
    else
        echo "No state file to backup"
        return 1
    fi
}
```

### Recovery Workflow

Present recovery options to user via AskUserQuestion:

```json
{
  "questions": [{
    "question": "Your health state file appears corrupted. How would you like to proceed?",
    "header": "Recovery",
    "options": [
      {
        "label": "Auto-repair (Recommended)",
        "description": "Attempt to recover valid portions and rebuild missing sections"
      },
      {
        "label": "Restore from backup",
        "description": "Restore from last known good backup (if available)"
      },
      {
        "label": "Re-initialize from scratch",
        "description": "Create new state file from current health data"
      },
      {
        "label": "Skip state features",
        "description": "Continue without persistent state tracking"
      }
    ],
    "multiSelect": false
  }]
}
```

### Recovery Option 1: Auto-Repair

Attempt to salvage valid portions:

```bash
auto_repair_state() {
    local corrupted_file="$1"
    local profile="$2"
    local output_file="$3"

    # Try to extract whatever we can
    python3 << 'PYTHON_SCRIPT'
import yaml
import sys
from datetime import datetime

corrupted_file = "$corrupted_file"
profile = "$profile"
output_file = "$output_file"

# Default empty state
default_state = {
    'profile_name': profile,
    'last_updated': datetime.now().isoformat(),
    'conditions': [],
    'biomarker_baselines': {},
    'genetics': {},
    'medications': [],
    'supplements': [],
    'actions': [],
    'completed_actions': [],
    'declined_actions': [],
    'goals': [],
    'last_sync': {}
}

try:
    # Try to load corrupted file
    with open(corrupted_file, 'r') as f:
        content = f.read()

    # Try standard load first
    try:
        data = yaml.safe_load(content)
        if data is None:
            data = {}
    except yaml.YAMLError:
        # Try line-by-line recovery
        data = {}
        for line in content.split('\n'):
            try:
                partial = yaml.safe_load(line)
                if isinstance(partial, dict):
                    data.update(partial)
            except:
                pass

    # Merge with defaults (keep valid data, fill gaps)
    for key, default_value in default_state.items():
        if key not in data:
            data[key] = default_value
            print(f"Restored missing field: {key}", file=sys.stderr)
        elif not isinstance(data[key], type(default_value)):
            print(f"Fixed type mismatch for: {key}", file=sys.stderr)
            data[key] = default_value

    # Update timestamp
    data['last_updated'] = datetime.now().isoformat()
    data['_repair_note'] = f"Auto-repaired on {datetime.now().isoformat()}"

    # Write repaired file
    with open(output_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    print("REPAIR_SUCCESS")

except Exception as e:
    print(f"REPAIR_FAILED:{e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
}
```

### Recovery Option 2: Restore from Backup

Find and restore the most recent valid backup:

```bash
restore_from_backup() {
    local profile="$1"
    local state_file=".state/${profile}/health-state.yaml"
    local backup_dir=".state/${profile}/backups"
    local daily_backup=".state/${profile}/health-state.yaml.bak"

    # Check daily backup first (from atomic writes)
    if [ -f "$daily_backup" ]; then
        if validate_state_file "$daily_backup" | grep -q "STATE_VALID"; then
            cp "$daily_backup" "$state_file"
            echo "Restored from daily backup"
            return 0
        fi
    fi

    # Check timestamped backups (oldest to newest for uncorrupted version)
    if [ -d "$backup_dir" ]; then
        for backup in $(ls -t "$backup_dir"/health-state.*.bak 2>/dev/null); do
            if validate_state_file "$backup" | grep -q "STATE_VALID"; then
                cp "$backup" "$state_file"
                echo "Restored from backup: $backup"
                return 0
            fi
        done
    fi

    echo "No valid backup found"
    return 1
}
```

### Recovery Option 3: Re-Initialize

Create fresh state from existing health data (same as State Initialization Bootstrap in CLAUDE.md):

```bash
# This invokes the standard initialization routine
# See CLAUDE.md "State Initialization (Bootstrap)" section
echo "Proceeding with fresh initialization..."
# The initialize_health_state function would go here
```

### Automatic Backup Schedule

To prevent future data loss, create backups during state updates:

```bash
# Before any state update, create dated backup
create_dated_backup() {
    local profile="$1"
    local state_file=".state/${profile}/health-state.yaml"
    local backup_dir=".state/${profile}/backups"
    local date_stamp=$(date +%Y%m%d)
    local backup_file="${backup_dir}/health-state.${date_stamp}.bak"

    # Only create one backup per day
    if [ ! -f "$backup_file" ]; then
        mkdir -p "$backup_dir"
        cp "$state_file" "$backup_file" 2>/dev/null
    fi

    # Cleanup: keep only last 30 daily backups
    ls -t "${backup_dir}/health-state."*.bak 2>/dev/null | \
        tail -n +31 | xargs rm -f 2>/dev/null
}
```

### Listing Available Backups

Show user what backups exist:

```bash
list_available_backups() {
    local profile="$1"
    local backup_dir=".state/${profile}/backups"

    echo "=== Available Backups ==="

    # Daily backup
    if [ -f ".state/${profile}/health-state.yaml.bak" ]; then
        local mod_date=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" ".state/${profile}/health-state.yaml.bak" 2>/dev/null)
        echo "• Daily backup: $mod_date"
    fi

    # Dated backups
    if [ -d "$backup_dir" ]; then
        for backup in $(ls -t "$backup_dir"/health-state.*.bak 2>/dev/null | head -5); do
            local date=$(basename "$backup" | grep -oE '[0-9]{8}')
            local formatted="${date:0:4}-${date:4:2}-${date:6:2}"
            echo "• $formatted: $backup"
        done
    fi

    # Corruption backups
    local corruption_count=$(ls "$backup_dir"/health-state.corrupted.* 2>/dev/null | wc -l | tr -d ' ')
    if [ "$corruption_count" -gt 0 ]; then
        echo "• Corruption archives: $corruption_count files"
    fi
}
```

## Example Session

```
User: /health-dashboard