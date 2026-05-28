---
name: green-mirage-audit
description: Use this skill when reviewing test suites to ensure they effectively verify correctness, especially after test runs pass or when questions about test quality arise.
---

# Skill body

## Purpose
This skill is designed for Test Suite Forensic Analysts who need to validate that test suites genuinely catch failures and do not merely pass without meaningful verification.

## Critical Steps
1. **Read Test Files**: Examine every test file line by line.
2. **Trace Execution Path**: Follow the code path from the test through the production code and back to the assertions.
3. **Verify Assertions**: Ensure each assertion would catch actual failures, not just check for the presence of outputs.
4. **Identify Gaps**: Look for scenarios where broken code could still pass the tests.

## Invariant Principles
1. **Passage Not Presence**: The value of a test lies in its ability to catch failures, not merely in passing.
2. **Consumption Validates**: Assertions must actively use outputs (e.g., parse, compile, execute) rather than just checking for existence.
3. **Complete Over Partial**: Full object assertions are necessary to expose potential bugs; partial checks can hide issues.
4. **Trace Before Judge**: Always follow the complete path from test to production before making a judgment on the test's validity.
5. **Evidence-Based Findings**: Every finding must include the exact line number, the specific code fix, and a traced failure scenario.

## Reasoning Schema
Before analyzing any test, follow this step-by-step approach:
1. **CLAIM**: What does the test's name or docstring promise?
2. **PATH**: What code is actually executed?
3. **CHECK**: What do the assertions verify?
4. **ESCAPE**: What could potentially pass this test without being valid?
5. **IMPACT**: What could break in production as a result?

## Reflection
Before concluding your audit:
- Have all tests been traced through the production code?
- Have all patterns been checked for each test?
- Does each finding include: line number, exact fix code, effort, and dependencies?
- Are dependencies between findings clearly identified?
- Is there a YAML block at the start with all required fields?

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| Test files | Yes | The test suite to audit (directory or file paths). |
| Production files | Yes | The source code that the tests are meant to protect. |
| Test run results | No | Recent test output showing pass/fail status. |

## Outputs
| Output | Type | Description |
|--------|------|-------------|
| Audit report | File | A report in YAML + markdown format detailing the audit findings. |