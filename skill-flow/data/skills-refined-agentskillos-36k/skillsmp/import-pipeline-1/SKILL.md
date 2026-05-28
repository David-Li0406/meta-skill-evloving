---
name: import-pipeline
description: Creates Robot Framework test cases for importing SnapLogic pipelines. Use when the user wants to import pipelines (.slp files), needs to know prerequisites for pipeline import, or wants to see pipeline import test case examples.
user-invocable: true
---

# SnapLogic Pipeline Import Skill

## Usage Examples

| What You Want | Example Prompt |
|---------------|----------------|
| Explain steps | `Explain the steps to import a pipeline` |
| Import single pipeline | `Create a robot test case to import my_pipeline.slp` |
| Import multiple pipelines | `Generate a test case to import multiple pipelines` |
| Check prerequisites | `What are the prerequisites for importing a pipeline?` |
| Get template | `Show me a template for importing pipelines` |
| See example | `What does a pipeline import test case look like?` |
| File location | `Where do I put my .slp pipeline file?` |
| Variables needed | `What variables do I need for pipeline import?` |
| Parameterization | `How do I parameterize my pipeline for testing?` |
| Troubleshoot | `Pipeline import failed - how do I fix it?` |

---

## Claude Instructions

**IMPORTANT:** When user asks a simple question like "How do I import a pipeline?", provide a **concise answer first** with just the template/command, then offer to explain more if needed. Do NOT dump all documentation.

**Response format for simple questions:**
1. Give the direct template or test case first
2. Add a brief note if relevant
3. Offer "Want me to explain more?" only if appropriate

---

## Quick Template Reference

**Import pipeline test case:**
```robotframework
[Template]    Import Pipelines From Template
${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${pipeline_file_name}
```

**Required variables:**
- `${pipeline_name}` - Logical name (without .slp)
- `${pipeline_file_name}` - Physical file (with .slp)
- Pipeline file location: `src/pipelines/your_pipeline.slp`

**Related slash command:** `/import-pipeline-testcase`

---

## Agentic Workflow (Claude: Follow these steps in order)

**This is the complete guide. Proceed with the steps below.**

### Step 1: Understand the User's Request
Parse what the user wants:
- Import a single pipeline or multiple pipelines?
- Need prerequisites checklist?
- Create test case?
- Show template or examples?
- Questions about pipeline parameterization?

### Step 2: Follow the Guide
Use the detailed instructions below to:
- Show the prerequisites for pipeline import
- Verify pipeline .slp file location
- Create or explain the test case
- Provide troubleshooting if needed

### Step 3: Respond to User
Provide the requested information or create the test case based on this guide.

---

## Quick Reference

**Pipeline file location:**
```
src/pipelines/your_pipeline.slp
```

**Required variables:**
- `${pipeline_name}` - Logical name (without .slp extension)
- `${pipeline_file_name}` - Physical file name (with .slp extension)
- `${PIPELINES_LOCATION_PATH}` - SnapLogic destination path
- `${unique_id}` - Generated in suite setup

**Related slash command:** `/import-pipeline-testcase`

**Baseline test references:**
- `test/suite/pipeline_tests/snowflake/snowflake_baseline_tests.robot`
- `test/suite/pipeline_tests/oracle/oracle_baseline_tests.robot`
- `test/suite/pipeline_tests/postgres/postgres_baseline_tests.robot`

---

## Prerequisites Checklist

Before importing a pipeline, ensure you have completed the following:

### Step 1: Pipeline Preparation in SnapLogic Designer

1. **Build and test your pipeline** in SnapLogic Designer
   - Ensure the pipeline executes successfully
   - **Best Practice:** Use pipeline parameters for:
     - Account names (e.g., `snowflake_acct`, `oracle_acct`)
     - Database connection details (schema, table names)
     - File paths
     - Any configurable values

2. **Why use pipeline parameters?**
   - Provides flexibility to execute pipelines with different data sets
   - Allows runtime updates through triggered tasks
   - Makes pipelines reusable across environments

3. **Determine deployment locations:**
   - Where should accounts be created? (e.g., `shared`, `accounts`)
   - Where should pipelines be imported? (e.g., project path)

