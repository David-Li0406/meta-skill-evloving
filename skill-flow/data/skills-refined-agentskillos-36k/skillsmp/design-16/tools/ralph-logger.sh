#!/bin/bash
# ralph-logger.sh - Execution journal for Ralph methodology
#
# Creates and maintains a structured log of:
# - Step execution status (pass/fail/retry)
# - PRP lineage (which requirement each step implements)
# - File changes (created/modified/deleted)
# - Playwright verification results
# - Learnings and insights captured during execution
#
# LEARNING FLOW:
#   1. Learnings captured during execution → ralph-learnings.md (pending)
#   2. Human reviews with `review-learnings` → Accept/Edit/Reject
#   3. Accepted learnings marked as reviewed
#   4. Valuable learnings promoted to invariants with `promote-learning`
#
# Usage:
#   ./ralph-logger.sh init <prp-file> <steps-dir>
#   ./ralph-logger.sh step-start <step-num>
#   ./ralph-logger.sh step-end <step-num> <status> [--learning "text"]
#   ./ralph-logger.sh playwright <step-num> <route> <pass/fail> <checks-passed> <checks-total>
#   ./ralph-logger.sh file-change <step-num> <action> <file-path>
#   ./ralph-logger.sh phase-summary <phase-num>
#   ./ralph-logger.sh report
#   ./ralph-logger.sh review-learnings          # Human gate for learnings
#   ./ralph-logger.sh promote-learning <id>     # Promote to invariant

set -e

VERSION="1.0.0"

# Default log location
LOG_DIR="${RALPH_LOG_DIR:-.}"
LOG_FILE="$LOG_DIR/ralph-execution.json"
LEARNINGS_FILE="$LOG_DIR/ralph-learnings.md"

# ============================================================================
# JSON helpers
# ============================================================================

ensure_log_exists() {
    if [[ ! -f "$LOG_FILE" ]]; then
        cat > "$LOG_FILE" << 'EOF'
{
  "version": "1.0.0",
  "prp": null,
  "started_at": null,
  "steps": {},
  "phases": {},
  "summary": {
    "total_steps": 0,
    "passed": 0,
    "failed": 0,
    "retries": 0,
    "files_created": 0,
    "files_modified": 0,
    "learnings_count": 0
  }
}
EOF
    fi
}

update_json() {
    local tmp=$(mktemp)
    python3 -c "
import json
import sys

with open('$LOG_FILE', 'r') as f:
    data = json.load(f)

# Execute the update
exec(sys.stdin.read())

with open('$tmp', 'w') as f:
    json.dump(data, f, indent=2)
" << EOF
$1
EOF
    mv "$tmp" "$LOG_FILE"
}

# ============================================================================
# Commands
# ============================================================================

cmd_init() {
    local prp_file="$1"
    local steps_dir="$2"

    [[ -z "$prp_file" ]] && { echo "Usage: $0 init <prp-file> <steps-dir>"; exit 1; }

    ensure_log_exists

    # Extract PRP metadata
    local prp_id=$(grep -m1 "PRP ID:" "$prp_file" 2>/dev/null | sed 's/.*PRP ID:\s*//' | tr -d '*' || echo "unknown")
    local prp_name=$(head -1 "$prp_file" | sed 's/^#\s*//')

    # Count steps
    local step_count=$(ls "$steps_dir"/step-*.sh 2>/dev/null | wc -l | tr -d ' ')

    update_json "
from datetime import datetime
data['prp'] = {
    'id': '$prp_id'.strip(),
    'name': '$prp_name'.strip(),
    'file': '$prp_file'
}
data['started_at'] = datetime.now().isoformat()
data['summary']['total_steps'] = $step_count
"

    # Initialize learnings file
    cat > "$LEARNINGS_FILE" << EOF
# Ralph Execution Learnings

**PRP:** $prp_name
**Started:** $(date '+%Y-%m-%d %H:%M')

---

## Learnings by Step

EOF

    echo "✓ Initialized Ralph execution log"
    echo "  PRP: $prp_name"
    echo "  Steps: $step_count"
    echo "  Log: $LOG_FILE"
}

