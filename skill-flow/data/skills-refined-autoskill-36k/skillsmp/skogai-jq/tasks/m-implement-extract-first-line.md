---
name: m-implement-extract-first-line
branch: feature/m-implement-extract-first-line
status: pending
created: 2025-11-14
submodules: [list of git submodules affected (delete if not super-repo)]
---

# [Human-Readable Title]

## Problem/Goal
[Clear description of what we're solving/building]

## Success Criteria
- [ ] Specific, measurable outcome
- [ ] Another concrete goal

## Context Manifest
<!-- Added by context-gathering agent -->

## User Notes
<!-- Any specific notes or requirements from the developer -->

## Work Log
<!-- Updated as work progresses -->
- [YYYY-MM-DD] Started task, initial research

## Problem/Goal

Get first line of content

Following the established pattern in config/jq-transforms/:
- Create extract-first-line/transform.jq with jq transformation logic
- Create extract-first-line/schema.json (input/args/output schemas)
- Create extract-first-line/test-input.json and test-expected.json
- Add test cases to test.sh
- Follow crud-get/crud-set structure exactly

## Success Criteria

- [ ] extract-first-line/transform.jq created with proper jq logic
- [ ] extract-first-line/schema.json created with input/args/output schemas
- [ ] extract-first-line/test-input.json and test-expected.json created
- [ ] Test cases added to test.sh
- [ ] All tests pass (./test.sh exits 0)
- [ ] Pattern matches existing transformations (crud-get/crud-set)
