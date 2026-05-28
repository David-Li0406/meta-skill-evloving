#!/bin/bash
# Get basic repo info: owner, name, default branch

OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')

echo "{\"owner\": \"$OWNER\", \"repo\": \"$REPO\", \"defaultBranch\": \"$DEFAULT_BRANCH\"}"
