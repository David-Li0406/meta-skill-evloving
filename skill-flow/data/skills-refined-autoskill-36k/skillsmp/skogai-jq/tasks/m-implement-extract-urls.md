---
name: m-implement-extract-urls
branch: feature/m-implement-extract-urls
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

Extract all URLs from content

Following the established pattern in config/jq-transforms/:
- Create extract-urls/transform.jq with jq transformation logic
- Create extract-urls/schema.json (input/args/output schemas)
- Create extract-urls/test-input.json and test-expected.json
- Add test cases to test.sh
- Follow crud-get/crud-set structure exactly

## Success Criteria

- [ ] extract-urls/transform.jq created with proper jq logic
- [ ] extract-urls/schema.json created with input/args/output schemas
- [ ] extract-urls/test-input.json and test-expected.json created
- [ ] Test cases added to test.sh
- [ ] All tests pass (./test.sh exits 0)
- [ ] Pattern matches existing transformations (crud-get/crud-set)
