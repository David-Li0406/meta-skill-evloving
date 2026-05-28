#!/bin/bash
# ralph-loop.sh - State-Aware RALPH Loop
# Runs cursor-agent in a loop with state machine progression and bounded retries
#
# Usage:
#   ./ralph-loop.sh --state-machine -n 20 --max-gate-retries 5 -y
#   ./ralph-loop.sh --state-machine --resume -y
#
# Modes:
#   Default (checkbox): Original behavior, tracks checkboxes
#   State Machine: Explicit gate transitions with retry limits

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/ralph-common.sh"

# =============================================================================
# Configuration
# =============================================================================

WORKSPACE="${WORKSPACE:-$(pwd)}"
MAX_ITERATIONS=20
MAX_GATE_RETRIES=5
STATE_MACHINE_MODE=false
RESUME=false
AUTO_APPROVE=false
DRY_RUN=false
VERBOSE=false

# =============================================================================
# Usage
# =============================================================================

usage() {
    cat <<EOF
Ralph Loop - State-Aware Autonomous Agent Runner

Usage: $(basename "$0") [OPTIONS]

Options:
  --state-machine       Enable state machine mode (vs checkbox mode)
  --resume              Resume from last state (don't reinitialize)
  -n, --iterations N    Max total iterations (default: 20)
  --max-gate-retries N  Max retries per gate before GUTTER (default: 5)
  -y, --yes             Auto-approve all prompts
  --dry-run             Show what would happen without executing
  -v, --verbose         Verbose output
  -h, --help            Show this help

Examples:
  # Run full pipeline with state machine
  $(basename "$0") --state-machine -n 30 --max-gate-retries 5 -y

  # Resume after GUTTER
  $(basename "$0") --state-machine --resume -y

  # Dry run to see gate commands
  $(basename "$0") --state-machine --dry-run

Environment:
  WORKSPACE             Project directory (default: pwd)
  CURSOR_AGENT          Path to cursor-agent (default: cursor-agent)

EOF
    exit 0
}

# =============================================================================
# Argument Parsing
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --state-machine)
            STATE_MACHINE_MODE=true
            shift
            ;;
        --resume)
            RESUME=true
            shift
            ;;
        -n|--iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --max-gate-retries)
            MAX_GATE_RETRIES="$2"
            shift 2
            ;;
        -y|--yes)
            AUTO_APPROVE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# =============================================================================
# Validation
# =============================================================================

validate_workspace() {
    if [[ ! -f "$WORKSPACE/RALPH_TASK.md" ]]; then
        echo -e "${RED}Error: RALPH_TASK.md not found in $WORKSPACE${NC}"
        exit 1
    fi
    
    if $STATE_MACHINE_MODE && ! is_state_machine_mode "$WORKSPACE"; then
        echo -e "${RED}Error: RALPH_TASK.md is not in state_machine mode${NC}"
        echo -e "${YELLOW}Hint: Add 'mode: state_machine' to the frontmatter${NC}"
        exit 1
    fi
}

# =============================================================================
# State Machine Loop
# =============================================================================

