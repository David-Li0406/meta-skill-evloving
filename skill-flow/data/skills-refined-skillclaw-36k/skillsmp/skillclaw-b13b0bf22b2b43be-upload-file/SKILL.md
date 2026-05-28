---
name: upload-file
description: Use this skill when you need to create Robot Framework test cases for uploading various file types to SnapLogic SLDB, including JSON, CSV, and JAR files, or when you need guidance on destination paths and examples.
---

# SnapLogic File Upload Skill

## Agentic Workflow

### Step 1: Understand the User's Request
Parse what the user wants:
- What file type? (JSON, CSV, .expr, .slp, .jar, etc.)
- Upload to which location? (project folder, shared folder)
- Single file or multiple files?
- Create test case?
- Show template or examples?
- Questions about SLDB or destination paths?

### Step 2: Provide Quick Reference
**Supported file types:**
- `json`
- `csv`
- `slp` (pipeline)
- `expr` (expression library)
- `jar`
- `txt`
- `xml`

**Key destination paths:**
- `${PIPELINES_LOCATION_PATH}` - Test input files, pipelines, project-specific files
- `${ACCOUNT_LOCATION_PATH}` - Expression libraries, JAR files, shared resources

### Step 3: Follow the Guide
Use the detailed instructions to:
- Identify the correct destination path variable
- Determine the appropriate file location convention
- Check baseline tests for reference if needed
- Create or explain the test case

### Step 4: Respond to User
Provide the requested information or create the test case based on the user's needs.

## Usage Examples

| What You Want | Example Prompt |
|---------------|----------------|
| Explain steps | `Explain the steps to upload a file to SnapLogic` |
| Upload JSON file | `Upload a JSON file to SnapLogic` |
| Upload CSV file | `Create a test case to upload CSV test data to my project` |
| Upload expression library | `Upload an expression library to the shared folder` |
| Upload JAR file | `Upload JDBC driver JAR for MySQL` |
| Upload multiple files | `I need to upload multiple input files for my Snowflake pipeline` |
| Get template | `Show me a template for uploading files` |
| See example | `How do I upload multiple files in one test case?` |
| Path questions | `What's the difference between PIPELINES_LOCATION_PATH and ACCOUNT_LOCATION_PATH?` |
| SLDB info | `What is SLDB and how does file storage work?` |
| Destination help | `Where should I upload expression libraries?` |

## Quick Template Reference

**Upload to project folder (test input files, pipelines):**
```robotframework
[Template]    Upload File Using File Protocol Template
${CURDIR}/../../test_data/input.json    ${PIPELINES_LOCATION_PATH}
```

**Upload to shared folder (expression libraries, JAR files):**
```robotframework
[Template]    Upload File Using File Protocol Template
${CURDIR}/../../test_data/my_library.expr    ${ACCOUNT_LOCATION_PATH}
```

**Related slash command:** `/upload-file-testcase`