cmd_step_start() {
    local step_num="$1"

    ensure_log_exists

    # Get step description from script
    local step_file="$LOG_DIR/ralph-steps-v3/step-${step_num}.sh"
    local description=""
    if [[ -f "$step_file" ]]; then
        description=$(grep -m1 "^# Step" "$step_file" | sed 's/^# Step [0-9]*: //' || echo "")
    fi

    # Get PRP lineage from script comments
    local prp_ref=$(grep -m1 "^# PRP:" "$step_file" 2>/dev/null | sed 's/^# PRP:\s*//' || echo "")

    update_json "
from datetime import datetime
data['steps']['$step_num'] = {
    'number': $step_num,
    'description': '''$description''',
    'prp_lineage': '''$prp_ref''',
    'started_at': datetime.now().isoformat(),
    'ended_at': None,
    'status': 'in_progress',
    'attempts': 1,
    'file_changes': [],
    'playwright': None,
    'learnings': []
}
"

    echo "═══════════════════════════════════════════════════════"
    echo "  STEP $step_num: $description"
    echo "  PRP: $prp_ref"
    echo "═══════════════════════════════════════════════════════"
}

cmd_step_end() {
    local step_num="$1"
    local status="$2"
    shift 2

    local learning=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --learning) learning="$2"; shift 2 ;;
            --retry)
                update_json "data['steps']['$step_num']['attempts'] += 1; data['summary']['retries'] += 1"
                shift ;;
            *) shift ;;
        esac
    done

    update_json "
from datetime import datetime
data['steps']['$step_num']['ended_at'] = datetime.now().isoformat()
data['steps']['$step_num']['status'] = '$status'
if '$status' == 'pass':
    data['summary']['passed'] += 1
elif '$status' == 'fail':
    data['summary']['failed'] += 1
if '''$learning''':
    data['steps']['$step_num']['learnings'].append('''$learning''')
    data['summary']['learnings_count'] += 1
"

    # Append to learnings file
    if [[ -n "$learning" ]]; then
        echo "" >> "$LEARNINGS_FILE"
        echo "### Step $step_num" >> "$LEARNINGS_FILE"
        echo "- $learning" >> "$LEARNINGS_FILE"
    fi

    if [[ "$status" == "pass" ]]; then
        echo "✓ Step $step_num PASSED"
    else
        echo "✗ Step $step_num FAILED"
    fi
}

cmd_file_change() {
    local step_num="$1"
    local action="$2"  # created, modified, deleted
    local file_path="$3"

    ensure_log_exists

    update_json "
data['steps']['$step_num']['file_changes'].append({
    'action': '$action',
    'file': '$file_path'
})
if '$action' == 'created':
    data['summary']['files_created'] += 1
elif '$action' == 'modified':
    data['summary']['files_modified'] += 1
"
}

cmd_playwright() {
    local step_num="$1"
    local route="$2"
    local status="$3"
    local passed="$4"
    local total="$5"

    ensure_log_exists

    update_json "
data['steps']['$step_num']['playwright'] = {
    'route': '$route',
    'status': '$status',
    'checks_passed': $passed,
    'checks_total': $total
}
"

    echo "  Playwright $route: $passed/$total checks ($status)"
}

cmd_phase_summary() {
    local phase_num="$1"

    ensure_log_exists

    # Calculate phase stats from steps
    python3 << EOF
import json

with open('$LOG_FILE', 'r') as f:
    data = json.load(f)

# Define phase boundaries (customize per project)
phase_ranges = {
    '1': (1, 8),
    '2': (9, 14),
    '3': (15, 24),
    '4': (25, 30),
    '5': (31, 33)
}

phase = '$phase_num'
if phase not in phase_ranges:
    print(f"Unknown phase: {phase}")
    exit(1)

start, end = phase_ranges[phase]
phase_steps = {k: v for k, v in data['steps'].items() if start <= int(k) <= end}

passed = sum(1 for s in phase_steps.values() if s.get('status') == 'pass')
failed = sum(1 for s in phase_steps.values() if s.get('status') == 'fail')
total = len(phase_steps)
files_created = sum(len([c for c in s.get('file_changes', []) if c['action'] == 'created']) for s in phase_steps.values())
files_modified = sum(len([c for c in s.get('file_changes', []) if c['action'] == 'modified']) for s in phase_steps.values())
learnings = [l for s in phase_steps.values() for l in s.get('learnings', [])]

print(f"""
═══════════════════════════════════════════════════════
  PHASE {phase} SUMMARY
═══════════════════════════════════════════════════════

Steps: {start}-{end} ({total} total)
Status: {passed} passed, {failed} failed
Files: {files_created} created, {files_modified} modified

Learnings ({len(learnings)}):""")

for i, l in enumerate(learnings[:5], 1):
    print(f"  {i}. {l}")

if len(learnings) > 5:
    print(f"  ... and {len(learnings) - 5} more")

print("═══════════════════════════════════════════════════════")
EOF
}

