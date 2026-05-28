#!/usr/bin/env bash
set -euo pipefail

# Safe wrapper for GitLab pipeline inspection API calls
# This script is allowlisted for Claude to use since all operations are read-only

usage() {
  cat << 'EOF'
Usage: glab-pipeline.sh <command> [args...]

Commands:
  project-id                    Get the current project's URL-encoded ID
  mr-pipelines <mr-number>      List pipelines for a merge request
  branch-pipelines <branch>     List pipelines for a branch
  pipeline-jobs <pipeline-id>   List jobs for a pipeline
  failed-jobs <pipeline-id>     List only failed jobs for a pipeline
  job-trace <job-id>            Get the log output for a job
  job-info <job-id>             Get metadata for a job
  pipeline-info <pipeline-id>   Get metadata for a pipeline

Examples:
  glab-pipeline.sh mr-pipelines 4674
  glab-pipeline.sh failed-jobs 4467641
  glab-pipeline.sh job-trace 62708639 | tail -200
EOF
}

get_project_id() {
  local project_path
  project_path=$(glab repo view --output json 2>/dev/null | jq -r '.path_with_namespace')
  # URL-encode the path (replace / with %2F)
  echo "${project_path//\//%2F}"
}

cmd_project_id() {
  get_project_id
}

cmd_mr_pipelines() {
  local mr_number="${1:-}"
  if [[ -z "$mr_number" ]]; then
    echo "Error: MR number required" >&2
    echo "Usage: glab-pipeline.sh mr-pipelines <mr-number>" >&2
    exit 1
  fi

  local project_id
  project_id=$(get_project_id)

  glab api "projects/${project_id}/merge_requests/${mr_number}/pipelines" 2>&1
}

cmd_branch_pipelines() {
  local branch="${1:-}"
  if [[ -z "$branch" ]]; then
    branch=$(git rev-parse --abbrev-ref HEAD)
  fi

  local project_id
  project_id=$(get_project_id)

  # Fetch pipelines, filtering out external (security scan) pipelines
  glab api "projects/${project_id}/pipelines?ref=${branch}&per_page=10" 2>&1 | \
    jq '[.[] | select(.source != "external")]'
}

cmd_pipeline_jobs() {
  local pipeline_id="${1:-}"
  if [[ -z "$pipeline_id" ]]; then
    echo "Error: Pipeline ID required" >&2
    echo "Usage: glab-pipeline.sh pipeline-jobs <pipeline-id>" >&2
    exit 1
  fi

  local project_id
  project_id=$(get_project_id)

  glab api "projects/${project_id}/pipelines/${pipeline_id}/jobs" 2>&1
}

cmd_failed_jobs() {
  local pipeline_id="${1:-}"
  if [[ -z "$pipeline_id" ]]; then
    echo "Error: Pipeline ID required" >&2
    echo "Usage: glab-pipeline.sh failed-jobs <pipeline-id>" >&2
    exit 1
  fi

  local project_id
  project_id=$(get_project_id)

  glab api "projects/${project_id}/pipelines/${pipeline_id}/jobs" 2>&1 | \
    jq -r '.[] | select(.status == "failed") | "\(.name): \(.status) - \(.web_url)"'
}

cmd_job_trace() {
  local job_id="${1:-}"
  if [[ -z "$job_id" ]]; then
    echo "Error: Job ID required" >&2
    echo "Usage: glab-pipeline.sh job-trace <job-id>" >&2
    exit 1
  fi

  local project_id
  project_id=$(get_project_id)

  glab api "projects/${project_id}/jobs/${job_id}/trace" 2>&1
}

cmd_job_info() {
  local job_id="${1:-}"
  if [[ -z "$job_id" ]]; then
    echo "Error: Job ID required" >&2
    echo "Usage: glab-pipeline.sh job-info <job-id>" >&2
    exit 1
  fi

  local project_id
  project_id=$(get_project_id)

  glab api "projects/${project_id}/jobs/${job_id}" 2>&1 | \
    jq '{id, name, status, failure_reason, started_at, finished_at, duration, web_url}'
}

cmd_pipeline_info() {
  local pipeline_id="${1:-}"
  if [[ -z "$pipeline_id" ]]; then
    echo "Error: Pipeline ID required" >&2
    echo "Usage: glab-pipeline.sh pipeline-info <pipeline-id>" >&2
    exit 1
  fi

  local project_id
  project_id=$(get_project_id)

  glab api "projects/${project_id}/pipelines/${pipeline_id}" 2>&1 | \
    jq '{id, status, ref, source, created_at, updated_at, web_url}'
}

# Main dispatch
main() {
  local command="${1:-}"
  shift || true

  case "$command" in
    project-id)
      cmd_project_id "$@"
      ;;
    mr-pipelines)
      cmd_mr_pipelines "$@"
      ;;
    branch-pipelines)
      cmd_branch_pipelines "$@"
      ;;
    pipeline-jobs)
      cmd_pipeline_jobs "$@"
      ;;
    failed-jobs)
      cmd_failed_jobs "$@"
      ;;
    job-trace)
      cmd_job_trace "$@"
      ;;
    job-info)
      cmd_job_info "$@"
      ;;
    pipeline-info)
      cmd_pipeline_info "$@"
      ;;
    help|--help|-h|"")
      usage
      ;;
    *)
      echo "Error: Unknown command '$command'" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
