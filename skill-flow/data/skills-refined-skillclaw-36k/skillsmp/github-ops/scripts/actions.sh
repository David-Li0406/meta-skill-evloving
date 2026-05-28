#!/usr/bin/env bash
#
# actions.sh - GitHub Actions Operations for GitHub Ops Skill
# MCP Parity: list_workflows, list_workflow_runs, get_workflow_run, get_workflow_run_logs,
#             list_workflow_jobs, get_job_logs, rerun_workflow_run, rerun_failed_jobs,
#             cancel_workflow_run, run_workflow, list_workflow_run_artifacts,
#             download_workflow_run_artifact, delete_workflow_run_logs, get_workflow_run_usage
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
LIMIT=30
JSON_OUTPUT=false
CONFIRM_DESTRUCTIVE=true

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

GitHub Actions Operations - GitHub MCP Server Parity

Actions:
  workflows         List workflows
  runs              List workflow runs
  run               View a workflow run
  jobs              List jobs in a run
  logs              Get run/job logs
  artifacts         List run artifacts
  download-artifact Download an artifact
  rerun             Rerun a workflow run
  rerun-failed      Rerun failed jobs
  cancel            Cancel a workflow run
  dispatch          Trigger a workflow
  usage             Get workflow run usage

Common Options:
  --owner OWNER     Repository owner
  --repo REPO       Repository name
  --run-id ID       Workflow run ID
  --job-id ID       Job ID
  --workflow FILE   Workflow file name
  --status STATUS   Filter by status (queued, in_progress, completed, etc.)
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") workflows --owner cli --repo cli
  $(basename "$0") runs --owner cli --repo cli --workflow ci.yml --limit 5
  $(basename "$0") run --owner cli --repo cli --run-id 12345
  $(basename "$0") logs --owner cli --repo cli --run-id 12345 --failed-only
EOF
    exit 0
}

error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}$1${NC}"
}

warn() {
    echo -e "${YELLOW}$1${NC}"
}

info() {
    echo -e "${BLUE}$1${NC}"
}

confirm() {
    if [[ "$CONFIRM_DESTRUCTIVE" == "true" ]]; then
        echo -e "${YELLOW}Warning: $1${NC}"
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Operation cancelled."
            exit 2
        fi
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --owner) OWNER="$2"; shift 2 ;;
            --repo) REPO="$2"; shift 2 ;;
            --run-id) RUN_ID="$2"; shift 2 ;;
            --job-id) JOB_ID="$2"; shift 2 ;;
            --artifact-id) ARTIFACT_ID="$2"; shift 2 ;;
            --workflow) WORKFLOW="$2"; shift 2 ;;
            --ref) REF="$2"; shift 2 ;;
            --status) STATUS="$2"; shift 2 ;;
            --actor) ACTOR="$2"; shift 2 ;;
            --branch) BRANCH="$2"; shift 2 ;;
            --event) EVENT="$2"; shift 2 ;;
            --inputs) INPUTS="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --failed-only) FAILED_ONLY=true; shift ;;
            --json) JSON_OUTPUT=true; shift ;;
            --no-confirm) CONFIRM_DESTRUCTIVE=false; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: List workflows
action_workflows() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing workflows for $OWNER/$REPO"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/actions/workflows?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/actions/workflows?per_page=$LIMIT" \
            --jq '.workflows[] | "\(.id)\t\(.name)\t\(.state)\t\(.path)"' | column -t -s $'\t'
    fi
}

# Action: List workflow runs
action_runs() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing workflow runs for $OWNER/$REPO (limit: $LIMIT)"
    
    local cmd="gh run list --repo $OWNER/$REPO --limit $LIMIT"
    
    [[ -n "${WORKFLOW:-}" ]] && cmd="$cmd --workflow $WORKFLOW"
    [[ -n "${STATUS:-}" ]] && cmd="$cmd --status $STATUS"
    [[ -n "${BRANCH:-}" ]] && cmd="$cmd --branch $BRANCH"
    [[ -n "${ACTOR:-}" ]] && cmd="$cmd --user $ACTOR"
    [[ -n "${EVENT:-}" ]] && cmd="$cmd --event $EVENT"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd="$cmd --json databaseId,name,displayTitle,status,conclusion,headBranch,event,createdAt,updatedAt"
    fi
    
    eval "$cmd"
}

# Action: View workflow run
action_run() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${RUN_ID:-}" ]] && error "Missing --run-id"
    
    info "Fetching workflow run #$RUN_ID"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/actions/runs/$RUN_ID"
    else
        gh run view "$RUN_ID" --repo "$OWNER/$REPO"
    fi
}

# Action: List jobs in a run
action_jobs() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${RUN_ID:-}" ]] && error "Missing --run-id"
    
    info "Listing jobs for run #$RUN_ID"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/actions/runs/$RUN_ID/jobs?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/actions/runs/$RUN_ID/jobs?per_page=$LIMIT" \
            --jq '.jobs[] | "\(.id)\t\(.name)\t\(.status)\t\(.conclusion // "-")\t\(.started_at[0:19])"' | column -t -s $'\t'
    fi
}

