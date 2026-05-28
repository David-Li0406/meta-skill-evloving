#!/usr/bin/env bash
# E2E test for Agent Mail auto-registration on spawn
# Tests that agents spawned with ntm are automatically registered with Agent Mail
# and that pane-to-agent name mappings are persisted for session recovery.
set -euo pipefail

log_e2e() {
    local test="$1"
    local step="$2"
    local status="$3"
    local details="$4"
    echo "[E2E-AMREG] $(date -Iseconds) test=${test} step=${step} status=${status} details=\"${details}\""
}

require_cmd() {
    local cmd="$1"
    if ! command -v "$cmd" >/dev/null 2>&1; then
        log_e2e "$TEST_NAME" "prereq" "fail" "missing=${cmd}"
        exit 1
    fi
}

check_agent_mail() {
    # Check if Agent Mail server is running by trying to list projects
    if ! curl -sf "http://localhost:8765/projects" >/dev/null 2>&1; then
        log_e2e "$TEST_NAME" "prereq" "skip" "Agent Mail server not running"
        exit 0
    fi
}

TEST_NAME="agent_mail_registration"
SESSION="e2e-amreg-${RANDOM}-$$"

TMP_ROOT="$(mktemp -d)"
PROJECTS_BASE="${TMP_ROOT}/projects"
CONFIG_DIR="${TMP_ROOT}/config"
CONFIG_PATH="${CONFIG_DIR}/config.toml"
PROJECT_DIR="${PROJECTS_BASE}/${SESSION}"
# Use temp directory for session data to avoid polluting real config
export XDG_CONFIG_HOME="${TMP_ROOT}/xdg_config"

cleanup() {
    tmux kill-session -t "${SESSION}" >/dev/null 2>&1 || true
    rm -rf "${TMP_ROOT}" || true
}
trap cleanup EXIT

mkdir -p "${PROJECTS_BASE}" "${CONFIG_DIR}" "${PROJECT_DIR}" "${XDG_CONFIG_HOME}"

# Create test config with Agent Mail enabled
cat > "${CONFIG_PATH}" <<EOF
projects_base = "${PROJECTS_BASE}"

[agents]
claude = "bash"
codex = "bash"
gemini = "bash"

[agent_mail]
enabled = true
EOF

# Check prerequisites
require_cmd ntm
require_cmd tmux
require_cmd curl
require_cmd jq

# Check Agent Mail availability (skip test if not running)
check_agent_mail
log_e2e "${TEST_NAME}" "prereq" "pass" "Agent Mail server available"

# Spawn agents with --cc=2 --cod=1 (3 total agents)
log_e2e "${TEST_NAME}" "spawn" "start" "cc=2 cod=1"
spawn_output="$(echo "y" | ntm --config "${CONFIG_PATH}" --json spawn "${SESSION}" --cc=2 --cod=1 2>&1)" || {
    log_e2e "${TEST_NAME}" "spawn" "fail" "exit_code=$?"
    echo "Spawn output: ${spawn_output}"
    exit 1
}
log_e2e "${TEST_NAME}" "spawn" "complete" "session=${SESSION}"

# Wait for panes to be ready
sleep 1

# Verify pane count
agent_pane_count="$(tmux list-panes -t "${SESSION}" -F '#{pane_title}' | grep -E '__(cc|cod)_' | wc -l | tr -d ' ')"
if [[ "${agent_pane_count}" != "3" ]]; then
    log_e2e "${TEST_NAME}" "verify_panes" "fail" "expected=3 got=${agent_pane_count}"
    tmux list-panes -t "${SESSION}" -F '#{pane_title}'
    exit 1
fi
log_e2e "${TEST_NAME}" "verify_panes" "pass" "pane_count=${agent_pane_count}"

# Check Agent Mail registration via API
log_e2e "${TEST_NAME}" "verify_registration" "start" "checking Agent Mail agents"

# URL-encode the project directory
PROJECT_KEY_ENCODED="$(printf '%s' "${PROJECT_DIR}" | jq -sRr @uri)"

