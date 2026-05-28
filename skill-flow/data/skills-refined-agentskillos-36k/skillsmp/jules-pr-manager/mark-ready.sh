#!/bin/bash
PR_ID=$1
if [ -z "$PR_ID" ]; then echo "PR ID required"; exit 1; fi
gh pr ready "$PR_ID"