# Action: Get logs
action_logs() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    if [[ -n "${JOB_ID:-}" ]]; then
        info "Fetching logs for job #$JOB_ID"
        gh api "repos/$OWNER/$REPO/actions/jobs/$JOB_ID/logs" 2>/dev/null || \
            warn "Note: Logs may have been deleted or the job may still be running"
    elif [[ -n "${RUN_ID:-}" ]]; then
        if [[ "${FAILED_ONLY:-false}" == "true" ]]; then
            info "Fetching logs for failed jobs in run #$RUN_ID"
            gh run view "$RUN_ID" --repo "$OWNER/$REPO" --log-failed
        else
            info "Fetching logs for run #$RUN_ID"
            gh run view "$RUN_ID" --repo "$OWNER/$REPO" --log
        fi
    else
        error "Missing --run-id or --job-id"
    fi
}

# Action: List artifacts
action_artifacts() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${RUN_ID:-}" ]] && error "Missing --run-id"
    
    info "Listing artifacts for run #$RUN_ID"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/actions/runs/$RUN_ID/artifacts"
    else
        gh api "repos/$OWNER/$REPO/actions/runs/$RUN_ID/artifacts" \
            --jq '.artifacts[] | "\(.id)\t\(.name)\t\(.size_in_bytes) bytes\t\(.created_at[0:19])"' | column -t -s $'\t'
    fi
}

# Action: Download artifact
action_download_artifact() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${ARTIFACT_ID:-}" ]] && error "Missing --artifact-id"
    
    info "Downloading artifact #$ARTIFACT_ID"
    
    # Get artifact info
    local artifact_name
    artifact_name=$(gh api "repos/$OWNER/$REPO/actions/artifacts/$ARTIFACT_ID" --jq '.name')
    
    # Download
    gh api "repos/$OWNER/$REPO/actions/artifacts/$ARTIFACT_ID/zip" > "${artifact_name}.zip"
    success "Downloaded: ${artifact_name}.zip"
}

# Action: Rerun workflow
action_rerun() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${RUN_ID:-}" ]] && error "Missing --run-id"
    
    confirm "This will rerun workflow run #$RUN_ID"
    
    info "Rerunning workflow run #$RUN_ID"
    gh run rerun "$RUN_ID" --repo "$OWNER/$REPO"
    success "Workflow rerun initiated"
}

# Action: Rerun failed jobs
action_rerun_failed() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${RUN_ID:-}" ]] && error "Missing --run-id"
    
    confirm "This will rerun failed jobs in run #$RUN_ID"
    
    info "Rerunning failed jobs in run #$RUN_ID"
    gh run rerun "$RUN_ID" --repo "$OWNER/$REPO" --failed
    success "Failed jobs rerun initiated"
}

# Action: Cancel run
action_cancel() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${RUN_ID:-}" ]] && error "Missing --run-id"
    
    confirm "This will CANCEL workflow run #$RUN_ID"
    
    info "Cancelling workflow run #$RUN_ID"
    gh run cancel "$RUN_ID" --repo "$OWNER/$REPO"
    success "Workflow run cancelled"
}

# Action: Trigger workflow
action_dispatch() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${WORKFLOW:-}" ]] && error "Missing --workflow"
    
    confirm "This will trigger workflow '$WORKFLOW' in $OWNER/$REPO"
    
    local ref="${REF:-main}"
    
    info "Triggering workflow: $WORKFLOW (ref: $ref)"
    
    local cmd="gh workflow run $WORKFLOW --repo $OWNER/$REPO --ref $ref"
    
    if [[ -n "${INPUTS:-}" ]]; then
        # Parse JSON inputs and pass as -f flags
        while IFS='=' read -r key value; do
            cmd="$cmd -f $key=$value"
        done < <(echo "$INPUTS" | jq -r 'to_entries[] | "\(.key)=\(.value)"')
    fi
    
    eval "$cmd"
    success "Workflow triggered"
}

# Action: Get usage
action_usage() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${RUN_ID:-}" ]] && error "Missing --run-id"
    
    info "Fetching usage for run #$RUN_ID"
    
    gh api "repos/$OWNER/$REPO/actions/runs/$RUN_ID/timing"
}

main() {
    [[ $# -eq 0 ]] && usage
    
    local action="$1"
    shift
    
    parse_args "$@"
    
    case "$action" in
        workflows) action_workflows ;;
        runs) action_runs ;;
        run) action_run ;;
        jobs) action_jobs ;;
        logs) action_logs ;;
        artifacts) action_artifacts ;;
        download-artifact) action_download_artifact ;;
        rerun) action_rerun ;;
        rerun-failed) action_rerun_failed ;;
        cancel) action_cancel ;;
        dispatch) action_dispatch ;;
        usage) action_usage ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action. Use --help for usage." ;;
    esac
}

main "$@"
