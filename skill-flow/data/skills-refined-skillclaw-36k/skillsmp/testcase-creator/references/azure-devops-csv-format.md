# Azure DevOps Test Case CSV Format Guide

## Header Row (Required)

```csv
ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,Assigned To,State
```

**Must be exact.** Nine columns total, all required.

---

## Test Case Structure

### Row Pattern for Each Test Case

```csv
,"Test Case","<Test Case Title>",,,,"GlobalMed","Cody Huls <CHuls@globalmed.com>","Design"
,,,"1","<First action>","<First expected result>",,,
,,,"2","<Second action>","<Second expected result>",,,
,,,"3","<Third action>","<Third expected result>",,,
,,,"4","<Fourth action>","<Fourth expected result>",,,

```

**Key requirements:**

- **Row 1:** Test case metadata row with title and default values for Area Path, Assigned To, State
- **Columns 1, 4, 5, 6:** Empty (`,,,`) on row 1
- **Row 2+:** Test steps starting from step 1
- **Columns 1-3:** Empty (`,,,`) on step rows
- **Step numbers:** Sequential starting from 1 (1, 2, 3, 4...)
- **ALL text values** in columns 2 (Work Item Type), 5 (Step Action), and 6 (Step Expected) MUST be wrapped in double quotes
- **Blank line between test cases**

---

## Complete Working Example

```csv
ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,Assigned To,State
,"Test Case","Verify Upload In Progress Modal Display and Content",,,,"GlobalMed","Cody Huls <CHuls@globalmed.com>","Design"
,,,"1","Navigate to eNcounter Summary Upload Modal","eNcounter Summary Upload Modal is displayed",,,
,,,"2","Locate Upload Summary button","Upload Summary button is accessible and clickable",,,
,,,"3","Click Upload Summary button","Upload in Progress modal displays",,,
,,,"4","Read modal content","Modal displays message informing user that upload is in progress",,,

,"Test Case","Verify Finish Button Ends Consult and Navigates to Let's Get Started",,,,"GlobalMed","Cody Huls <CHuls@globalmed.com>","Design"
,,,"1","Navigate to eNcounter Summary Upload Modal","eNcounter Summary Upload Modal is displayed",,,
,,,"2","Click Upload Summary button","Upload in Progress modal is displayed",,,
,,,"3","Locate Finish button","Finish button is visible and clickable in the modal",,,
,,,"4","Click Finish button","Button is clicked",,,
,,,"5","Verify consult session ends","Consult session is terminated",,,
,,,"6","Verify navigation","User is navigated to Let's Get Started Screen",,,

,"Test Case","Verify Modal Components with Comma-Separated Values",,,,"GlobalMed","Cody Huls <CHuls@globalmed.com>","Design"
,,,"1","Navigate to eNcounter Summary Upload Modal","eNcounter Summary Upload Modal is displayed",,,
,,,"2","Click Upload Summary button","Upload Summary button is clicked",,,
,,,"3","Observe Upload in Progress modal","Upload in Progress modal displays immediately after button click",,,
,,,"4","Verify modal components","Modal contains upload progress indicator, message, and action buttons (Finish and X)",,,

```

---

## Critical Formatting Rules

### 1. Header Row Structure

Nine columns in exact order:

1. `ID` - Always empty in data rows
2. `Work Item Type` - "Test Case" on metadata row, empty on step rows
3. `Title` - Test case title on metadata row, empty on step rows
4. `Test Step` - Empty on metadata row, sequential numbers on step rows
5. `Step Action` - Empty on metadata row, action description on step rows
6. `Step Expected` - Empty on metadata row, expected result on step rows
7. `Area Path` - "GlobalMed" on metadata row, empty on step rows
8. `Assigned To` - "Cody Huls <CHuls@globalmed.com>" on metadata row, empty on step rows
9. `State` - "Design" on metadata row, empty on step rows

### 2. Mandatory Double Quotes

