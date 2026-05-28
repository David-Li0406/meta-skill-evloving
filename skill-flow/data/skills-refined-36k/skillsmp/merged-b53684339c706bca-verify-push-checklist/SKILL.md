---
name: verify-push-checklist
description: Use this skill when preparing for or verifying the outcome of a push to a remote repository.
---

# Verify Push Checklist

## Overview
CRITICAL: Always verify the following checklist before and after pushing to remote.

## Before Pushing Checklist

- [ ] `npm run build` has run and `./dist/` is up to date
- [ ] Ensure the dist folder is committed

## After Pushing Checklist

- [ ] `npx-test.sh` does not produce failures
- [ ] `npm-install-test.sh` does not produce failures

## Why This Matters
Successful Git pushes do not guarantee that the package works. These checks ensure the package is both built correctly and functional.

## Common Mistakes
- Pushing without committing the built dist folder
- Forgetting to run build before pushing
- Having uncommitted dist changes
- Assuming successful push means package works
- Skipping verification after "git push succeeded"
- Closing work without testing package installation