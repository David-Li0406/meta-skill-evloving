# Workflow: Add Test Cases to Existing Test File

<required_reading>
**Read the appropriate reference based on the test file layer:**
- Data layer: references/data-layer-tests.md
- Biz layer: references/biz-layer-tests.md
- Service layer: references/service-layer-tests.md

**Always read**: references/table-driven-tests.md
</required_reading>

<process>
## Step 1: Read Existing Test File

Read the test file to understand:
- Current test structure
- Existing test cases and scenarios covered
- Helper functions available
- Mock patterns used
- Assertion style

## Step 2: Identify Gaps

Determine what scenarios are missing:
- Validation errors not covered
- Edge cases (nil, empty, boundary values)
- Error paths not tested
- Specific business logic branches

Ask user: "What scenarios would you like to add?"

## Step 3: Match Existing Patterns

Follow the exact patterns from existing tests:
- Use same table structure
- Use same helper functions
- Use same mock setup style
- Use same assertion methods
- Match naming conventions

## Step 4: Write New Test Cases

Add new test cases to existing test tables:

```go
{
    name: "descriptive name for new scenario",
    input: // test input,
    setup: func(deps) {
        // mock configuration
    },
    wantErr: true/false,
    checkResult: func(t *testing.T, result) {
        // assertions
    },
},
```

## Step 5: Update Test File

Use Edit tool to add new test cases to the existing test table.

Preserve:
- Existing test structure
- Indentation and formatting
- Import statements
- Helper functions

## Step 6: Run Tests

```bash
cd {service-directory}
make test
```

Verify new test cases pass.
</process>

<success_criteria>
- [ ] Existing test file analyzed
- [ ] Gaps identified
- [ ] New test cases match existing patterns
- [ ] Test cases added to correct test functions
- [ ] `make test` passes with new cases
</success_criteria>