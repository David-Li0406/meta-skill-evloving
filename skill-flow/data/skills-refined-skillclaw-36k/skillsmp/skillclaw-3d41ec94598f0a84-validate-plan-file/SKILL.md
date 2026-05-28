---
name: validate-plan-file
description: Use this skill to validate that orchestrator plan files conform to the expected JSON schema, ensuring proper structure and required fields before processing.
---

# Validate Plan File

Validate orchestrator plan files against expected JSON schema.

## Instructions

### Step 1: Read Plan File
Load the plan file using the Read tool.

### Step 2: Determine Schema
Map the file name to the schema in `.claude/schemas/`:
- `.bug-*-plan.json` → `bug-plan.schema.json`
- `.security-*-plan.json` → `security-plan.schema.json`
- `.dead-code-*-plan.json` → `dead-code-plan.schema.json`
- `.dependency-*-plan.json` → `dependency-plan.schema.json`

### Step 3: Validate Required Fields

**Base schema** (all plans):
- `workflow`: String (required)
- `phase`: String (required)
- `config`: Object (required, domain-specific)
- `validation`: Object (required, with `required` array)
- `nextAgent`: String (optional)
- `timestamp`: String (optional, ISO-8601)
- `metadata`: Object (optional)

**Domain-specific config**:
- **Bug**: `config.priority` (critical|high|medium|low|all)
- **Security**: `config.severity` (critical|high|medium|low|all)
- **Dead Code**: `config.type` (critical|high|medium|low|all)
- **Dependency**: `config.category` (security|unused|outdated|all)

### Step 4: Return Result
Return a JSON object with the validation result:

```json
{
  "valid": true|false,
  "file": "filename",
  "errors": [],
  "warnings": [],
  "schema": "schema-name"
}
```

## Error Handling
- **File Not Found**: Return an error with the path.
- **Invalid JSON**: Return a parsing error.
- **Missing Required Fields**: List all missing fields.
- **Invalid Enum Values**: Report with allowed values.