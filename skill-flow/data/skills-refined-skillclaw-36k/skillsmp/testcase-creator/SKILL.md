---
name: testcase-creator
description: Generate requirements-based test cases from Gherkin user stories using BDD methodology. Use this skill when the user asks to create test cases, generate test cases from user stories, analyze requirements for testing, convert user stories to test cases, or work with files in docs/user-stories/. This skill performs comprehensive requirement analysis and outputs Azure DevOps-compatible CSV test case files with proper formatting for import.
---

# Test Case Creator

Transform Gherkin user stories into comprehensive, requirements-based test cases through systematic requirement analysis.

## Input

**File location:** `docs/user-stories/<UserStoryID>_<title>.us.txt`  
**Format:** Gherkin scenarios (Given/When/Then syntax)

## Output

Two files with consistent naming:

1. **Requirement Analysis:** `docs/requirement-analysis/<UserStoryID>_<title>.RequirementAnalysis.txt`
   - Requirements Analysis table (Scenario → Requirement → Test Case mapping)
   - Detailed Test Cases table (one row per test case ID, hierarchical numbering x.y.z)
   - Test Coverage Summary

2. **Test Cases CSV:** `docs/test-cases/<UserStoryID>_<title>.TestCases.csv`
   - Azure DevOps import format (2026 version)
   - Columns: `ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,Assigned To,State`
   - ALL text in columns 2, 5, 6 wrapped in double quotes
   - Default values: GlobalMed, Cody Huls <CHuls@globalmed.com>, Design
   - Blank row between test cases

## Documentation

📚 **Comprehensive guides:**

- `.claude/skills/testcase-creator/references/requirement-analysis-guide.md` - Complete formatting rules, examples, anti-patterns
- `.claude/skills/testcase-creator/references/testcase-instructions.md` - Test case writing methodology (how to combine test case IDs, patterns, step writing)
- `.claude/skills/testcase-creator/references/azure-devops-csv-format.md` - CSV formatting specifications (columns, quotes, structure)

📁 **Working examples:**

- `.claude/skills/testcase-creator/examples/eNr_118557_Welcome-Log-In-Screen-Forms-Based-Authentication.*` - Authentication workflows and component verification
- `.claude/skills/testcase-creator/examples/eNr_118559_Select-Patient-eNcounter-Cloud-Search.*` - Comprehensive search UI with validation
- `.claude/skills/testcase-creator/examples/eNr_121265_workspace-screen-share.*` - Screen share modal workflows
- `.claude/skills/testcase-creator/examples/eNr_122019_encounter-refresh-user-directory-participants-tab.*` - Participants tab management
- `.claude/skills/testcase-creator/examples/eNr_124798_app-loading-behavior.*` - Connection retry and error handling

**IMPORTANT:** Always review the example files in `.claude/skills/testcase-creator/examples/` to ensure correct output format for both RequirementAnalysis.txt and TestCases.csv files.

## Execution Workflow

### Step 1: Read Examples (MANDATORY)

Before generating any output, read at least one example to internalize the exact format:

```
Read .claude/skills/testcase-creator/examples/eNr_121265_workspace-screen-share.TestCases.csv
```

Or use the comprehensive reference example:

```
Read .claude/skills/testcase-creator/examples/eNr_118559_Select-Patient-eNcounter-Cloud-Search.TestCases.csv
```

### Step 2: Generate Documentation

1. Read user story from `docs/user-stories/`
2. Extract requirements and map to test case IDs (hierarchical numbering x.y.z)
3. Generate RequirementAnalysis.txt (follow `references/requirement-analysis-guide.md`)
4. Generate TestCases.csv (follow `references/azure-devops-csv-format.md` and `references/testcase-instructions.md`)

### Step 3: Validation (MANDATORY)

After creating both files, validate format compliance:

**RequirementAnalysis.txt validation:**

- [ ] Three-column table: Scenario Name | Requirement | Test Case
- [ ] Hierarchical test case IDs (1.1.1, 1.1.2, 2.1.1, etc.)
- [ ] Test Coverage Summary section with counts

**TestCases.csv validation:**

- [ ] Read the generated CSV file back
- [ ] Header exactly: `ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,Assigned To,State` (9 columns)
- [ ] Metadata row format: `,"Test Case","<Title>",,,,"GlobalMed","Cody Huls <CHuls@globalmed.com>","Design"`
- [ ] ALL text in columns 2, 5, 6 wrapped in double quotes
- [ ] Step rows: `,,,"1","<Action>","<Expected>",,,` (columns 1-3 empty, columns 7-9 empty)
- [ ] Step numbers sequential: 1, 2, 3, 4... (NO duplicate step 1 - old format deprecated)
- [ ] Blank row between test cases
- [ ] Special characters (quotes, commas) properly handled

**If validation fails:** Read example CSV again and regenerate with corrections.

## Format Changes (2026)

**Key differences from old format:**

1. ✅ **New columns added:** Area Path, Assigned To, State (now 9 columns total)
2. ✅ **Duplicate first step removed:** Each test case starts with step 1 only once
3. ✅ **Mandatory quotes:** ALL text in columns 2, 5, 6 must be wrapped in double quotes
4. ✅ **Default values:** Use GlobalMed, Cody Huls <CHuls@globalmed.com>, Design

**Deprecated patterns:**

- ❌ Old 6-column header
- ❌ Duplicate step 1 in test cases
- ❌ Optional quotes (quotes are now mandatory)
