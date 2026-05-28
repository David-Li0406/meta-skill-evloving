#!/bin/bash
# ralph-common.sh - State Machine Functions for Ralph Loop
# Part of the State-Aware RALPH Loop system

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Cross-platform sed -i
sedi() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# =============================================================================
# State File Management
# =============================================================================

# Initialize state file from template
initialize_state() {
    local workspace="$1"
    local state_file="$workspace/.ralph/state.md"
    local template_dir
    template_dir="$(dirname "${BASH_SOURCE[0]}")"
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    mkdir -p "$workspace/.ralph"
    
    if [[ -f "$template_dir/state-template.md" ]]; then
        sed "s/{{TIMESTAMP}}/$timestamp/g" "$template_dir/state-template.md" > "$state_file"
    else
        cat > "$state_file" <<EOF
# RALPH State

current_state: INIT
retry_count: 0
max_retries: 5
started_at: $timestamp
history:
  - $timestamp | INIT
EOF
    fi
    
    echo -e "${GREEN}✓ State initialized: $state_file${NC}"
}

# Read current state from .ralph/state.md
get_current_state() {
    local workspace="$1"
    local state_file="$workspace/.ralph/state.md"
    
    if [[ ! -f "$state_file" ]]; then
        echo "INIT"
        return
    fi
    
    grep "^current_state:" "$state_file" | cut -d: -f2 | tr -d ' '
}

# Get retry count for current state
get_retry_count() {
    local workspace="$1"
    local state_file="$workspace/.ralph/state.md"
    
    if [[ ! -f "$state_file" ]]; then
        echo "0"
        return
    fi
    
    grep "^retry_count:" "$state_file" | cut -d: -f2 | tr -d ' '
}

# Get max retries setting
get_max_retries() {
    local workspace="$1"
    local state_file="$workspace/.ralph/state.md"
    
    if [[ ! -f "$state_file" ]]; then
        echo "5"
        return
    fi
    
    local max
    max=$(grep "^max_retries:" "$state_file" | cut -d: -f2 | tr -d ' ')
    echo "${max:-5}"
}

# Set max retries
set_max_retries() {
    local workspace="$1"
    local max="$2"
    local state_file="$workspace/.ralph/state.md"
    
    if grep -q "^max_retries:" "$state_file"; then
        sedi "s/^max_retries:.*/max_retries: $max/" "$state_file"
    else
        # Insert after retry_count
        sedi "/^retry_count:/a\\
max_retries: $max" "$state_file"
    fi
}

# Increment retry count
increment_retry() {
    local workspace="$1"
    local state_file="$workspace/.ralph/state.md"
    local current
    current=$(get_retry_count "$workspace")
    local next=$((current + 1))
    
    sedi "s/^retry_count:.*/retry_count: $next/" "$state_file"
    echo "$next"
}

# Reset retry count (called on state transition)
reset_retry_count() {
    local workspace="$1"
    local state_file="$workspace/.ralph/state.md"
    
    sedi "s/^retry_count:.*/retry_count: 0/" "$state_file"
}

# Transition to next state
transition_state() {
    local workspace="$1"
    local new_state="$2"
    local state_file="$workspace/.ralph/state.md"
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local old_state
    old_state=$(get_current_state "$workspace")
    
    # Update current state
    sedi "s/^current_state:.*/current_state: $new_state/" "$state_file"
    
    # Reset retry count
    sedi "s/^retry_count:.*/retry_count: 0/" "$state_file"
    
    # Append to history
    echo "  - $timestamp | $old_state -> $new_state" >> "$state_file"
    
    echo -e "${GREEN}✓ Transitioned: $old_state → $new_state${NC}"
}

# =============================================================================
# Task File Parsing (RALPH_TASK.md)
# =============================================================================

# Check if task file is in state machine mode
is_state_machine_mode() {
    local workspace="$1"
    local task_file="$workspace/RALPH_TASK.md"
    
    if [[ ! -f "$task_file" ]]; then
        return 1
    fi
    
    grep -q "^mode: state_machine" "$task_file"
}

