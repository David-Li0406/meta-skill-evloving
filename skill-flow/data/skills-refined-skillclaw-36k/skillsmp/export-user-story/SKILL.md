---
name: export-user-story
description: Export user story acceptance criteria from Azure DevOps by ID and optionally generate requirement analysis and test cases. Use this skill when the user wants to export a user story from Azure DevOps, create test documentation, or generate a complete test package from a user story ID.
---

# Export User Story

Export user story acceptance criteria from Azure DevOps and optionally generate requirement analysis and test cases.

## Quick Start

**Export only:**

```
@export-user-story 122019
```

**Export + generate test cases (full documentation):**

```
@export-user-story 122019 --full
```

**Important:** The skill will automatically:

1. Configure Python environment using `configure_python_environment` tool
2. Execute export script with proper PowerShell syntax (`&` operator)
3. Use `--auto` flag for non-interactive filename generation

## Workflow

### 1. Export Acceptance Criteria

**CRITICAL: Always configure Python environment first**

```powershell
# Step 1: Configure Python environment (ALWAYS DO THIS FIRST)
# Use configure_python_environment tool with workspace path

# Step 2: Run export script with --auto flag for non-interactive mode
& ".venv/Scripts/python.exe" ".claude/skills/export-user-story/scripts/export-acceptance-criteria.py" <work_item_id> --auto
```

**PowerShell syntax notes:**

- MUST use `&` call operator before the quoted Python executable path
- Use relative paths from workspace root (`.venv/Scripts/python.exe`)
- The `--auto` flag is required for non-interactive execution

**What it does:**

- Fetches user story from Azure DevOps API
- Converts HTML to formatted text with:
  - Proper Scenario spacing
  - Bullet points as markdown (`- Item`)
  - Clean Given/When/Then formatting
- Saves to: `docs/user-stories/<prefix>_<id>_<title>.us.txt`

**Prerequisites:**

- Python environment configured using `configure_python_environment` tool
- `.claude/skills/export-user-story/scripts/.env` configured with Azure DevOps credentials
- Python packages installed (see README)

**Examples:**

- See `.claude/skills/export-user-story/examples/` for sample output files

### 2. Generate Test Cases (Optional)

After export completes, invoke the testcase-creator skill:

```
@testcase-creator generate test cases for <filename>.us.txt
```

**What it generates:**

- `docs/requirement-analysis/<filename>.RequirementAnalysis.txt` - Requirement breakdown and metrics
- `docs/test-cases/<filename>.TestCases.csv` - Azure DevOps importable test cases

## Full Workflow

When user requests `--full` or "complete test package":

1. **Prompt for User Story ID** if not provided
2. **Configure Python environment** using `configure_python_environment` tool (REQUIRED FIRST STEP)
3. **Run export script** with proper PowerShell syntax:
   - Use `&` operator before quoted path
   - Use relative path: `.venv/Scripts/python.exe`
   - Include `--auto` flag for non-interactive mode
   - Example: `& ".venv/Scripts/python.exe" ".claude/skills/export-user-story/scripts/export-acceptance-criteria.py" 122060 --auto`
4. **Invoke testcase-creator** skill automatically with the exported file
5. **Confirm outputs** created:
   - `.us.txt` (acceptance criteria)
   - `.RequirementAnalysis.txt` (requirement analysis)
   - `.TestCases.csv` (test cases)

## Configuration

The export script uses environment variables from `.claude/skills/export-user-story/scripts/.env`:

```
AZURE_DEVOPS_ORGANIZATION=your-org
AZURE_DEVOPS_PROJECT=your-project
AZURE_DEVOPS_PAT=your-personal-access-token
PRODUCT_PREFIX=eNr
```

Copy `.claude/skills/export-user-story/scripts/.env.example` to `.claude/skills/export-user-story/scripts/.env` and fill in your values.

## File Naming Convention

All generated files follow the same naming pattern:

```
<prefix>_<id>_<title>.<extension>
```

Examples:

- `eNr_122019_participants_tab.us.txt`
- `eNr_122019_participants_tab.RequirementAnalysis.txt`
- `eNr_122019_participants_tab.TestCases.csv`

## Error Handling

**PowerShell syntax errors:**

- If you see `Unexpected token` error, ensure `&` operator is used before quoted path
- Correct: `& ".venv/Scripts/python.exe" "script.py"`
- Incorrect: `".venv/Scripts/python.exe" "script.py"`

**Python environment errors:**

- Always run `configure_python_environment` tool BEFORE executing Python scripts
- Use the returned Python executable path in terminal commands

**Authentication errors:**

- Verify PAT in `.env` has not expired
- Check organization and project names are correct

**Empty acceptance criteria:**

- Script will prompt whether to create empty file
- Manual entry may be needed in Azure DevOps

**Formatting issues:**

- Script handles HTML lists, line breaks, and special characters
- Scenarios automatically separated with blank lines
