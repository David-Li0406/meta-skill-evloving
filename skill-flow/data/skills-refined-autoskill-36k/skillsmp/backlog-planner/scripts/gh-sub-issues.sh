#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  gh-sub-issues.sh list <parent-issue-number> [--repo OWNER/REPO] [--limit N]
  gh-sub-issues.sh add <parent-issue-number> <child-issue-number...> [--repo OWNER/REPO]
  gh-sub-issues.sh remove <parent-issue-number> <child-issue-number...> [--repo OWNER/REPO]

Notes:
  - Requires gh CLI auth and GitHub sub-issues support in the repo.
  - If the API is not available, use a checklist in the epic issue instead.
USAGE
}

die() {
  echo "Error: $*" >&2
  exit 1
}

require_gh() {
  command -v gh >/dev/null 2>&1 || die "gh CLI is required."
}

get_repo() {
  local repo="${1:-}"
  if [[ -z "$repo" ]]; then
    repo=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)
  fi
  [[ -n "$repo" ]] || die "Repo not detected. Use --repo OWNER/REPO."
  echo "$repo"
}

issue_id() {
  local owner="$1" name="$2" number="$3"
  local query id
  query='query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){issue(number:$number){id}}}'
  id=$(gh api graphql -f query="$query" -F owner="$owner" -F name="$name" -F number="$number" \
    --jq '.data.repository.issue.id')
  if [[ -z "$id" || "$id" == "null" ]]; then
    return 0
  fi
  echo "$id"
}

list_sub_issues() {
  local owner="$1" name="$2" parent="$3" limit="$4"
  local query lines status
  query='query($owner:String!,$name:String!,$number:Int!,$limit:Int!){repository(owner:$owner,name:$name){issue(number:$number){subIssues(first:$limit){nodes{number title}}}}}'
  set +e
  lines=$(gh api graphql -f query="$query" -F owner="$owner" -F name="$name" -F number="$parent" -F limit="$limit" \
    --jq '.data.repository.issue.subIssues.nodes[] | "#\(.number) \(.title)"' 2>/dev/null)
  status=$?
  set -e
  if [[ $status -ne 0 ]]; then
    die "Sub-issues API not available for this repo."
  fi
  if [[ -z "$lines" ]]; then
    echo "No sub-issues."
  else
    printf '%s\n' "$lines"
  fi
}

add_sub_issues() {
  local owner="$1" name="$2" parent="$3"; shift 3
  local parent_id child_number child_id query
  parent_id=$(issue_id "$owner" "$name" "$parent")
  [[ -n "$parent_id" ]] || die "Parent issue not found."
  query='mutation($issueId:ID!,$subIssueId:ID!){addSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId}){issue{id}}}'
  for child_number in "$@"; do
    child_id=$(issue_id "$owner" "$name" "$child_number")
    [[ -n "$child_id" ]] || die "Child issue not found: $child_number"
    gh api graphql -f query="$query" -f issueId="$parent_id" -f subIssueId="$child_id" >/dev/null
    echo "Added sub-issue #$child_number -> #$parent"
  done
}

remove_sub_issues() {
  local owner="$1" name="$2" parent="$3"; shift 3
  local parent_id child_number child_id query
  parent_id=$(issue_id "$owner" "$name" "$parent")
  [[ -n "$parent_id" ]] || die "Parent issue not found."
  query='mutation($issueId:ID!,$subIssueId:ID!){removeSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId}){issue{id}}}'
  for child_number in "$@"; do
    child_id=$(issue_id "$owner" "$name" "$child_number")
    [[ -n "$child_id" ]] || die "Child issue not found: $child_number"
    gh api graphql -f query="$query" -f issueId="$parent_id" -f subIssueId="$child_id" >/dev/null
    echo "Removed sub-issue #$child_number from #$parent"
  done
}

main() {
  require_gh
  local cmd="" repo="" limit="50"
  local args=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      list|add|remove) cmd="$1"; shift ;;
      --repo)
        if [[ $# -lt 2 || "$2" == -* ]]; then
          die "--repo requires OWNER/REPO."
        fi
        repo="$2"; shift 2 ;;
      --limit)
        if [[ $# -lt 2 || "$2" == -* ]]; then
          die "--limit requires a number."
        fi
        limit="$2"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) args+=("$1"); shift ;;
    esac
  done

  [[ -n "$cmd" ]] || { usage; exit 1; }
  [[ ${#args[@]} -ge 1 ]] || { usage; exit 1; }

  repo=$(get_repo "$repo")
  local owner="${repo%/*}" name="${repo#*/}"

  case "$cmd" in
    list)
      list_sub_issues "$owner" "$name" "${args[0]}" "$limit"
      ;;
    add)
      [[ ${#args[@]} -ge 2 ]] || die "add requires parent and one or more child issue numbers."
      add_sub_issues "$owner" "$name" "${args[0]}" "${args[@]:1}"
      ;;
    remove)
      [[ ${#args[@]} -ge 2 ]] || die "remove requires parent and one or more child issue numbers."
      remove_sub_issues "$owner" "$name" "${args[0]}" "${args[@]:1}"
      ;;
  esac
}

main "$@"
