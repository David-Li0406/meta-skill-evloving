---
name: verify-push-process
description: Use this skill when preparing for and verifying the integrity of code changes before and after pushing to a remote repository.
---

# Skill body

## Overview
CRITICAL: Always verify the following checklist before and after pushing to remote.

## Checklist Before Pushing
- [ ] `npm run build` has run and `./dist/` is up to date
- [ ] Ensure the dist folder is committed

## Checklist After Pushing
- [ ] `npx-test.sh` does not produce failures
- [ ] `npm-install-test.sh` does not produce failures

## Why This Matters
Pushing code to a remote repository does not guarantee that the package works. These checks ensure that the package is both built correctly and functional after the push.

## Common Mistakes
- Pushing without committing the built dist folder
- Forgetting to run build before pushing
- Having uncommitted dist changes
- Assuming successful push means package works
- Skipping verification after "git push succeeded"
- Closing work without testing package installation