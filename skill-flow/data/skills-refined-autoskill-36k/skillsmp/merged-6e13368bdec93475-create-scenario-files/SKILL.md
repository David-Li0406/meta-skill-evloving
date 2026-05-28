---
name: create-scenario-files
description: Use this skill to create test scenario JSON files for Output SDK workflows, enabling consistent testing and validation of workflows during development and after migration.
---

# Creating Scenario Files for Workflow Testing

## Overview

This skill documents how to create test scenario JSON files for Output SDK workflows. Scenario files provide predefined inputs for testing workflows, ensuring consistent validation and debugging.

## When to Use This Skill

- After migrating workflows to set up test inputs.
- During development to document expected behaviors and create regression tests.
- To add new test cases or debug workflow behavior with specific inputs.

## Scenario File Basics

### Location

Scenario files are stored in a `scenarios/` subfolder within the workflow directory:

```
src/workflows/{workflow-name}/
├── workflow.ts
├── steps.ts
├── types.ts
└── scenarios/
    ├── basic_input.json
    ├── edge_case_empty.json
    └── full_options.json
```

### File Format

Scenario files are JSON files that match the workflow's input schema:

```json
{
  "fieldName": "value",
  "optionalField": "optional value",
  "numericField": 42,
  "arrayField": ["item1", "item2"]
}
```

### Naming Convention

Use descriptive names that indicate the test case, following `snake_case`:

```
basic_input.json           # Standard happy path
edge_case_empty.json       # Empty or minimal input
complex_input.json         # Full-featured input with all options
error_missing_field.json   # Missing required field (for error testing)
```

## Creating Scenario Files

### Step 1: Understand Input Schema

Review the workflow's input schema in `types.ts` to ensure your scenario files match the expected structure.

### Step 2: Create scenarios/ Directory

```bash
mkdir -p src/workflows/{workflow-name}/scenarios
```

### Step 3: Create Basic Scenario

Start with a minimal valid input:

```json
{
  "userId": "test-user-001",
  "reportType": "daily"
}
```

### Step 4: Create Additional Scenarios

**Full Options Scenario:**

```json
{
  "userId": "test-user-001",
  "reportType": "weekly",
  "options": {
    "includeCharts": true,
    "maxPages": 5
  }
}
```

**Edge Case - Empty Optional:**

```json
{
  "userId": "test-user-002",
  "reportType": "monthly",
  "options": {}
}
```

## Running Workflows with Scenarios

Use the Output CLI to run a workflow with a scenario file:

```bash
npx output workflow run <workflow_name> --input src/<workflow>/scenarios/<scenario>.json
```

### Example Commands

```bash
npx output workflow run my_workflow --input src/workflows/my_workflow/scenarios/basic_input.json
```

## Scenario Categories

### 1. Happy Path Scenarios

Test normal, expected usage:

```json
{
  "userId": "user-12345",
  "action": "process"
}
```

### 2. Edge Case Scenarios

Test boundary conditions:

```json
{
  "userId": "",
  "action": "validate"
}
```

### 3. Error Scenarios

Test error handling (may cause expected failures):

```json
{
  "userId": 12345,
  "action": "process"
}
```

### 4. Complex Scenarios

Test complex inputs:

```json
{
  "userId": "user-001",
  "documents": [
    {
      "id": "doc-1",
      "title": "First Document",
      "content": "Content of first document"
    }
  ],
  "options": {
    "processAll": true,
    "outputFormat": "json"
  }
}
```

## Best Practices

- Document the purpose of each scenario within the JSON file.
- Use realistic data that matches real use cases.
- Cover all enum values and include variations of optional fields.

## Verification Checklist

- [ ] Scenario file located in `scenarios/` folder inside workflow directory.
- [ ] File uses `.json` extension and follows naming conventions.
- [ ] JSON is valid and matches the input schema.
- [ ] Workflow runs successfully with the scenario.

## Related Skills

- `output-dev-types-file` - Defining inputSchema that scenarios must match.
- `output-workflow-run` - Running workflows with scenario files.
- `output-workflow-list` - Finding available workflows.