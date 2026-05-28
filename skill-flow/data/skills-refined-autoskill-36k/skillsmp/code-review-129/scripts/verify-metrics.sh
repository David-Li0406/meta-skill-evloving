#!/bin/bash
# Verify code review metrics are collected correctly from /tmp/metrics_code-review.sh

set -e

TARGET_FILE="/tmp/metrics_code-review.sh"

if [[ ! -f "$TARGET_FILE" || ! -r "$TARGET_FILE" ]]; then
 echo "Error: '$TARGET_FILE' not available."
 echo "Be sure to use the script from the code-review skill."
 exit 1
fi

REQUIRED_VARS=("REPO_NAME" "REPO_URL" "CURRENT_BRANCH" "CREATED_BY" "EMAIL" "CHANGESET_SUMMARY" "CODE_REVIEW_SUMMARY" "FILES_CHANGED" "LINES_ADDED" "LINES_DELETED" "CRITICAL_ISSUES_COUNT" "HIGH_PRIORITY_ISSUES_COUNT" "ESTIMATION_MODEL" "ESTIMATED_HOURS")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
  # 使用grep检查变量定义（支持简单的赋值形式）
  # 查找形如 VAR=、VAR= VALUE、readonly VAR=等形式的定义
  if ! grep -qE "^[[:space:]]*(declare[[:space:]]+)?(readonly[[:space:]]+)?$var[[:space:]]*=" "$TARGET_FILE"; then
      MISSING_VARS+=("$var")
  fi
done

if [[ ${#MISSING_VARS[@]} -eq 0 ]]; then
    echo "✅ Metrics collected correctly."
    exit 0
else
    echo "Metrics not collected correctly. The following variables are undefined:"
    printf "%s," "${MISSING_VARS[@]}" | sed 's/,$//'
    echo ""
    echo "Be sure to use the script from the code-review skill."
    exit 1
fi