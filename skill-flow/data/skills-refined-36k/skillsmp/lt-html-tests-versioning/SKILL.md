---
name: lt-html-tests-versioning
description: Ensure TEST_VERSION is updated whenever creating or editing Lithuanian HTML practice tests under tests/ (including tests/kids/). Use when modifying test content or logic so saved progress invalidation works correctly.
---

# Lt Html Tests Versioning

## Overview

Keep test HTML versions in sync with edits by updating `TEST_VERSION` on every change to test content or behavior.

## Guidelines

- Locate `const TEST_VERSION = "x.y.z";` in the test HTML. If missing, add it next to other top-level constants, matching `template.html`.
- Increment the version any time the test file changes (word lists, gap-fill variants, translations, UI, or logic).
- Use semantic versioning; default to a patch bump (`x.y.z` -> `x.y.(z+1)`) unless the user requests a specific version.
- For larger changes: bump minor for new words/test types, bump major for structural or UX changes.
