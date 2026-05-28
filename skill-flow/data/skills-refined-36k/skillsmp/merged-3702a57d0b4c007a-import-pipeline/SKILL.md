---
name: import-pipeline
description: Use this skill to create Robot Framework test cases for importing SnapLogic pipelines (.slp files), check prerequisites, or view test case examples.
---

# SnapLogic Pipeline Import Skill

## Agentic Workflow

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

---

## Prerequisites Checklist

Before importing a pipeline, ensure you have completed the following:

### Step 1: Pipeline Preparation in SnapLogic Designer
1. **Build and test your pipeline** in SnapLogic Designer.
2. **Export Pipeline as .slp File**: Right-click on your pipeline and select **Export** or **Download as SLP**.
3. **Upload Pipeline to Project**: Upload your `.slp` pipeline file to:
   ```
   src/pipelines/
   ```

### Step 2: Verify File Location
```bash
# Check if pipeline exists
ls src/pipelines/*.slp
```

---

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

## Quick Start Template

Here's a basic test case template for importing pipelines:

```robotframework
*** Settings ***
Documentation    Imports SnapLogic pipelines for testing
Resource         snaplogic_common_robot/snaplogic_apis_keywords/snaplogic_keywords.resource
Resource         ../../resources/common/general.resource
Library          Collections

*** Variables ***
${pipeline_name}                my_pipeline
${pipeline_file_name}           my_pipeline.slp

*** Test Cases ***
Import Pipeline
    [Documentation]    Imports pipeline file (.slp) into the SnapLogic project space.
    [Template]    Import Pipelines From Template
    ${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${pipeline_file_name}
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

---

## Key Environment Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `${PIPELINES_LOCATION_PATH}` | Project folder path for pipelines | `ml-legacy-migration/slim-travis-automation-ps/slim_travis_project` |
| `${ORG_NAME}` | SnapLogic organization name | `ml-legacy-migration` |
| `${PROJECT_SPACE}` | Project space name | `slim-travis-automation-ps` |
| `${PROJECT_NAME}` | Project name | `slim_travis_project` |

---

## Complete Example from Baseline Test

```robotframework
*** Variables ***
${pipeline_name}                        snowflake_keypair
${pipeline_file_name}                   snowflake_keypair.slp

*** Test Cases ***
Import Pipeline
    [Documentation]    Imports Snowflake pipeline files (.slp) into the SnapLogic project space.
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

## Checklist Before Committing

- [ ] Pipeline .slp file exists in `src/pipelines/`
- [ ] Pipeline tested and working in SnapLogic Designer
- [ ] Pipeline uses parameters for configurable values
- [ ] `${pipeline_name}` variable defined (without .slp extension)
- [ ] `${pipeline_file_name}` variable defined (with .slp extension)
- [ ] Test has appropriate tags
- [ ] Documentation describes the pipeline being imported
- [ ] Required accounts are created before pipeline import (if pipeline references them)