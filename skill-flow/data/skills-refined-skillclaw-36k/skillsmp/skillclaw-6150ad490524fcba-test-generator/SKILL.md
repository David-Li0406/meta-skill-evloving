---
name: test-generator
description: Use this skill when you need to generate test code from specifications, components, and API endpoints, creating unit tests, integration tests, and E2E tests that follow project testing patterns and conventions.
---

# Skill body

## Step-by-Step Instructions

### Step 1: Identify Test Type
Determine what type of test is needed:
- **Unit Test**: Component/function testing
- **Integration Test**: Service/API integration
- **E2E Test**: Full user flow testing
- **API Test**: Endpoint testing

### Step 2: Analyze Target Code
Examine the code to test:
- Read component/function code
- Identify test cases
- Understand dependencies
- Note edge cases

### Step 3: Analyze Test Patterns
Review existing tests:
- Read similar test files
- Identify testing patterns
- Note testing framework usage
- Understand mocking strategies

### Step 4: Generate Test Code
Create tests following patterns:
- Use the appropriate testing framework
- Follow project conventions
- Include comprehensive coverage
- Add edge cases and error scenarios

### Step 5: Coverage Analysis
After generating tests, analyze coverage:
1. **Check that generated tests cover all requirements**:
   - Verify all functions/methods are tested
   - Check all branches are covered (if/else, switch, etc.)
   - Ensure all edge cases are tested
   - Validate error scenarios are covered

2. **Validate tests are runnable**:
   - Check test syntax is valid
   - Verify imports are correct
   - Ensure the test framework is properly configured
   - Validate test setup/teardown is correct

3. **Report coverage percentage**:
   - Calculate line coverage (if possible)
   - Calculate branch coverage (if possible)
   - Report uncovered code paths
   - Suggest additional tests for uncovered scenarios