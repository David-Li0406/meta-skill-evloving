---
name: lt-html-tests-runner
description: Run targeted Playwright checks for Lithuanian HTML practice tests in /mnt/c/Programming/Projects/Pets/eduardmikhailau.github.io. Use when the user says “run tests” or after adding/editing HTML files under tests/ (including tests/kids/). Use git diff to detect changed HTML tests and run only those by default; run the full suite only when explicitly requested.
---

# Lt Html Tests Runner

## Overview

Run targeted Playwright checks for changed HTML test pages, using git diff to detect which tests changed. Use the full suite only when explicitly requested.

## Workflow

1. Work from repo root: `/mnt/c/Programming/Projects/Pets/eduardmikhailau.github.io`.
2. Detect changed HTML test files via git:
   - `git diff --name-only`
   - `git diff --name-only --cached`
   - `git ls-files --others --exclude-standard`
   - Filter to `tests/**/*.html`.
3. If HTML tests changed, validate only those files, then run only those tests with Playwright:
   - `node scripts/validate-html-tests.mjs <relative path> [more paths...]`
   - `npx playwright test tests/all-tests.spec.js -g "<relative path>"`
   - Run the Playwright command once per changed HTML file (preserve relative path under `tests/`).
4. If no HTML tests changed but the user explicitly asked to run tests, run the full suite:
   - `npm run test:html`
5. Report results: pass/fail summary and any failing file/errors.
6. Optional full validation (only if user explicitly asks for full validation):
   - `node scripts/validate-html-tests.mjs`