### Step 2: Export Pipeline as .slp File

1. In SnapLogic Designer, right-click on your pipeline
2. Select **Export** or **Download as SLP**
3. Save the `.slp` file

### Step 3: Upload Pipeline to Project

**IMPORTANT:** Upload your `.slp` pipeline file to:

```
src/pipelines/
```

Full path:
```
/snaplogic-robotframework-examples/src/pipelines/your_pipeline.slp
```

### Step 4: Verify File Location

```bash
# Check if pipeline exists
ls src/pipelines/*.slp
```

---

## Expected Outcome After Prerequisites

- Valid `.slp` pipeline file in `src/pipelines/`
- Clear understanding of required accounts
- Knowledge of database/service credentials needed
- Defined import locations for pipelines and accounts
- Pipeline uses parameters for flexibility

---

## Quick Start Template

Here's a basic test case template for importing pipelines:

> **IMPORTANT: Required Libraries**
> When creating any new Robot file, ALWAYS include these Resource imports under `*** Settings ***`:
> - `snaplogic_common_robot/snaplogic_apis_keywords/snaplogic_keywords.resource` - SnapLogic API keywords from installed package
> - `../../resources/common/general.resource` - Project-specific common keywords

```robotframework
*** Settings ***
Documentation    Imports SnapLogic pipelines for testing
...              Uploads pipeline definitions (.slp files) to the specified project location
Resource         snaplogic_common_robot/snaplogic_apis_keywords/snaplogic_keywords.resource
Resource         ../../resources/common/general.resource
Library          Collections

*** Variables ***
# Pipeline configuration
${pipeline_name}                my_pipeline
${pipeline_file_name}           my_pipeline.slp

*** Test Cases ***
Import Pipeline
    [Documentation]    Imports pipeline file (.slp) into the SnapLogic project space.
    ...    This test case uploads pipeline definitions and deploys them to the specified location,
    ...    making them available for task creation and execution.
    ...
    ...    PREREQUISITES:
    ...    - ${unique_id} - Generated from suite setup (Check connections keyword)
    ...    - Pipeline .slp file must exist in src/pipelines/ directory
    ...    - SnapLogic project and folder structure must be in place
    ...
    ...    ARGUMENT DETAILS:
    ...    - Argument 1: ${unique_id} - Unique test execution identifier for naming/tracking
    ...    - Argument 2: ${PIPELINES_LOCATION_PATH} - SnapLogic folder path where pipelines will be imported
    ...    - Argument 3: ${pipeline_name} - Logical name for the pipeline (without .slp extension)
    ...    - Argument 4: ${pipeline_file_name} - Physical .slp file name to import
    [Tags]    pipeline_import    setup
    [Template]    Import Pipelines From Template
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${pipeline_file_name}
```

---

## How Pipeline Import Works

```
┌─────────────────────────┐
│  src/pipelines/         │
│  your_pipeline.slp      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│   Import Pipelines      │     │   SnapLogic API         │
│   From Template         │────▶│   Pipeline Import       │
│   Keyword               │     │                         │
└─────────────────────────┘     └───────────┬─────────────┘
                                            │
                                            ▼
                                ┌─────────────────────────┐
                                │   Pipeline Available    │
                                │   in SnapLogic at:      │
                                │   ${PIPELINES_LOCATION_ │
                                │   PATH}/${pipeline_name}│
                                └─────────────────────────┘
```

---

## Template Keyword Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `${unique_id}` | Unique test execution identifier (generated in suite setup) | `test_20240115_143022` |
| `${PIPELINES_LOCATION_PATH}` | SnapLogic path where pipeline will be imported | `org/project_space/project` |
| `${pipeline_name}` | Logical name for the pipeline (used in SnapLogic) | `snowflake_etl` |
| `${pipeline_file_name}` | Physical .slp file name in src/pipelines/ | `snowflake_etl.slp` |

---

## Key Environment Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `${PIPELINES_LOCATION_PATH}` | Project folder path for pipelines | `ml-legacy-migration/slim-travis-automation-ps/slim_travis_project` |
| `${ORG_NAME}` | SnapLogic organization name | `ml-legacy-migration` |
| `${PROJECT_SPACE}` | Project space name | `slim-travis-automation-ps` |
| `${PROJECT_NAME}` | Project name | `slim_travis_project` |

