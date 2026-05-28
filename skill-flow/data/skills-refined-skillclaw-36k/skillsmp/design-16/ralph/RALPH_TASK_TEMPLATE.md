# RALPH State Machine Task

---
mode: state_machine
spec_file: docs/specs/my-feature.spec.md
prp_file: prp/my-feature.prp.md
---

## States

### STRESS_TEST
order: 1
command: |
  ~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh stress-test {{spec_file}}
pass_condition: "Instruction generated"
on_fail: Fix completeness gaps identified in spec, then re-run gate
on_pass: Transition to VALIDATE

### VALIDATE
order: 2
command: |
  ~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh validate {{spec_file}}
pass_condition: "Structure validation passed"
on_fail: Fix ambiguities and clarity issues in spec, then re-run gate
on_pass: Transition to GENERATE_PRP

### GENERATE_PRP
order: 3
command: |
  ~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh generate {{spec_file}}
pass_condition: "generate-instruction.md"
on_fail: Check error output, ensure spec meets validation gates
on_pass: Transition to CHECK_PRP

### CHECK_PRP
order: 4
command: |
  ~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh check {{prp_file}}
pass_condition: "PRP validation passed"
on_fail: Fix PRP structure based on output
on_pass: Transition to GENERATE_TESTS

### GENERATE_TESTS
order: 5
command: |
  ~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh implement {{prp_file}}
pass_condition: "implement-instruction.md"
on_fail: Ensure PRP meets all requirements before test generation
on_pass: Transition to CHECK_TESTS

### CHECK_TESTS
order: 6
command: |
  python -m pytest tests/ --collect-only -q 2>&1
pass_condition: "selected"
on_fail: Tests don't exist, have syntax errors, or don't match PRP criteria
on_pass: Transition to IMPLEMENT

### IMPLEMENT
order: 7
command: |
  python -m pytest tests/ -v --tb=short 2>&1
pass_condition: "passed"
on_fail: Fix code to pass failing tests (ensure ALL tests pass)
on_pass: Transition to COMPLETE

### COMPLETE
order: 8
terminal: true

## GUTTER Configuration

on_gutter: |
  echo ""
  echo "🚨 GUTTER REACHED: Max retries exhausted for state: {{current_state}}"
  echo ""
  echo "Last output saved to: .ralph/gutter-{{current_state}}.log"
  echo "Git diff saved to: .ralph/gutter-diff.patch"
  echo ""
  echo "Steps to recover:"
  echo "  1. Review the issue: cat .ralph/gutter-{{current_state}}.log"
  echo "  2. Fix the problem manually"
  echo "  3. Resume the loop: ./ralph-loop.sh --state-machine --resume -y"
  echo ""
  exit 1
