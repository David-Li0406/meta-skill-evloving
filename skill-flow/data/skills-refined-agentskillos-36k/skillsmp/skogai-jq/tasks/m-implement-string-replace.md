---
name: m-implement-string-replace
branch: feature/m-implement-string-replace
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

Replace pattern in string

Following the established pattern in config/jq-transforms/:
- Create string-replace/transform.jq with jq transformation logic
- Create string-replace/schema.json (input/args/output schemas)
- Create string-replace/test-input.json and test-expected.json
- Add test cases to test.sh
- Follow crud-get/crud-set structure exactly

## Success Criteria

- [ ] string-replace/transform.jq created with proper jq logic
- [ ] string-replace/schema.json created with input/args/output schemas
- [ ] string-replace/test-input.json and test-expected.json created
- [ ] Test cases added to test.sh
- [ ] All tests pass (./test.sh exits 0)
- [ ] Pattern matches existing transformations (crud-get/crud-set)