# Get spec file from task
get_spec_file() {
    local workspace="$1"
    local task_file="$workspace/RALPH_TASK.md"
    
    grep "^spec_file:" "$task_file" | cut -d: -f2- | tr -d ' '
}

# Get PRP file from task (may be generated)
get_prp_file() {
    local workspace="$1"
    local task_file="$workspace/RALPH_TASK.md"
    
    # First check if explicitly defined
    local prp
    prp=$(grep "^prp_file:" "$task_file" 2>/dev/null | cut -d: -f2- | tr -d ' ')
    
    if [[ -z "$prp" ]]; then
        # Derive from spec file
        local spec
        spec=$(get_spec_file "$workspace")
        prp="${spec%.spec.md}.prp.md"
        prp="${prp/specs/prp}"
    fi
    
    echo "$prp"
}

# Get all state names in order
get_state_order() {
    local workspace="$1"
    local task_file="$workspace/RALPH_TASK.md"
    
    # Extract state names with their order numbers, sort, return names only
    grep -E "^### [A-Z_]+" "$task_file" | \
        while read -r line; do
            state=$(echo "$line" | sed 's/^### //')
            # Get order from next line
            order=$(grep -A1 "^### $state$" "$task_file" | grep "^order:" | cut -d: -f2 | tr -d ' ')
            echo "$order $state"
        done | sort -n | awk '{print $2}'
}

# Get next state after current
get_next_state() {
    local workspace="$1"
    local current_state="$2"
    local states
    states=$(get_state_order "$workspace")
    local found=false
    
    while read -r state; do
        if $found; then
            echo "$state"
            return 0
        fi
        if [[ "$state" == "$current_state" ]]; then
            found=true
        fi
    done <<< "$states"
    
    # No next state means we're at terminal
    echo "COMPLETE"
}

# Get gate command for a state
get_gate_command() {
    local workspace="$1"
    local state="$2"
    local task_file="$workspace/RALPH_TASK.md"
    
    # Parse the command block for this state
    # Format: ### STATE_NAME\norder: N\ncommand: |\n  actual_command
    awk -v state="$state" '
        $0 ~ "^### " state "$" { found=1; next }
        found && /^command:/ { in_cmd=1; next }
        found && in_cmd && /^[a-z_]+:/ { exit }
        found && in_cmd { gsub(/^  /, ""); print }
    ' "$task_file"
}

# Get pass condition for a state
get_pass_condition() {
    local workspace="$1"
    local state="$2"
    local task_file="$workspace/RALPH_TASK.md"
    
    awk -v state="$state" '
        $0 ~ "^### " state "$" { found=1; next }
        found && /^pass_condition:/ { gsub(/^pass_condition: *"?/, ""); gsub(/"$/, ""); print; exit }
    ' "$task_file"
}

# Get on_fail action for a state
get_on_fail() {
    local workspace="$1"
    local state="$2"
    local task_file="$workspace/RALPH_TASK.md"
    
    awk -v state="$state" '
        $0 ~ "^### " state "$" { found=1; next }
        found && /^on_fail:/ { gsub(/^on_fail: */, ""); print; exit }
    ' "$task_file"
}

# Check if state is terminal
is_terminal_state() {
    local workspace="$1"
    local state="$2"
    local task_file="$workspace/RALPH_TASK.md"
    
    awk -v state="$state" '
        $0 ~ "^### " state "$" { found=1; next }
        found && /^terminal: *true/ { print "yes"; exit }
        found && /^###/ { exit }
    ' "$task_file" | grep -q "yes"
}

# Get GUTTER action
get_gutter_action() {
    local workspace="$1"
    local task_file="$workspace/RALPH_TASK.md"
    
    awk '
        /^## GUTTER Configuration/ { found=1; next }
        found && /^on_gutter:/ { in_gutter=1; next }
        found && in_gutter && /^[a-z]+:/ { exit }
        found && in_gutter { gsub(/^  /, ""); print }
    ' "$task_file"
}

