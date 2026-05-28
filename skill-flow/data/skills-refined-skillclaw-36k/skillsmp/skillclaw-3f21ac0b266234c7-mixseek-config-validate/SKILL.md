---
name: mixseek-config-validate
description: Use this skill when you need to validate MixSeek configuration files (team.toml, orchestrator.toml, evaluator.toml, judgment.toml) for correctness and compliance with TOML syntax and MixSeek schema.
---

# MixSeek Configuration Validation

## Overview

This skill validates MixSeek configuration files to ensure they comply with TOML syntax and the MixSeek schema. It detects syntax errors, missing required fields, and out-of-range values, providing suggestions for corrections.

## Prerequisites

- MixSeek-Core must be installed.
- The configuration file to be validated must exist.
- Python command must be available (detected using the `detect-python-command` skill).

## Supported File Types

| File Type     | Description                | Example Path                     |
|---------------|----------------------------|----------------------------------|
| team          | Team configuration         | `configs/agents/team-*.toml`    |
| orchestrator  | Orchestrator configuration  | `orchestrator.toml`             |
| evaluator     | Evaluator configuration     | `configs/evaluators/evaluator.toml` |
| judgment      | Judgment configuration      | `configs/judgment/judgment.toml` |

## Usage Instructions

### Step 1: Confirm the File to Validate

Ask the user which file they want to validate:

```
Please specify the file to validate:
- Specific file: configs/agents/team-web-research.toml
- All configurations: All configuration files
```

### Step 2: Execute Validation

Use the `detect-python-command` skill's `run-python.sh` to perform the validation:

```bash
# Validate a specific file
.skills/detect-python-command/scripts/run-python.sh \
    .skills/mixseek-config-validate/scripts/validate-config.py <file-path>

# Validate by specifying file type
.skills/detect-python-command/scripts/run-python.sh \
    .skills/mixseek-config-validate/scripts/validate-config.py <file-path> --type team
```

### Step 3: Report Results

Report the validation results to the user:

- **On Success**: Display the validation items and results.
- **On Failure**: Provide details of the errors and suggestions for corrections.

## Validation Items

### TOML Syntax Validation

- Correctness of basic syntax
- Quoting of strings
- Format of arrays and tables
- Format of comments

### Schema Validation

| Item            | Description                          |
|-----------------|--------------------------------------|
| Required Fields | Check for existence of necessary fields |
| Field Types     | Validate the correct type of values |
| Value Ranges    | Ensure numbers are within allowed ranges |
| Format          | Validate special formats like models |
| Uniqueness      | Check for uniqueness of fields like agent_name |
| Consistency     | Ensure conditions like min_rounds <= max_rounds |

## Example

### Validating a Single File

```
User: Validate team.toml

Agent: Validating configs/agents/team-web-research.toml...

       ✅ TOML Syntax: OK
       ✅ Required Fields: OK
         - team.team_id: "team-web-research"
         - team.team_name: "Web Research Team"
         - team.leader.model: "google-gla:gemini-2.5-pro"
       ✅ Model Format: OK
       ✅ Member Agent Count: 2/15
       ✅ agent_name Uniqueness: OK

       Validation successful: This configuration file is valid.
```

### When Errors Are Present

```
User: Validate team.toml

Agent: Validating configs/agents/team-broken.toml...

       ❌ Errors detected:

       1. Missing Required Fields
          - team.members[0].tool_description is undefined
          - Suggestion: Add tool_description = "Description of the agent"

       2. Out of Range Value
          - team.max_concurrent_members = 100 (allowed range: 1-50)
          - Suggestion: Change to a value between 1 and 50

       3. Model Format Error
          - team.leader.model = "gemini-pro" (invalid)
          - Suggestion: Use the format "google-gla:gemini-2.5-pro"
```