**CRITICAL:** ALL text values in columns 2, 5, and 6 must be wrapped in double quotes, even if they don't contain commas or special characters.

**Correct:**

```csv
,,,"1","Navigate to Select Patient screen","Select Patient screen is displayed",,,
```

**Incorrect:**

```csv
,,,"1",Navigate to Select Patient screen,Select Patient screen is displayed,,,
```

### 3. Handling Special Characters

When Step Action or Step Expected contains commas, quotes, or other special characters, the text is already wrapped in double quotes (as required), which handles the CSV escaping:

```csv
,,,"4","Verify modal components","Modal contains upload progress indicator, message, and action buttons (Finish and X)",,,
```

When the text contains double quotes, escape them by doubling:

```csv
,,,"5","Verify error message text","Error message reads ""Connection Failed, please contact your system administrator""",,,
```

### 4. Test Case Metadata Row

First row of each test case:

```csv
,"Test Case","<Title>",,,,"GlobalMed","Cody Huls <CHuls@globalmed.com>","Design"
```

- Column 1 (ID): Empty
- Column 2 (Work Item Type): `"Test Case"` (quoted)
- Column 3 (Title): Test case title in quotes
- Columns 4, 5, 6 (Test Step, Step Action, Step Expected): Empty
- Column 7 (Area Path): `"GlobalMed"` (quoted)
- Column 8 (Assigned To): `"Cody Huls <CHuls@globalmed.com>"` (quoted)
- Column 9 (State): `"Design"` (quoted)

### 5. Test Step Rows

Subsequent rows after metadata row:

```csv
,,,"1","Navigate to workspace page","Workspace page is displayed",,,
```

- Columns 1, 2, 3 (ID, Work Item Type, Title): Empty (`,,,`)
- Column 4 (Test Step): Step number in quotes (`"1"`, `"2"`, `"3"`, etc.)
- Column 5 (Step Action): Action description in quotes
- Column 6 (Step Expected): Expected result in quotes
- Columns 7, 8, 9 (Area Path, Assigned To, State): Empty (`,,,`)

### 6. Blank Lines

Insert one blank line between each test case for visual clarity.

### 7. No Special Formatting

- No bullet points
- No line breaks within cells
- No paragraph-style text
- Keep actions and expected results concise

---

## Reference Files

### Format Documentation

- **testcase-instructions.md** - Formatting rules and guidelines
- **testcase-example.csv** - Complete example with multiple test cases (eNr_118559)

### Complete Working Examples

Examples located in `.claude/skills/testcase-creator/examples/`:

- **eNr_118557_Welcome-Log-In-Screen-Forms-Based-Authentication.TestCases.csv**
  - Forms-based authentication workflow
  - Welcome screen component verification
  - License detection scenarios

- **eNr_118559_Select-Patient-eNcounter-Cloud-Search.TestCases.csv**
  - Patient search with validation fields
  - DICOM Worklist integration
  - Comprehensive field verification examples

- **eNr_121265_workspace-screen-share.TestCases.csv**
  - Modal workflows with screen sharing
  - State transitions during active sharing

- **eNr_122019_encounter-refresh-user-directory-participants-tab.TestCases.csv**
  - Tab navigation and participant management
  - Multiple user types and call states

- **eNr_124798_app-loading-behavior.TestCases.csv**
  - Connection retry logic with timing validation
  - Error message handling with escaped quotes

Each example includes the paired RequirementAnalysis.txt file showing the input requirements that generated the test cases.

---

## Import Verification

After generating a CSV file, verify:

- [ ] Header has all 9 columns in correct order
- [ ] ALL text in columns 2, 5, 6 is wrapped in double quotes
- [ ] Metadata row has correct default values (GlobalMed, Cody Huls, Design)
- [ ] Step numbers are sequential (1, 2, 3, 4...)
- [ ] Blank lines separate test cases
- [ ] No duplicate first step (old format is deprecated)
- [ ] Test import in Azure DevOps to confirm format compatibility
