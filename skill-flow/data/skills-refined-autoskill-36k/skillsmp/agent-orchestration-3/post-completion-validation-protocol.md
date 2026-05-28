---
title: "Post-Completion Validation Protocol"
purpose: "Orchestrator guidance for verifying sub-agent task completion by commit type"
source: "Synthesized from am-i-complete.md and is-it-done.md"
version: "1.0.0"
last_updated: "2025-11-15"
---

# Post-Completion Validation Protocol

The orchestrator must NOT accept sub-agent completion claims without type-specific verification evidence.

## Core Principle

EXIT_CODE_0_DEFINITION:

- Command executed without uncaught exception
- Process terminated normally (not crashed)
- NOT proof program achieved functional goal
- NOT proof output is correct
- NOT proof behavior is expected

COMPLETION_DEFINITION:

- "works" = executes AND produces expected behavior in ALL functional scenarios
- "fixed" = original problem NO LONGER occurs when tested in realistic scenario
- NOT "passes linters" or "compiles without errors"

## Verification Checklist by Commit Type

### fix: Bug Fix Verification

TRIGGER: Sub-agent claims bug fix complete

VERIFICATION_CHECKLIST:

1. Require proof bug reproduced before fix
   - "Show test that failed before fix"
   - Failing test output required
2. Require proof same test now passes
   - "Show same test passing after fix"
   - Passing test output required
3. Require edge case testing evidence
   - "Show error handling scenarios tested"
   - Terminal output of edge case tests
4. Require regression test suite results
   - "Show full test suite still passes"
   - Complete test run output

REJECTION_CRITERIA:

- Agent claims "bug should be fixed" without before/after proof
- Agent shows only compilation success
- Agent provides try-except wrapper without root cause investigation
- Agent skips regression test suite execution

REQUIRED_EVIDENCE:

- Terminal output showing test failure before fix
- Same test passing after fix
- Full test suite results demonstrating no regressions
- Edge case test results

SOURCE: am-i-complete.md lines 28-121, is-it-done.md lines 39-47

### feat: Feature Addition Verification

TRIGGER: Sub-agent claims feature implementation complete

VERIFICATION_CHECKLIST:

1. Require end-to-end demonstration
   - "Show feature working in intended context"
   - Complete user workflow demonstration
2. Require ALL acceptance criteria verification
   - "Prove each acceptance criterion met"
   - Evidence for each criterion
3. Require edge case testing evidence
   - "Show error handling scenarios"
   - "Show input validation working"
4. Require integration testing proof
   - "Show feature integrates with existing functionality"
   - Integration test results

REJECTION_CRITERIA:

- Agent claims "feature implemented" without E2E demonstration
- Agent shows only unit tests passing
- Agent demonstrates happy path only
- Agent provides theoretical explanation instead of execution proof

REQUIRED_EVIDENCE:

- Terminal output of complete feature workflow
- Test results covering unit, integration, and E2E levels
- Edge case and error handling demonstrations
- Proof all acceptance criteria met

SOURCE: am-i-complete.md lines 125-217, is-it-done.md lines 49-56

### refactor: Code Restructuring Verification

TRIGGER: Sub-agent claims refactoring complete

VERIFICATION_CHECKLIST:

1. Require proof tests passed before refactoring
   - "Show baseline test results before changes"
   - Pre-refactor test suite output
2. Require proof tests still pass after refactoring
   - "Show same tests passing after changes"
   - Post-refactor test suite output
3. Require proof behavior unchanged
   - "Show functional equivalence evidence"
   - Before/after output comparison
4. Require proof performance not degraded
   - "Show performance metrics if applicable"
   - Performance test results if relevant

REJECTION_CRITERIA:

- Agent claims "refactoring complete" without before/after test evidence
- Agent shows only linter passing
- Agent cannot prove behavior unchanged
- Agent introduces new test failures
- Agent refactored code lacking tests without adding them first

REQUIRED_EVIDENCE:

- Baseline test results before refactoring
- Same test results after refactoring
- Proof all tests still pass
- Performance metrics if applicable

SOURCE: am-i-complete.md lines 220-274, is-it-done.md lines 58-64

### docs: Documentation Change Verification

TRIGGER: Sub-agent claims documentation complete