cmd_report() {
    ensure_log_exists

    python3 << 'EOF'
import json
from datetime import datetime

with open('$LOG_FILE'.replace('$LOG_FILE', '') or 'ralph-execution.json', 'r') as f:
    data = json.load(f)

print("""
╔═══════════════════════════════════════════════════════════════╗
║  RALPH EXECUTION REPORT                                       ║
╚═══════════════════════════════════════════════════════════════╝
""")

if data.get('prp'):
    print(f"PRP: {data['prp'].get('name', 'Unknown')}")
    print(f"ID:  {data['prp'].get('id', 'Unknown')}")

print(f"""
Started: {data.get('started_at', 'Unknown')}

───────────────────────────────────────────────────────────────
SUMMARY
───────────────────────────────────────────────────────────────
Total Steps:    {data['summary']['total_steps']}
Passed:         {data['summary']['passed']}
Failed:         {data['summary']['failed']}
Retries:        {data['summary']['retries']}
Files Created:  {data['summary']['files_created']}
Files Modified: {data['summary']['files_modified']}
Learnings:      {data['summary']['learnings_count']}

───────────────────────────────────────────────────────────────
STEP DETAILS
───────────────────────────────────────────────────────────────""")

for step_num in sorted(data['steps'].keys(), key=int):
    step = data['steps'][step_num]
    status_icon = "✓" if step['status'] == 'pass' else "✗" if step['status'] == 'fail' else "○"
    playwright = ""
    if step.get('playwright'):
        pw = step['playwright']
        playwright = f" | Playwright {pw['route']}: {pw['checks_passed']}/{pw['checks_total']}"

    print(f"{status_icon} Step {step_num}: {step.get('description', '')[:40]}")
    print(f"  PRP: {step.get('prp_lineage', 'N/A')}")
    print(f"  Attempts: {step.get('attempts', 1)}{playwright}")

    if step.get('file_changes'):
        created = [c['file'] for c in step['file_changes'] if c['action'] == 'created']
        if created:
            print(f"  Created: {', '.join(c.split('/')[-1] for c in created[:3])}")

    if step.get('learnings'):
        for l in step['learnings'][:2]:
            print(f"  💡 {l[:60]}...")
    print()

print("───────────────────────────────────────────────────────────────")
EOF
}

# ============================================================================
# LEARNING REVIEW & PROMOTION (Human Gate)
# ============================================================================

INVARIANTS_FILE="${DESIGNOPS_ROOT:-$HOME/.claude/plugins/design-ops}/invariants/learned-invariants.md"

cmd_review_learnings() {
    ensure_log_exists

    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  LEARNING REVIEW (Human Gate)                                 ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""

    # Extract all learnings with their step context
    python3 << 'PYEOF'
import json

with open('ralph-execution.json', 'r') as f:
    data = json.load(f)

learnings = []
for step_num, step in data.get('steps', {}).items():
    for learning in step.get('learnings', []):
        learnings.append({
            'id': f"L{step_num}-{len(learnings)+1}",
            'step': step_num,
            'prp': step.get('prp_lineage', 'N/A'),
            'text': learning,
            'status': 'pending'
        })

if not learnings:
    print("No learnings to review.")
else:
    print(f"Found {len(learnings)} learning(s) to review:\n")
    for i, l in enumerate(learnings, 1):
        print(f"[{l['id']}] Step {l['step']} ({l['prp']})")
        print(f"    {l['text']}")
        print()

print("""
───────────────────────────────────────────────────────────────
REVIEW OPTIONS
───────────────────────────────────────────────────────────────
For each learning, decide:

  [A] Accept    - Keep as project learning
  [E] Edit      - Modify before accepting
  [R] Reject    - Not valuable, discard
  [P] Promote   - Elevate to invariant (guides future projects)

To promote a learning to invariant:
  ./ralph-logger.sh promote-learning L15-1

Invariants become reusable rules that prevent repeat mistakes.
───────────────────────────────────────────────────────────────
""")
PYEOF
}

