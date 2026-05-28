---
name: import-pipeline
description: Use this skill when you want to create Robot Framework test cases for importing SnapLogic pipelines (.slp files), check prerequisites, or see examples of pipeline imports.
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
- Troubleshooting assistance?

### Step 2: Provide Information
Based on the user's request, provide the relevant information or create the test case. Use the following templates and references as needed.

## Quick Reference

**Import pipeline test case template:**
```robotframework
[Template]    Import Pipelines From Template
${unique_id}    ${PIPELINES_LOCATION_PATH}    ${pipeline_name}    ${pipeline_file_name}
```

**Required variables:**
- `${pipeline_name}` - Logical name (without .slp extension)
- `${pipeline_file_name}` - Physical file name (with .slp extension)
- `${PIPELINES_LOCATION_PATH}` - SnapLogic destination path
- `${unique_id}` - Generated in suite setup

**Pipeline file location:**
```
src/pipelines/your_pipeline.slp
```

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

**Related slash command:** `/import-pipeline-testcase`

### Step 3: Respond to User
Provide the requested information or create the test case based on the user's needs. For simple questions, give a concise answer first, then offer to explain more if needed.