#!/bin/bash
# Retrieve data from different temporary file paths based on which task, and report it to the remote API endpoint.

set -e

is_absolute_call() {
  if [[ "$0" == /* ]]; then
    IS_ABSOLUTE_CALL="true"
  else
    IS_ABSOLUTE_CALL="false"
  fi
}

is_absolute_call

if [[ "$IS_ABSOLUTE_CALL" == "false" ]]; then
  echo "Please call this script using an absolute path"
  exit 1
fi

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Error: At least one parameter 'task' are required"
  exit 1
fi

TASK=$1
COLLECT_COMMIT_ID=$2

FILE_PATH=""
REPO_NAME=$(basename -s .git "$(git config --get remote.origin.url)")
case "$TASK" in
  "code-review")
    FILE_PATH="/tmp/metrics_code-review_${REPO_NAME:-unknown}.sh"
    ;;
  "create-unit-test")
    FILE_PATH="/tmp/metrics_unit-test_${REPO_NAME:-unknown}.sh"
    ;;
  *)
    echo "Error: Unknown task '$TASK'. Available tasks: code-review, create-unit-test"
    exit 1
    ;;
esac

echo "Task: '$TASK'"

if [ ! -f "$FILE_PATH" ]; then
  echo "Error: the file '$FILE_PATH' does not exist."
  exit 1
fi

CHAR_COUNT=$(cat "$FILE_PATH" | wc -c)

if [ "$CHAR_COUNT" -le 1 ]; then
  echo "Error: The file '$FILE_PATH' exists, but its content is empty."
  exit 1
fi

echo "File path to be retrieved: '$FILE_PATH'"

# Source variables from the temporary file
source $FILE_PATH

if [ "$COLLECT_COMMIT_ID" = "true" ]; then
  COMMIT_ID=$(git rev-parse --short=7 HEAD)
  echo "Commit ID captured: ${COMMIT_ID}"
fi

# Create the JSON payload
REPORT_JSON=$(cat <<END_JSON
{
  "taskName": "$CHANGESET_SUMMARY",
  "repoName": "$REPO_NAME",
  "repoUrl": "$REPO_URL",
  "createdBy": "$CREATED_BY",
  "email": "$EMAIL",
  "filesChanged": "$FILES_CHANGED",
  "linesAdded": "$LINES_ADDED",
  "linesDeleted": "$LINES_DELETED",
  "criticalIssues": "$CRITICAL_ISSUES_COUNT",
  "highPriorityIssues": "$HIGH_PRIORITY_ISSUES_COUNT",
  "codeReviewSummary": "$CODE_REVIEW_SUMMARY",
  "estimationModel": "$ESTIMATION_MODEL",
  "estimatedHours": "$ESTIMATED_HOURS",
  "commitId": "$COMMIT_ID"
}
END_JSON
)

# Send the report to the API endpoint
RESPONSE=$(curl --max-time 3 -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$REPORT_JSON" "$webhook_url" 2>/dev/null)

# Extract HTTP code and body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check if the request was successful
if echo "$BODY" | grep -q '"code":200'; then
  echo "✅ Successfully reported metrics, clear the file '$FILE_PATH'"
  echo '' > $FILE_PATH
  exit 0
else
  echo "Error: Failed to report metrics. HTTP Status: $HTTP_CODE, Response: $BODY"
  exit 1
fi