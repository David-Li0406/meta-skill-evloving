---
name: upload-file
description: Use this skill to create Robot Framework test cases for uploading various file types to SnapLogic SLDB, including JSON, CSV, expression libraries, pipelines, and JAR files.
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

### Step 2: Follow the Guide
Use the detailed instructions below to:
- Identify the correct destination path variable
- Determine the appropriate file location convention
- Check baseline tests for reference if needed
- Create or explain the test case

### Step 3: Respond to User
Provide the requested information or create the test case based on this guide.

---

## Quick Reference

**Supported file types:**
`json`, `csv`, `slp` (pipeline), `expr` (expression library), `jar`, `txt`, `xml`

**Key destination paths:**
| Variable | Use For |
|----------|---------|
| `${PIPELINES_LOCATION_PATH}` | Test input files, pipelines, project-specific files |
| `${ACCOUNT_LOCATION_PATH}` | Expression libraries, JAR files, shared resources |

**What is SLDB?**
SLDB (SnapLogic Database) is SnapLogic's internal file storage. Files uploaded to project spaces are stored in SLDB and referenced using paths like `sldb:///org/project_space/project/file.json`.

**Related slash command:** `/upload-file-testcase`

---

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

---

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

---

## Test Case Examples by File Type

### JSON Input Files
```robotframework
Upload JSON Test Input File
    [Documentation]    Uploads JSON test input file to SnapLogic project folder.
    [Tags]    upload    json    setup
    [Template]    Upload File Using File Protocol Template
    ${CURDIR}/../../test_data/actual_expected_data/input_data/snowflake/test_input.json    ${PIPELINES_LOCATION_PATH}
```

### CSV Input Files
```robotframework
Upload CSV Test Data
    [Documentation]    Uploads CSV test data file to SnapLogic project folder.
    [Tags]    upload    csv    setup
    [Template]    Upload File Using File Protocol Template
    ${CURDIR}/../../test_data/actual_expected_data/input_data/test_data.csv    ${PIPELINES_LOCATION_PATH}
```

### Expression Libraries
```robotframework
Upload Expression Library
    [Documentation]    Uploads expression library (.expr) to shared folder.
    [Tags]    upload    expr    setup
    [Template]    Upload File Using File Protocol Template
    ${CURDIR}/../../test_data/actual_expected_data/expression_libraries/my_library.expr    ${ACCOUNT_LOCATION_PATH}
```

### Multiple Files in One Test Case
```robotframework
Upload Multiple Test Files
    [Documentation]    Uploads multiple files to SnapLogic using data-driven approach.
    [Tags]    upload    setup    multi_file
    [Template]    Upload File Using File Protocol Template
    ${CURDIR}/../../test_data/actual_expected_data/input_data/snowflake/test_input1.json    ${PIPELINES_LOCATION_PATH}
    ${CURDIR}/../../test_data/actual_expected_data/input_data/snowflake/test_input2.json    ${PIPELINES_LOCATION_PATH}
    ${CURDIR}/../../test_data/actual_expected_data/input_data/snowflake/test_input3.json    ${PIPELINES_LOCATION_PATH}
    ${CURDIR}/../../test_data/actual_expected_data/expression_libraries/snowflake/snowflake_library.expr    ${ACCOUNT_LOCATION_PATH}
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Source file not found` | File path is incorrect | Check `${CURDIR}` relative path |
| `Permission denied` | User lacks write access to destination | Verify `${ACCOUNT_LOCATION_PATH}` permissions |
| `File not uploaded` | Destination path doesn't exist | Ensure project space/folder exists |

### Debug Tips
1. **Verify file exists locally:**
   ```robotframework
   File Should Exist    ${input_file_path}
   ```

2. **Log the paths being used:**
   ```robotframework
   Log    Local path: ${input_file_path}    console=yes
   Log    Destination: ${PIPELINES_LOCATION_PATH}    console=yes
   ```

3. **Check environment variables:**
   ```bash
   make check-env
   ```

---

## Checklist Before Committing
- [ ] Local file path uses `${CURDIR}` for relative paths
- [ ] Destination path uses appropriate environment variable
- [ ] Expression libraries go to `${ACCOUNT_LOCATION_PATH}` (shared)
- [ ] Test input files go to `${PIPELINES_LOCATION_PATH}` (project)
- [ ] Test has appropriate tags
- [ ] Documentation describes the file being uploaded
- [ ] No hardcoded paths (use environment variables)