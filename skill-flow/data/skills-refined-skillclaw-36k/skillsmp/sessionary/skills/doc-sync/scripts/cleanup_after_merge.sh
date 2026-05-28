#!/bin/bash
#
# PR merge 후 Git 정리 작업
#
# Usage:
#   bash cleanup_after_merge.sh <branch_name>
#
# 수행 작업:
#   1. git fetch origin -p - 원격 브랜치 삭제 상태 반영
#   2. git checkout main - main 브랜치로 이동
#   3. git pull origin main - main 최신화
#   4. git branch -d <branch> - 작업 완료된 로컬 브랜치 삭제

set -e

BRANCH_NAME=$1

if [ -z "$BRANCH_NAME" ]; then
    echo "Usage: bash cleanup_after_merge.sh <branch_name>"
    exit 1
fi

echo "=== Git Cleanup After Merge ==="

# 1. 원격 브랜치 삭제 상태 반영
echo "[1/4] Fetching and pruning remote branches..."
git fetch origin -p

# 2. main으로 checkout
echo "[2/4] Checking out main branch..."
git checkout main

# 3. main 최신화
echo "[3/4] Pulling latest changes from main..."
git pull origin main

# 4. 작업 완료된 로컬 브랜치 삭제
echo "[4/4] Deleting local branch: $BRANCH_NAME"
if git branch --list "$BRANCH_NAME" | grep -q "$BRANCH_NAME"; then
    git branch -d "$BRANCH_NAME"
    echo "Successfully deleted local branch: $BRANCH_NAME"
else
    echo "Branch '$BRANCH_NAME' does not exist locally (already deleted or never created)"
fi

echo ""
echo "=== Cleanup completed successfully ==="
echo "Current branch: $(git rev-parse --abbrev-ref HEAD)"
echo "Latest commit: $(git log -1 --oneline)"
