# Requirement Analysis Guide

Extract requirements from Gherkin scenarios and map to test cases with hierarchical numbering.

## 4-Step Analysis Process

### 1. Parse Gherkin Scenarios

- **Given**: Preconditions, **When**: Actions, **Then**: Expected outcomes, **And**: Additional steps
- Analyze if multiple "And" clauses = separate requirements or combined verification

### 2. Extract Requirements

- Specific and measurable
- Starts with what "should" happen
- Avoid vague language ("works correctly")
- One testable aspect per requirement

### 3. Identify Combination Opportunities

**✅ Combine:** Natural workflow, redundant setup if separate, multi-aspect verification of same interaction, maintainable  
**❌ Separate:** Different paths, different preconditions, independent failures, error vs success conditions

### 4. Map to Test Cases

Hierarchical numbering: `Scenario.Requirement.TestCase` (e.g., 1.1.1, 1.2.1, 2.1.1)

## Output Format

### Requirements Analysis Table

Scenario → Requirement → Test Case traceability

**Format:**

- Empty cells (`|  |`) continue same scenario/requirement
- Empty row (`|`) separates scenarios
- Number hierarchically: Scenario (1, 2), Requirement (1.1, 1.2), Test Case (1.1.1, 1.1.2)

### Detailed Test Cases Table

**⚠️ CRITICAL: One row per test case ID (x.y.z) from Requirements Analysis**

This table must have exactly the same number of rows as the "Total Test Cases" count in your Requirements Analysis table. Each test case ID (1.1.1, 1.2.1, 2.1.1, etc.) gets its own individual row.

**Format:**

```
| Test Case ID | Test Scenario | Expected Result | Test Data |
|--------------|---------------|-----------------|-----------|
| 1.1.1 | [Action to test first requirement of scenario 1] | [Expected outcome] | [Data needed or N/A] |
| 1.2.1 | [Action to test second requirement of scenario 1] | [Expected outcome] | [Data needed or N/A] |
| 2.1.1 | [Action to test first requirement of scenario 2] | [Expected outcome] | [Data needed or N/A] |
| 2.2.1 | [Action to test second requirement of scenario 2] | [Expected outcome] | [Data needed or N/A] |
```

**Columns explained:**

- **Test Case ID:** Hierarchical ID from Requirements Analysis (x.y.z format)
- **Test Scenario:** Specific action or verification being performed
- **Expected Result:** What should happen when the test is executed
- **Test Data:** Prerequisites, test data needed, or "N/A" if none required

### Test Coverage Summary

**Metrics:**

- Total Scenarios (count)
- Total Requirements (x.y format count)
- Total Test Cases (x.y.z format count) = Detailed Test Cases row count
- CSV Test Cases (count, may be less due to CSV combination)

## Complete Working Examples

**📁 ALWAYS reference these example files in `.claude/skills/testcase-creator/examples/` when generating requirement analysis:**

### Example Files:

1. **eNr_118557_Welcome-Log_In_Screen-Forms-Based-Authentication.RequirementAnalysis.txt**
   - 11 scenarios → 35 requirements → 35 test case IDs → 11 CSV test cases
   - Demonstrates: Forms-based authentication, license detection, multiple welcome screen variants, device clearing messages

2. **eNr_121265_workspace-screen-share.RequirementAnalysis.txt**
   - 13 scenarios → 43 requirements → 43 test case IDs → 13 CSV test cases
   - Demonstrates: Complex multi-scenario feature, modal interactions, state management

3. **eNr_122019_encounter_refresh-user-directory-participants-tab.RequirementAnalysis.txt**
   - 7 scenarios → 26 requirements → 26 test case IDs → 12 CSV test cases
   - Demonstrates: Tab navigation, user filtering, guest user workflows

4. **eNr_124798_app-loading-behavior.RequirementAnalysis.txt**
   - 3 scenarios → 11 requirements → 11 test case IDs → 4 CSV test cases
   - Demonstrates: Time-based behavior, retry logic, error handling, system state verification

**These examples show:**

- Correct Requirements Analysis table format with empty cells and separators
- Proper hierarchical numbering (x.y.z format)
- One row per test case ID in Detailed Test Cases table
- Test Coverage Summary with accurate counts
- How to analyze "And" clauses for combination vs separation decisions
- Requirements-to-CSV test case mapping strategies

## Decision Guidelines

**Multiple "And" Clauses:**

- Same action/load verification? → Combine
- Independent features? → Separate
- Maintainable combined? → If yes, combine

**Conditional Scenarios:** Different preconditions (license types, roles, flags) → Separate

**Navigation:** Simple nav + destination → Combine | Complex multi-step → Break into checkpoints

## Quality Checklist

- [ ] All scenarios represented
- [ ] Requirements testable and specific
- [ ] Hierarchical numbering (x.y.z)
- [ ] Detailed Test Cases: one row per test case ID
- [ ] Total Test Cases count = Detailed Test Cases rows
- [ ] Tables formatted with empty cells/separators