VERIFICATION_CHECKLIST:

1. Require proof all code examples execute
   - "Show all code snippets running successfully"
   - Terminal output for each example
2. Require proof all commands/instructions work
   - "Show each command executing as documented"
   - Command execution output
3. Require proof links and references are valid
   - "Show all links accessible"
   - Link validation results
4. Require proof documentation is followable
   - "Show step-by-step execution following docs"
   - Complete workflow following documentation

REJECTION_CRITERIA:

- Agent claims "docs updated" without testing examples
- Agent provides untested code snippets
- Agent includes broken links
- Agent documentation contains unverified commands
- Agent cannot demonstrate docs are followable

REQUIRED_EVIDENCE:

- Terminal output of all code examples executing
- Command execution results
- Link validation results
- Proof documentation workflow is complete and accurate

SOURCE: is-it-done.md lines 66-71

### test: Test Addition/Modification Verification

TRIGGER: Sub-agent claims test suite changes complete

VERIFICATION_CHECKLIST:

1. Require proof tests execute
   - "Show test suite running"
   - Complete test execution output
2. Require proof tests fail appropriately for negative cases
   - "Show tests catching expected failures"
   - Failing test output for deliberate failures
3. Require proof tests cover stated scenarios
   - "Show coverage report if applicable"
   - Evidence each scenario is tested
4. Require proof tests are in correct location
   - "Show tests follow project structure"
   - File paths matching conventions

REJECTION_CRITERIA:

- Agent claims "tests added" without execution proof
- Agent shows only test file creation
- Agent cannot demonstrate tests catch failures
- Agent places tests in incorrect locations
- Agent tests pass without testing actual functionality

REQUIRED_EVIDENCE:

- Terminal output of test suite execution
- Test results showing appropriate pass/fail scenarios
- Coverage metrics if applicable
- File structure showing correct test placement

SOURCE: am-i-complete.md lines 311-320, is-it-done.md lines 83-91

### chore: Maintenance Task Verification

TRIGGER: Sub-agent claims maintenance task complete

VERIFICATION_CHECKLIST:

1. Require proof task executed successfully
   - "Show command/operation output"
   - Terminal output of operation
2. IF dependency_update THEN
   - Require proof project still builds
   - Require proof tests still pass
   - Show build and test output
3. IF config_change THEN
   - Require proof configuration loads
   - Require proof system functions with new config
   - Show validation output
4. IF cleanup_task THEN
   - Require proof removed items no longer referenced
   - Require proof no broken dependencies
   - Show verification results

REJECTION_CRITERIA:

- Agent claims "maintenance complete" without execution proof
- Agent updates dependencies without running tests
- Agent changes configuration without validation
- Agent removes code without checking references

REQUIRED_EVIDENCE:

- Terminal output of maintenance operation
- Build and test results if applicable
- Configuration validation if applicable
- Reference check results if cleanup performed

SOURCE: is-it-done.md lines 80-91

### perf: Performance Improvement Verification

TRIGGER: Sub-agent claims performance optimization complete

VERIFICATION_CHECKLIST:

1. Require proof baseline performance measured
   - "Show before-optimization metrics"
   - Baseline benchmark results
2. Require proof after-optimization metrics
   - "Show after-optimization metrics"
   - Post-optimization benchmark results
3. Require proof improvement quantified
   - "Show percentage improvement or metric delta"
   - Comparison of before/after
4. Require proof functionality preserved
   - "Show all tests still pass"
   - Test suite results

REJECTION_CRITERIA:

- Agent claims "performance improved" without before/after metrics
- Agent provides estimated improvement instead of measured
- Agent breaks functionality for performance gains
- Agent cannot quantify improvement

REQUIRED_EVIDENCE:

- Baseline performance metrics
- Post-optimization performance metrics
- Quantified improvement (percentage, time saved, etc.)
- Test suite results proving functionality intact

SOURCE: is-it-done.md lines 109-120

### ci: CI/CD Pipeline Change Verification

TRIGGER: Sub-agent claims CI/CD changes complete

VERIFICATION_CHECKLIST:

1. Require proof pipeline executes
   - "Show pipeline run output"
   - Complete pipeline execution log
2. Require proof all stages pass
   - "Show each stage result"
   - Stage-by-stage results
