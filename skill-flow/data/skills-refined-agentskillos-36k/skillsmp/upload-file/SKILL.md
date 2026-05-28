---
name: upload-file
description: Creates Robot Framework test cases for uploading files to SnapLogic SLDB. Use when the user wants to upload files (JSON, CSV, expression libraries, pipelines, JAR files, etc.), needs to know which destination path to use, or wants to see file upload test case examples.
user-invocable: true
---

# SnapLogic File Upload Skill

## Agentic Workflow (Claude: Follow these steps in order)

### Step 1: Load the Complete Guide
```
ACTION: Use the Read tool to load:
{{cookiecutter.primary_pipeline_name}}/.claude/skills/upload-file/SKILL.md
```
**Do not proceed until you have read the complete guide.**

### Step 2: Understand the User's Request
Parse what the user wants:
- What file type? (JSON, CSV, .expr, .slp, .jar, etc.)
- Upload to which location? (project folder, shared folder)
- Single file or multiple files?
- Create test case?
- Show template or examples?
- Questions about SLDB or destination paths?

### Step 3: Follow the Guide
Use the detailed instructions from the file you loaded in Step 1 to:
- Identify the correct destination path variable
- Determine the appropriate file location convention
- Check baseline tests for reference if needed
- Create or explain the test case

### Step 4: Respond to User
Provide the requested information or create the test case based on the complete guide.

---

## Quick Reference

**Supported file types:**
`json`, `csv`, `slp` (pipeline), `expr` (expression library), `jar`, `txt`, `xml`

**Key destination paths:**
- `${PIPELINES_LOCATION_PATH}` - Test input files, pipelines, project-specific files
- `${ACCOUNT_LOCATION_PATH}` - Expression libraries, JAR files, shared resources

**Related slash command:** `/upload-file-testcase`
