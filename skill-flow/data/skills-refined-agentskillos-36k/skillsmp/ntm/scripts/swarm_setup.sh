#!/bin/bash
# swarm_setup.sh - Create tmux sessions with agent panes for multi-project work
# Usage: ./swarm_setup.sh [--launch]
#   --launch: Also start the agents (cc, cod, gmi) in each pane

set -euo pipefail

LAUNCH_AGENTS=false
if [[ "${1:-}" == "--launch" ]]; then
    LAUNCH_AGENTS=true
fi

# Kill existing tmux server
tmux kill-server 2>/dev/null || true
sleep 1

PANES_PER_SESSION=12

# Session names
CC_SESSIONS=(cc_agents_1 cc_agents_2 cc_agents_3)
COD_SESSIONS=(cod_agents_1 cod_agents_2 cod_agents_3)
GMI_SESSIONS=(gmi_agents_1 gmi_agents_2 gmi_agents_3)

# Project assignments with agent counts
# Format: "project_name:cc_count:cod_count:gmi_count"
PROJECTS=(
    "flywheel_connectors:4:4:2"
    "wezterm_automata:3:3:2"
    "asupersync:3:3:2"
    "ntm:3:3:2"
    "jeffreysprompts_premium:3:3:2"
    "jeffreys-skills.md:3:3:2"
    "rust_stream_deck:1:1:1"
    "fastapi_rust:1:1:1"
    "coding_agent_usage_tracker:1:1:1"
    "process_triage:1:1:1"
    "coding_agent_account_manager:1:1:1"
    "rust_proxy:1:1:1"
    "remote_compilation_helper:1:1:1"
    "destructive_command_guard:1:1:1"
    "flywheel_gateway:1:1:1"
    "meta_skill:1:1:1"
    "agent_settings_backup_script:1:1:1"
    "coding_agent_session_search:1:1:1"
    "sqlmodel_rust:1:1:1"
    "rano:1:1:1"
    "agentic_coding_flywheel_setup:1:1:1"
)

# Build flat arrays of pane assignments
declare -a CC_PANES=()
declare -a COD_PANES=()
declare -a GMI_PANES=()

for proj_spec in "${PROJECTS[@]}"; do
    IFS=':' read -r proj cc_count cod_count gmi_count <<< "$proj_spec"
    for ((i=0; i<cc_count; i++)); do
        CC_PANES+=("$proj")
    done
    for ((i=0; i<cod_count; i++)); do
        COD_PANES+=("$proj")
    done
    for ((i=0; i<gmi_count; i++)); do
        GMI_PANES+=("$proj")
    done
done

# Pad arrays to fill all panes
while ((${#CC_PANES[@]} < PANES_PER_SESSION * 3)); do
    CC_PANES+=("EMPTY")
done
while ((${#COD_PANES[@]} < PANES_PER_SESSION * 3)); do
    COD_PANES+=("EMPTY")
done
while ((${#GMI_PANES[@]} < PANES_PER_SESSION * 3)); do
    GMI_PANES+=("EMPTY")
done

echo "CC agents: 34 (+2 empty), COD agents: 34 (+2 empty), GMI agents: 27 (+9 empty)"

# Create a session with 12 panes using simple sequential splitting
create_session_with_panes() {
    local session_name=$1

    # Create session with first window
    tmux new-session -d -s "$session_name" -x 320 -y 80

    # Add 11 more panes by splitting (total = 12)
    for ((i=1; i<12; i++)); do
        # Always split the first pane, tmux will rebalance
        tmux split-window -t "${session_name}"
        tmux select-layout -t "${session_name}" tiled
    done

    # Final tiled layout
    tmux select-layout -t "${session_name}" tiled
}

# Setup a specific pane with project and agent
setup_pane() {
    local session=$1
    local pane_idx=$2
    local project=$3
    local agent_cmd=$4  # cc, cod, or gmi

    local target="${session}:1.${pane_idx}"

    if [[ "$project" != "EMPTY" ]]; then
        # Change to project directory
        tmux send-keys -t "$target" "cd /dp/${project} && clear" Enter
        sleep 0.02

        if [[ "$LAUNCH_AGENTS" == "true" ]]; then
            sleep 0.1
            tmux send-keys -t "$target" "$agent_cmd" Enter
        fi
    else
        tmux send-keys -t "$target" "echo 'Empty pane - available for assignment'" Enter
    fi
}

# Create all sessions
echo "Creating sessions..."
for session in "${CC_SESSIONS[@]}" "${COD_SESSIONS[@]}" "${GMI_SESSIONS[@]}"; do
    echo "  Creating $session..."
    create_session_with_panes "$session"
done

# Helper to track instances
declare -A cc_instance=()
declare -A cod_instance=()
declare -A gmi_instance=()

# Assign CC panes
echo "Assigning CC panes..."
for session_idx in 0 1 2; do
    session="${CC_SESSIONS[$session_idx]}"
    for pane_idx in $(seq 1 12); do
        global_idx=$((session_idx * 12 + pane_idx - 1))
        proj="${CC_PANES[$global_idx]}"
        setup_pane "$session" "$pane_idx" "$proj" "cc"
    done
done

# Assign COD panes
echo "Assigning COD panes..."
for session_idx in 0 1 2; do
    session="${COD_SESSIONS[$session_idx]}"
    for pane_idx in $(seq 1 12); do
        global_idx=$((session_idx * 12 + pane_idx - 1))
        proj="${COD_PANES[$global_idx]}"
        setup_pane "$session" "$pane_idx" "$proj" "cod"
    done
done

# Assign GMI panes
echo "Assigning GMI panes..."
for session_idx in 0 1 2; do
    session="${GMI_SESSIONS[$session_idx]}"
    for pane_idx in $(seq 1 12); do
        global_idx=$((session_idx * 12 + pane_idx - 1))
        proj="${GMI_PANES[$global_idx]}"
        setup_pane "$session" "$pane_idx" "$proj" "gmi"
    done
done

echo ""
echo "=== SWARM SETUP COMPLETE ==="
echo "Sessions created:"
tmux list-sessions 2>/dev/null || echo "  (none)"
echo ""
echo "Pane layout (12 panes per session):"
echo "  CC:  ${CC_SESSIONS[*]}"
echo "  COD: ${COD_SESSIONS[*]}"
echo "  GMI: ${GMI_SESSIONS[*]}"
echo ""
if [[ "$LAUNCH_AGENTS" == "true" ]]; then
    echo "Agents launched in all panes."
else
    echo "To launch agents, run: $0 --launch"
    echo "Or attach and manually run cc/cod/gmi in each pane."
fi
echo ""
echo "Attach with: tmux attach -t cc_agents_1"