# List agents for this project
agents_json="$(curl -sf "http://localhost:8765/projects/${PROJECT_KEY_ENCODED}/agents" 2>/dev/null)" || {
    log_e2e "${TEST_NAME}" "verify_registration" "fail" "could not query agents"
    exit 1
}

agent_count="$(echo "${agents_json}" | jq 'length')"
if [[ "${agent_count}" -lt 3 ]]; then
    log_e2e "${TEST_NAME}" "verify_registration" "fail" "expected>=3 agents got=${agent_count}"
    echo "Agents: ${agents_json}"
    exit 1
fi
log_e2e "${TEST_NAME}" "verify_registration" "pass" "agent_count=${agent_count}"

# Verify registry file was created with pane mappings
log_e2e "${TEST_NAME}" "verify_registry" "start" "checking persistent registry"

# Get the project slug for the registry path
# The slug is derived from the project directory name
project_slug="$(basename "${PROJECT_DIR}")"
registry_path="${XDG_CONFIG_HOME}/ntm/sessions/${SESSION}/${project_slug}/agent_registry.json"

if [[ ! -f "${registry_path}" ]]; then
    log_e2e "${TEST_NAME}" "verify_registry" "fail" "registry file not found at ${registry_path}"
    # List what exists
    find "${XDG_CONFIG_HOME}" -name "*.json" -type f 2>/dev/null || true
    exit 1
fi

# Verify registry content
registry_json="$(cat "${registry_path}")"
registry_agent_count="$(echo "${registry_json}" | jq '.agents | length')"
if [[ "${registry_agent_count}" != "3" ]]; then
    log_e2e "${TEST_NAME}" "verify_registry" "fail" "expected 3 agents in registry got=${registry_agent_count}"
    echo "Registry content: ${registry_json}"
    exit 1
fi
log_e2e "${TEST_NAME}" "verify_registry" "pass" "registry_agents=${registry_agent_count}"

# Verify pane titles in registry match actual panes
pane_titles="$(tmux list-panes -t "${SESSION}" -F '#{pane_title}' | grep -E '__(cc|cod)_' | sort)"
registry_titles="$(echo "${registry_json}" | jq -r '.agents | keys[]' | sort)"

# Check that each pane title appears in the registry
while IFS= read -r title; do
    if ! echo "${registry_titles}" | grep -qF "${title}"; then
        log_e2e "${TEST_NAME}" "verify_mapping" "fail" "pane title not in registry: ${title}"
        exit 1
    fi
done <<< "${pane_titles}"
log_e2e "${TEST_NAME}" "verify_mapping" "pass" "all pane titles mapped"

# Verify each registry entry has a valid agent name (adjective-noun format from server)
while IFS= read -r agent_name; do
    if [[ -z "${agent_name}" ]]; then
        log_e2e "${TEST_NAME}" "verify_names" "fail" "empty agent name in registry"
        exit 1
    fi
    # Agent names should be non-empty and typically follow adjective-noun pattern
    # Just verify they're not placeholder values
    if [[ "${agent_name}" == "placeholder" || "${agent_name}" == "unknown" ]]; then
        log_e2e "${TEST_NAME}" "verify_names" "fail" "placeholder agent name: ${agent_name}"
        exit 1
    fi
done <<< "$(echo "${registry_json}" | jq -r '.agents[]')"
log_e2e "${TEST_NAME}" "verify_names" "pass" "all agent names valid"

# Verify pane_id_map is also populated
pane_id_count="$(echo "${registry_json}" | jq '.pane_id_map | length')"
if [[ "${pane_id_count}" != "3" ]]; then
    log_e2e "${TEST_NAME}" "verify_pane_ids" "fail" "expected 3 pane IDs got=${pane_id_count}"
    exit 1
fi
log_e2e "${TEST_NAME}" "verify_pane_ids" "pass" "pane_id_count=${pane_id_count}"

log_e2e "${TEST_NAME}" "complete" "pass" "all verifications passed"