cmd_promote_learning() {
    local learning_id="$1"

    [[ -z "$learning_id" ]] && { echo "Usage: $0 promote-learning <learning-id>"; exit 1; }

    # Create invariants directory if needed
    mkdir -p "$(dirname "$INVARIANTS_FILE")"

    # Initialize invariants file if needed
    if [[ ! -f "$INVARIANTS_FILE" ]]; then
        cat > "$INVARIANTS_FILE" << 'EOF'
# Learned Invariants

Invariants extracted from project learnings. These guide future projects.

## Format

Each invariant has:
- **ID**: Unique identifier (e.g., INV-001)
- **Source**: Which project/step it came from
- **Rule**: The invariant statement
- **Context**: When this applies
- **Example**: Concrete example

---

## Invariants

EOF
    fi

    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  PROMOTE LEARNING TO INVARIANT                                ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""

    # Extract the learning
    python3 << PYEOF
import json
import sys

with open('ralph-execution.json', 'r') as f:
    data = json.load(f)

learning_id = '$learning_id'
step_num = learning_id.split('-')[0].replace('L', '')

step = data.get('steps', {}).get(step_num)
if not step:
    print(f"Step {step_num} not found")
    sys.exit(1)

learnings = step.get('learnings', [])
if not learnings:
    print(f"No learnings in step {step_num}")
    sys.exit(1)

# Get the learning index from the ID
idx = int(learning_id.split('-')[1]) - 1 if '-' in learning_id else 0
if idx >= len(learnings):
    print(f"Learning index {idx+1} not found in step {step_num}")
    sys.exit(1)

learning = learnings[idx]
prp = step.get('prp_lineage', 'Unknown')
prp_name = data.get('prp', {}).get('name', 'Unknown')

print(f"Learning: {learning}")
print(f"Source: Step {step_num} - {prp}")
print(f"Project: {prp_name}")
print()
print("Converting to invariant format...")
print()

# Count existing invariants to generate new ID
import os
invariants_file = '$INVARIANTS_FILE'
inv_count = 0
if os.path.exists(invariants_file):
    with open(invariants_file, 'r') as f:
        inv_count = f.read().count('### INV-')

new_id = f"INV-{inv_count + 1:03d}"

# Write the invariant
invariant_entry = f'''
### {new_id}

**Source:** {prp_name} / Step {step_num} ({prp})
**Date:** $(date '+%Y-%m-%d')

**Rule:** {learning}

**Context:** [Add when this invariant applies]

**Example:** [Add concrete example]

**Validation:** [How to check this invariant is met]

---
'''

with open(invariants_file, 'a') as f:
    f.write(invariant_entry)

print(f"✓ Created invariant {new_id}")
print(f"  File: {invariants_file}")
print()
print("Next steps:")
print("  1. Edit the invariant to add Context, Example, Validation")
print("  2. Reference in future PRPs: 'Must satisfy INV-{inv_count + 1:03d}'")
PYEOF
}

# ============================================================================
# Main
# ============================================================================

case "${1:-}" in
    init) shift; cmd_init "$@" ;;
    step-start) shift; cmd_step_start "$@" ;;
    step-end) shift; cmd_step_end "$@" ;;
    file-change) shift; cmd_file_change "$@" ;;
    playwright) shift; cmd_playwright "$@" ;;
    phase-summary) shift; cmd_phase_summary "$@" ;;
    report) cmd_report ;;
    review-learnings) cmd_review_learnings ;;
    promote-learning) shift; cmd_promote_learning "$@" ;;
    *)
        echo "Ralph Logger v$VERSION"
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  init <prp> <steps-dir>     Initialize log for a PRP"
        echo "  step-start <N>             Log step N starting"
        echo "  step-end <N> <status>      Log step N result (pass/fail)"
        echo "  file-change <N> <action> <file>  Log file change"
        echo "  playwright <N> <route> <status> <passed> <total>"
        echo "  phase-summary <N>          Show phase N summary"
        echo "  report                     Full execution report"
        echo ""
        echo "Learning Review (Human Gate):"
        echo "  review-learnings           Review pending learnings"
        echo "  promote-learning <id>      Promote learning to invariant"
        exit 1
        ;;
esac
