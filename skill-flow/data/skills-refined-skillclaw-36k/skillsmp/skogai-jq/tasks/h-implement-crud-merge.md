---
name: h-implement-crud-merge
branch: feature/h-implement-crud-merge
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

Deep merge two objects

Following the established pattern in config/jq-transforms/:
- Create crud-merge/transform.jq with jq transformation logic
- Create crud-merge/schema.json (input/args/output schemas)
- Create crud-merge/test-input.json and test-expected.json
- Add test cases to test.sh
- Follow crud-get/crud-set structure exactly

## Success Criteria

- [ ] crud-merge/transform.jq created with proper jq logic
- [ ] crud-merge/schema.json created with input/args/output schemas
- [ ] crud-merge/test-input.json and test-expected.json created
- [ ] Test cases added to test.sh
- [ ] All tests pass (./test.sh exits 0)
- [ ] Pattern matches existing transformations (crud-get/crud-set)