3. Require proof changes handle both success AND failure cases
   - "Show pipeline behavior on intentional failure"
   - Failure handling demonstration
4. Require proof changes integrate with existing workflow
   - "Show end-to-end workflow execution"
   - Complete workflow results

REJECTION_CRITERIA:

- Agent claims "pipeline updated" without execution proof
- Agent shows only configuration file changes
- Agent tests only success path
- Agent cannot demonstrate failure handling

REQUIRED_EVIDENCE:

- Complete pipeline execution output
- Results for all pipeline stages
- Failure case handling demonstration
- Integration with existing workflow proof

SOURCE: is-it-done.md lines 74-79

### build: Build System Change Verification

TRIGGER: Sub-agent claims build system changes complete

VERIFICATION_CHECKLIST:

1. Require proof build executes successfully
   - "Show complete build output"
   - Full build log
2. Require proof build artifacts are valid
   - "Show artifact validation"
   - Artifact inspection results
3. Require proof clean build works
   - "Show build from clean state"
   - Clean build output
4. Require proof all build targets function
   - "Show each build target executing"
   - Results for each target

REJECTION_CRITERIA:

- Agent claims "build system updated" without build execution
- Agent shows only configuration changes
- Agent cannot demonstrate clean build
- Agent tests only default build target

REQUIRED_EVIDENCE:

- Complete build output
- Artifact validation results
- Clean build results
- All build targets execution proof

SOURCE: is-it-done.md lines 74-79

### style: Code Formatting/Style Verification

TRIGGER: Sub-agent claims style changes complete

VERIFICATION_CHECKLIST:

1. Require proof linters pass
   - "Show linter output"
   - Linter results
2. Require proof formatters applied
   - "Show formatter execution output"
   - Formatter results
3. Require proof tests still pass
   - "Show test suite results"
   - Test execution output
4. Require proof no functional changes introduced
   - "Show diff contains only style changes"
   - Git diff or equivalent

REJECTION_CRITERIA:

- Agent claims "style updated" without linter execution
- Agent makes functional changes in style commit
- Agent breaks tests with formatting changes
- Agent cannot demonstrate only style changed

REQUIRED_EVIDENCE:

- Linter output showing compliance
- Formatter execution results
- Test suite results
- Diff showing only style changes

SOURCE: is-it-done.md lines 83-91

### revert: Revert Previous Commit Verification

TRIGGER: Sub-agent claims revert complete

VERIFICATION_CHECKLIST:

1. Require proof original commit identified
   - "Show commit hash and message being reverted"
   - Git log or equivalent
2. Require proof revert applied cleanly
   - "Show revert operation output"
   - Revert command results
3. Require proof state matches pre-commit
   - "Show tests that failed after original commit now pass"
   - "Show behavior restored to pre-commit state"
4. Require proof no merge conflicts or issues
   - "Show clean working state"
   - Status check results

REJECTION_CRITERIA:

- Agent claims "reverted" without identifying specific commit
- Agent cannot prove state restored
- Agent leaves merge conflicts unresolved
- Agent reverts without testing result

REQUIRED_EVIDENCE:

- Commit identification (hash, message)
- Revert operation output
- Test results proving state restored
- Clean working state confirmation

SOURCE: is-it-done.md lines 156-164

## General Verification Protocol

TRIGGER: Sub-agent reports completion for any task type

MANDATORY_QUESTIONS:

1. "What evidence can you provide that this ACTUALLY works?"
2. "Have you EXECUTED the code in its intended context?"
3. "Have you OBSERVED the expected behavior?"
4. "Have you TESTED failure scenarios?"
5. "Have you VERIFIED no regressions?"

EVIDENCE_REQUIREMENTS:

- Terminal output showing problem → solution → verification
- NOT "exit code 0"
- NOT "linting passed"
- NOT "it should work"
- NOT paraphrased results

ACCEPTANCE_CRITERIA:

- Orchestrator can reproduce verification steps
- Evidence demonstrates functional success
- All test scenarios covered
- No unintended side effects observed

SOURCE: is-it-done.md lines 93-147

## Red Flags - Automatic Rejection Triggers

TRIGGER: Sub-agent response contains these phrases

REJECT_IF_CONTAINS:

- "It passes all the linters" (NOT verification of functionality)
- "It exits with code 0" (NOT proof it works)
- "The code looks correct" (NOT evidence)
- "It should work" (Agent hasn't tested it)
- "I've updated the code" (But have they verified behavior?)
- "The implementation is complete" (Without execution proof)
- "All changes committed" (Without verification proof)

CORRECT_RESPONSE: "I need to see actual execution evidence. Please provide terminal output showing [specific behavior] working in practice, not compilation/linting success."

SOURCE: is-it-done.md lines 149-155

## Proper Verification Workflow

The orchestrator must ensure sub-agents follow:

1. REPRODUCE the issue/requirement
2. IMPLEMENT the solution
3. VERIFY with actual execution
4. DOCUMENT the evidence
5. CONFIRM no regressions
6. Only THEN claim completion

REJECTION_PATTERN: IF agent_skips_any_step THEN

- REJECT completion claim
- REQUEST missing step execution
- AWAIT evidence before acceptance

SOURCE: is-it-done.md lines 156-164

## Quality Gates Assessment

MINIMUM_VERIFICATION_GATES:

- [ ] Pre-commit hooks passed (if they exist)
- [ ] Unit tests executed and passed
- [ ] Integration tests executed and passed
- [ ] Linting passed (necessary but NOT sufficient)
- [ ] Type checking passed (necessary but NOT sufficient)
- [ ] Manual testing in realistic scenarios completed
- [ ] Evidence collected and provided

The orchestrator must verify ALL gates passed, not just subset.

SOURCE: is-it-done.md lines 80-91

## Evidence Collection Standards

ACCEPTABLE_EVIDENCE:

- Terminal output showing problem reproducing
- Terminal output showing problem fixed
- Test execution results (not just exit codes)
- Actual output/behavior demonstration
- Before/after comparisons
- Error handling verification

UNACCEPTABLE_EVIDENCE:

- Paraphrased results
- "I tested it and it works"
- Exit code alone
- Linting pass alone
- Code review alone
- Agent's assertion without proof

The orchestrator must request acceptable evidence when unacceptable evidence provided.

SOURCE: is-it-done.md lines 93-102

## Orchestrator Response Templates

### When Agent Claims Completion Without Evidence

TEMPLATE: "I cannot accept task completion without verification evidence. Please provide:

1. Terminal output demonstrating [specific behavior]
2. Test execution results (not just pass/fail, actual output)
3. Evidence that [specific acceptance criterion] is met

Please execute the verification steps and share the output."

### When Agent Provides Insufficient Evidence

TEMPLATE: "The evidence provided (linting pass / exit code 0 / 'it should work') is insufficient. I need to see:

1. [Specific behavior] demonstrated in realistic scenario
2. [Specific test] execution output
3. [Specific edge case] handling proof

Please run these scenarios and share terminal output."

### When Agent Provides Complete Evidence

TEMPLATE: "Verification evidence accepted:

- [Specific criterion 1]: ✅ Verified via [evidence]
- [Specific criterion 2]: ✅ Verified via [evidence]
- [Specific criterion 3]: ✅ Verified via [evidence]

Task completion confirmed. Proceeding to [next step]."

## Task-Type Detection Logic

The orchestrator must identify task type from:

- Commit message prefix (fix:, feat:, refactor:, etc.)
- Task description context
- Acceptance criteria nature
- User's original request

IF task_type_ambiguous THEN

- Request clarification from user
- Apply GENERAL_VERIFICATION_PROTOCOL
- Require comprehensive evidence

## Completion Verification Formula

TASK_COMPLETE = ( evidence_execution PROVIDED AND acceptance_criteria_verified AND regression_tests_passed AND edge_cases_tested AND no_red_flags_present )

IF NOT TASK_COMPLETE THEN

- REJECT completion claim
- REQUEST specific missing evidence
- AWAIT re-submission with evidence

## Notes for Orchestrator

The orchestrator must understand:

- Sub-agents may claim completion prematurely (training data pattern)
- Linting/compilation success ≠ functional success
- Agent confidence ≠ actual verification
- "Should work" means "haven't tested"
- Evidence prevents shipping broken functionality

The orchestrator's role is GATEKEEPER preventing unverified completions.

Trust is built through rigorous verification, not optimistic acceptance.