---

## Test Case Examples

### Basic Pipeline Import

```robotframework
*** Variables ***
${pipeline_name}                snowflake_demo
${pipeline_file_name}           snowflake_demo.slp

*** Test Cases ***
Import Snowflake Pipeline
    [Documentation]    Imports Snowflake demo pipeline into the project.
    [Tags]    snowflake    pipeline_import
    [Template]    Import Pipelines From Template
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${pipeline_file_name}
```

### Multiple Pipeline Import

```robotframework
*** Variables ***
# Pipeline 1
${pipeline1_name}               data_extractor
${pipeline1_file_name}          data_extractor.slp

# Pipeline 2
${pipeline2_name}               data_transformer
${pipeline2_file_name}          data_transformer.slp

# Pipeline 3
${pipeline3_name}               data_loader
${pipeline3_file_name}          data_loader.slp

*** Test Cases ***
Import ETL Pipelines
    [Documentation]    Imports multiple ETL pipeline files into the project.
    ...    Each row represents a pipeline import operation.
    [Tags]    etl    pipeline_import    multi_pipeline
    [Template]    Import Pipelines From Template
    # unique_id    pipelines_location    pipeline_name    pipeline_file_name
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline1_name}    ${pipeline1_file_name}
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline2_name}    ${pipeline2_file_name}
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline3_name}    ${pipeline3_file_name}
```

### Pipeline Import with Account Creation (Complete Setup)

```robotframework
*** Settings ***
Documentation    Complete pipeline setup with account and import
Resource         snaplogic_common_robot/snaplogic_apis_keywords/snaplogic_keywords.resource
Resource         ../../resources/common/general.resource
Library          Collections

*** Variables ***
${pipeline_name}                oracle_to_snowflake
${pipeline_file_name}           oracle_to_snowflake.slp

*** Test Cases ***
Create Oracle Account
    [Documentation]    Creates Oracle source account.
    [Tags]    oracle    account_setup
    [Template]    Create Account From Template
    ${ACCOUNT_LOCATION_PATH}    ${ORACLE_ACCOUNT_PAYLOAD_FILE_NAME}    ${ORACLE_ACCOUNT_NAME}    overwrite_if_exists=${TRUE}

Create Snowflake Account
    [Documentation]    Creates Snowflake destination account.
    [Tags]    snowflake    account_setup
    [Template]    Create Account From Template
    ${ACCOUNT_LOCATION_PATH}    ${SNOWFLAKE_ACCOUNT_PAYLOAD_KEY_PAIR_FILE_NAME}    ${SNOWFLAKE_KEYPAIR_ACCOUNT_NAME}    overwrite_if_exists=${TRUE}

Import Pipeline
    [Documentation]    Imports the Oracle to Snowflake pipeline.
    [Tags]    pipeline_import
    [Template]    Import Pipelines From Template
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${pipeline_file_name}
```

---

## File Location Conventions

### Pipeline Files
```
src/
└── pipelines/                          # Upload your .slp files here
    ├── snowflake_demo.slp
    ├── oracle_etl.slp
    ├── kafka_consumer.slp
    └── data_processor.slp
```

### Test Suite Structure
```
test/suite/pipeline_tests/
├── snowflake/
│   └── snowflake_baseline_tests.robot  # Contains Import Pipeline test case
├── oracle/
│   └── oracle_baseline_tests.robot
└── your_system/
    └── your_tests.robot
```

---

## Pipeline Parameterization Best Practices

### Why Parameterize?

Parameterized pipelines are more flexible and reusable:

```
# In SnapLogic Designer, use expression parameters like:
_snowflake_acct       # Account reference
_schema_name          # Database schema
_table_name           # Target table
_input_file           # Input file path
```

### Using Parameters in Test Cases

