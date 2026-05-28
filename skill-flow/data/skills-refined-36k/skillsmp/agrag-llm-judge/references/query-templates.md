# Query Templates

Use these prompts to evaluate AgRAG across simple, moderate, complex, and negative cases. Mix 5-10 prompts per run.

## Simple
- What tests verify REQ_HANDOVER_001?
- Tests for Authentication feature
- List tests with FAIL result
- Find high priority test cases
- What tests cover function initiate_handover?

## Moderate
- Impact analysis for FILE_src_network_handover_py
- Tests in Handover Tests suite
- Failed tests in Authentication feature
- Tests tagged with regression
- Tests related to error ERR_1000

## Complex
- Coverage for REQ_SIGNALING_010 by component
- Tests for functions in HandoverManager class
- Which feature area has the most failing tests?
- Requirements with no test coverage
- Functions covered by failed authentication tests

## Negative
- Find tests in the 'Deprecated Tests' suite
- Tests for IPv7 protocol support
- Tests verifying REQ_AI_ML_001

Notes:
- Replace IDs if they do not exist in your dataset.
- If you need real IDs, run a quick keyword search first and then reuse those IDs in later prompts.
