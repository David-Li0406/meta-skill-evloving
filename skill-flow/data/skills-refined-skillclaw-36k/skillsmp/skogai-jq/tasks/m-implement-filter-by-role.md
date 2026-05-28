---
name: m-implement-filter-by-role
branch: feature/m-implement-filter-by-role
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

Filter messages by role

Following the established pattern in config/jq-transforms/:
- Create filter-by-role/transform.jq with jq transformation logic
- Create filter-by-role/schema.json (input/args/output schemas)
- Create filter-by-role/test-input.json and test-expected.json
- Add test cases to test.sh
- Follow crud-get/crud-set structure exactly

## Success Criteria

- [ ] filter-by-role/transform.jq created with proper jq logic
- [ ] filter-by-role/schema.json created with input/args/output schemas
- [ ] filter-by-role/test-input.json and test-expected.json created
- [ ] Test cases added to test.sh
- [ ] All tests pass (./test.sh exits 0)
- [ ] Pattern matches existing transformations (crud-get/crud-set)
