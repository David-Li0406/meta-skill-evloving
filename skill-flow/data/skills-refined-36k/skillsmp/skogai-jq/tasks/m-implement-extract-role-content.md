---
name: m-implement-extract-role-content
branch: feature/m-implement-extract-role-content
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

Extract role and content from message

Following the established pattern in config/jq-transforms/:
- Create extract-role-content/transform.jq with jq transformation logic
- Create extract-role-content/schema.json (input/args/output schemas)
- Create extract-role-content/test-input.json and test-expected.json
- Add test cases to test.sh
- Follow crud-get/crud-set structure exactly

## Success Criteria

- [ ] extract-role-content/transform.jq created with proper jq logic
- [ ] extract-role-content/schema.json created with input/args/output schemas
- [ ] extract-role-content/test-input.json and test-expected.json created
- [ ] Test cases added to test.sh
- [ ] All tests pass (./test.sh exits 0)
- [ ] Pattern matches existing transformations (crud-get/crud-set)