# =============================================================================
# Gate Execution
# =============================================================================

# Run gate command and capture output
run_gate_command() {
    local workspace="$1"
    local state="$2"
    local command
    command=$(get_gate_command "$workspace" "$state")
    
    # Substitute variables
    local spec_file
    spec_file=$(get_spec_file "$workspace")
    local prp_file
    prp_file=$(get_prp_file "$workspace")
    
    command="${command//\{\{spec_file\}\}/$spec_file}"
    command="${command//\{\{prp_file\}\}/$prp_file}"
    command="${command//\{\{current_state\}\}/$state}"
    
    echo -e "${CYAN}Running gate command for $state...${NC}" >&2
    echo -e "${MAGENTA}$command${NC}" >&2
    
    # Run and capture output
    local output
    output=$(cd "$workspace" && eval "$command" 2>&1)
    local exit_code=$?
    
    echo "$output"
    return $exit_code
}

# Check if gate output indicates pass
check_gate_passed() {
    local output="$1"
    local pass_condition="$2"

    # Special handling for pytest output
    if echo "$pass_condition" | grep -qi "passed"; then
        # If pass_condition mentions "passed", ensure no test failures
        if echo "$output" | grep -E "^(FAILED|ERROR|.* FAILED)" >/dev/null; then
            return 1
        fi
    fi

    # Check for pass condition in output (case-insensitive)
    if echo "$output" | grep -qi "$pass_condition"; then
        return 0
    else
        return 1
    fi
}

# Execute GUTTER action
execute_gutter() {
    local workspace="$1"
    local state="$2"
    local last_output="$3"

    # Save last output to log
    mkdir -p "$workspace/.ralph"
    echo "$last_output" > "$workspace/.ralph/gutter-$state.log"

    # Save diff
    (cd "$workspace" && git diff > ".ralph/gutter-diff.patch" 2>/dev/null) || true

    # Get and run custom gutter action
    local gutter_action
    gutter_action=$(get_gutter_action "$workspace")

    # Substitute state variable
    gutter_action="${gutter_action//\{\{current_state\}\}/$state}"

    if [[ -n "$gutter_action" ]]; then
        echo -e "${RED}🚨 GUTTER: Executing custom action...${NC}"
        (cd "$workspace" && eval "$gutter_action")
    else
        echo -e "${RED}🚨 GUTTER REACHED: Max retries exhausted for state: $state${NC}"
        echo -e "${YELLOW}Last output saved to: .ralph/gutter-$state.log${NC}"
        echo -e "${YELLOW}Diff saved to: .ralph/gutter-diff.patch${NC}"
        echo -e "${YELLOW}To resume: ./ralph-loop.sh --state-machine --resume -y${NC}"
    fi
}

# =============================================================================
# Display Functions
# =============================================================================

show_state_status() {
    local workspace="$1"
    local current
    current=$(get_current_state "$workspace")
    local retries
    retries=$(get_retry_count "$workspace")
    local max
    max=$(get_max_retries "$workspace")
    
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           RALPH State Machine Status                     ║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║${NC}  Current State:  ${GREEN}$current${NC}"
    echo -e "${CYAN}║${NC}  Retry Count:    ${YELLOW}$retries / $max${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Show pipeline progress
    local states
    states=$(get_state_order "$workspace")
    local reached=true
    
    echo -e "${CYAN}Pipeline Progress:${NC}"
    while read -r state; do
        if [[ "$state" == "$current" ]]; then
            echo -e "  ${YELLOW}▶ $state${NC} (current)"
            reached=false
        elif $reached; then
            echo -e "  ${GREEN}✓ $state${NC}"
        else
            echo -e "  ${NC}○ $state${NC}"
        fi
    done <<< "$states"
    echo ""
}