run_state_machine_loop() {
    local iteration=0
    local last_output=""
    
    # Initialize or resume state
    if [[ "$RESUME" != true ]]; then
        initialize_state "$WORKSPACE"
        # Transition from INIT to first actual state
        local first_state
        first_state=$(get_state_order "$WORKSPACE" | head -1)
        if [[ -n "$first_state" && "$first_state" != "INIT" ]]; then
            transition_state "$WORKSPACE" "$first_state"
        fi
    else
        echo -e "${CYAN}Resuming from existing state...${NC}"
        reset_retry_count "$WORKSPACE"
    fi
    
    # Set max retries in state file
    set_max_retries "$WORKSPACE" "$MAX_GATE_RETRIES"
    
    # Show initial status
    show_state_status "$WORKSPACE"
    
    # Main loop
    while [[ $iteration -lt $MAX_ITERATIONS ]]; do
        iteration=$((iteration + 1))
        
        local state
        state=$(get_current_state "$WORKSPACE")
        local retries
        retries=$(get_retry_count "$WORKSPACE")
        
        echo ""
        echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
        echo -e "${CYAN}  Iteration $iteration / $MAX_ITERATIONS  |  State: $state  |  Retry: $retries / $MAX_GATE_RETRIES${NC}"
        echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
        
        # Check if terminal state
        if is_terminal_state "$WORKSPACE" "$state"; then
            echo -e "${GREEN}🎉 Reached terminal state: $state${NC}"
            echo -e "${GREEN}Pipeline complete!${NC}"
            return 0
        fi
        
        # Check COMPLETE state
        if [[ "$state" == "COMPLETE" ]]; then
            echo -e "${GREEN}🎉 All gates passed!${NC}"
            return 0
        fi
        
        # Check retry limit
        if [[ $retries -ge $MAX_GATE_RETRIES ]]; then
            echo -e "${RED}🚨 GUTTER: Max retries ($MAX_GATE_RETRIES) exceeded for state $state${NC}"
            execute_gutter "$WORKSPACE" "$state" "$last_output"
            return 1
        fi
        
        # Get gate info
        local command
        command=$(get_gate_command "$WORKSPACE" "$state")
        local pass_condition
        pass_condition=$(get_pass_condition "$WORKSPACE" "$state")
        local on_fail
        on_fail=$(get_on_fail "$WORKSPACE" "$state")
        
        if $VERBOSE; then
            echo -e "${MAGENTA}Gate Command:${NC}"
            echo "$command"
            echo -e "${MAGENTA}Pass Condition: $pass_condition${NC}"
        fi
        
        if $DRY_RUN; then
            echo -e "${YELLOW}[DRY RUN] Would execute:${NC}"
            echo "$command"
            echo -e "${YELLOW}[DRY RUN] Pass condition: $pass_condition${NC}"
            
            # Simulate pass for dry run
            local next_state
            next_state=$(get_next_state "$WORKSPACE" "$state")
            echo -e "${YELLOW}[DRY RUN] Would transition to: $next_state${NC}"
            transition_state "$WORKSPACE" "$next_state"
            continue
        fi
        
        # Generate agent prompt
        local prompt
        prompt=$(generate_agent_prompt "$WORKSPACE" "$state" "$iteration")
        
        # Run cursor-agent
        echo -e "${CYAN}Spawning cursor-agent for state: $state${NC}"
        
        local agent_cmd="${CURSOR_AGENT:-cursor-agent}"
        if $AUTO_APPROVE; then
            $agent_cmd "$prompt" || true
        else
            $agent_cmd "$prompt" || true
        fi
        
        # Run gate command to check result
        echo -e "${CYAN}Checking gate...${NC}"
        local gate_output
        gate_output=$(run_gate_command "$WORKSPACE" "$state") || true
        last_output="$gate_output"
        
        if $VERBOSE; then
            echo -e "${MAGENTA}Gate Output:${NC}"
            echo "$gate_output"
        fi
        
        # Check if gate passed
        if check_gate_passed "$gate_output" "$pass_condition"; then
            local next_state
            next_state=$(get_next_state "$WORKSPACE" "$state")
            echo -e "${GREEN}✅ Gate PASSED: $state → $next_state${NC}"
            transition_state "$WORKSPACE" "$next_state"
        else
            local new_retries
            new_retries=$(increment_retry "$WORKSPACE")
            echo -e "${RED}❌ Gate FAILED (retry $new_retries/$MAX_GATE_RETRIES)${NC}"
            
            if [[ -n "$on_fail" ]]; then
                echo -e "${YELLOW}Hint: $on_fail${NC}"
            fi
        fi
        
        # Brief pause between iterations
        sleep 1
    done
    
    echo -e "${YELLOW}Max iterations ($MAX_ITERATIONS) reached${NC}"
    return 1
}

# =============================================================================
# Agent Prompt Generation
# =============================================================================

generate_agent_prompt() {
    local workspace="$1"
    local state="$2"
    local iteration="$3"
    
    local retries
    retries=$(get_retry_count "$workspace")
    local max_retries
    max_retries=$(get_max_retries "$workspace")
    local remaining=$((max_retries - retries))
    
    local command
    command=$(get_gate_command "$workspace" "$state")
    local pass_condition
    pass_condition=$(get_pass_condition "$workspace" "$state")
    local on_fail
    on_fail=$(get_on_fail "$workspace" "$state")
    
    # Substitute variables in command
    local spec_file
    spec_file=$(get_spec_file "$workspace")
    local prp_file
    prp_file=$(get_prp_file "$workspace")
    
    command="${command//\{\{spec_file\}\}/$spec_file}"
    command="${command//\{\{prp_file\}\}/$prp_file}"
    
    cat <<EOF
# Ralph State Machine - Iteration $iteration

## Current State: $state
## Retry: $retries / $max_retries

## Your Task

You are working on gate: **$state**

**Gate Command**:
\`\`\`bash
$command
\`\`\`

**Pass Condition**: Output must contain "$pass_condition"

## Instructions

1. Read the current spec/PRP/code as needed
2. Run the gate command above
3. If it FAILS:
   - Read the output carefully
   - Fix the issues identified
   - Hint: $on_fail
   - Commit your fix: \`git add -A && git commit -m "fix($state): [what you fixed]"\`
4. If it PASSES:
   - The loop will automatically transition you to the next state
   - Do NOT manually edit .ralph/state.md

## Important

- You have **$remaining attempts left** for this gate
- If you exhaust retries, you'll enter GUTTER state (requires human intervention)
- Focus ONLY on passing the current gate, not future states
- After making changes, run the gate command again to verify

## Files to Check

- Spec: $spec_file
- PRP: $prp_file
- State: .ralph/state.md

EOF
}

# =============================================================================
# Main
# =============================================================================

main() {
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           Ralph Loop - State Machine Mode                ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    validate_workspace
    
    if $STATE_MACHINE_MODE; then
        run_state_machine_loop
    else
        echo -e "${RED}Error: Non-state-machine mode not implemented in this version${NC}"
        echo -e "${YELLOW}Use --state-machine flag${NC}"
        exit 1
    fi
}

main "$@"