```robotframework
*** Variables ***
# Task parameters that map to pipeline parameters
&{task_params_set}
...    snowflake_acct=../shared/${SNOWFLAKE_ACCOUNT_NAME}
...    schema_name=DEMO
...    table_name=DEMO.TEST_TABLE
...    input_file=${input_file_name}

*** Test Cases ***
Create Triggered Task With Parameters
    [Documentation]    Creates task with pipeline parameters.
    [Tags]    task_creation
    [Template]    Create Triggered Task From Template
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${task_name}    ${GROUNDPLEX_NAME}    ${task_params_set}
```

---

## Complete Example from Baseline Test

From `snowflake_baseline_tests.robot`:

```robotframework
*** Variables ***
# Pipeline name and file details
${pipeline_name}                        snowflake_keypair
${pipeline_file_name}                   snowflake_keypair.slp
${sf_acct_keypair}                      ${pipeline_name}_account

# Task Details
${task_name}                            Task

# Task parameters
&{task_params_set}
...                                     snowflake_acct=../shared/${sf_acct_keypair}
...                                     schema=DEMO
...                                     table=DEMO.TEST_SNAP4
...                                     destination_hint=BRAZE:Subscription
...                                     isTest=test
...                                     test_input_file=${input_file1_path}

*** Test Cases ***
Import Pipeline
    [Documentation]    Imports Snowflake pipeline files (.slp) into the SnapLogic project space.
    ...    This test case uploads pipeline definitions and deploys them to the specified location,
    ...    making them available for task creation and execution.
    ...
    ...    PREREQUISITES:
    ...    - ${unique_id} - Generated from suite setup (Check connections keyword)
    ...    - Pipeline .slp files must exist in the test_data directory
    ...    - SnapLogic project and folder structure must be in place
    ...
    ...    ARGUMENT DETAILS:
    ...    - Argument 1: ${unique_id} - Unique test execution identifier for naming/tracking
    ...    - Argument 2: ${PIPELINES_LOCATION_PATH} - SnapLogic folder path where pipelines will be imported
    ...    - Argument 3: ${pipeline_name} - Logical name for the pipeline (without .slp extension)
    ...    - Argument 4: ${pipeline_file_name} - Physical .slp file name to import
    [Tags]    snowflake_demo    snowflake_demo3    snowflake_multiple_files
    [Template]    Import Pipelines From Template

    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${pipeline_file_name}
```

---

## Typical Test Execution Flow

```
┌─────────────────────────┐
│  1. Suite Setup         │
│  (Generate unique_id)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  2. Create Accounts     │
│  (Database, S3, etc.)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  3. Upload Files        │
│  (Input data, expr libs)│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  4. Import Pipeline     │  ◄── THIS SKILL
│  (.slp file)            │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  5. Create Task         │
│  (Triggered/Ultra)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  6. Execute Task        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  7. Verify Results      │
└─────────────────────────┘
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Pipeline file not found` | .slp file not in src/pipelines/ | Upload pipeline to `src/pipelines/` |
| `Import failed` | Invalid .slp format | Re-export pipeline from SnapLogic Designer |
| `Pipeline already exists` | Pipeline with same name exists | Use different name or delete existing |
| `Permission denied` | User lacks import permissions | Check SnapLogic permissions |
| `Project not found` | PIPELINES_LOCATION_PATH incorrect | Verify path in .env file |

### Debug Tips

1. **Verify pipeline file exists:**
   ```bash
   ls src/pipelines/${pipeline_file_name}
   ```

2. **Log the paths being used:**
   ```robotframework
   Log    Pipeline file: ${pipeline_file_name}    console=yes
   Log    Destination: ${PIPELINES_LOCATION_PATH}    console=yes
   ```

3. **Check environment variables:**
   ```bash
   make check-env
   ```

---

## Checklist Before Committing

- [ ] Pipeline .slp file exists in `src/pipelines/`
- [ ] Pipeline tested and working in SnapLogic Designer
- [ ] Pipeline uses parameters for configurable values
- [ ] `${pipeline_name}` variable defined (without .slp extension)
- [ ] `${pipeline_file_name}` variable defined (with .slp extension)
- [ ] Test has appropriate tags
- [ ] Documentation describes the pipeline being imported
- [ ] Required accounts are created before pipeline import (if pipeline references them)
