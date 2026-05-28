# Test Case Writing Guide

This guide explains **how to write test cases** from requirement analysis documents. For CSV formatting rules, see [azure-devops-csv-format.md](azure-devops-csv-format.md).

---

## Overview: From Requirements to Test Cases

The requirement analysis document contains a hierarchical mapping:

```
Scenario → Requirements → Test Case IDs
```

Your job is to intelligently group related test case IDs into comprehensive, executable test cases for the CSV file.

**Key principle:** Create efficient test cases that maximize coverage while minimizing test execution time by combining related verifications into logical workflows.

---

## Step 1: Understanding the Requirement Analysis Document

Each requirement analysis document has two main sections:

### Requirements Analysis Table

Shows the hierarchical breakdown:

```
| Scenario Name | Requirement | Test Case |
|---------------|-------------|-----------|
| Scenario 1: Screen Share Button | 1.1 Screen share icon should be visible | 1.1.1 Verify icon is visible |
|  | 1.2 Icon should be in bottom right corner | 1.2.1 Verify icon position |
```

### Detailed Test Cases Table

Provides execution guidance for each test case ID:

```
| Test Case ID | Test Scenario | Expected Result | Test Data |
|--------------|---------------|-----------------|-----------|
| 1.1.1 | Navigate to workspace and observe icon | Icon is visible | N/A |
| 1.2.1 | Verify icon position | Icon in bottom right corner | N/A |
```

---

## Step 2: Identifying Combination Opportunities

Analyze the test case IDs to identify logical groupings. Combine test cases when they:

### ✅ Should be Combined

**1. Sequential UI verifications in the same location:**

```
Test Case IDs:
- 1.1.1 Verify screen share icon is visible
- 1.2.1 Verify screen share icon position in bottom right corner

Combined CSV Test Case: "Verify Screen Share Icon Visibility and Position"
```

**2. Multiple related attributes of the same element:**

```
Test Case IDs:
- 2.1.1 Verify current user's avatar displays
- 2.2.1 Verify current user's name displays
- 2.3.1 Verify current user's role displays
- 2.4.1 Verify only current user shown when not on call

Combined CSV Test Case: "Verify Participants Tab Display When Not On Call"
```

**3. State setup followed by immediate verifications:**

```
Test Case IDs:
- 3.1.1 Verify loading spinner displays
- 3.2.1 Verify "Loading ..." text displays
- 3.3.1 Verify loading UI matches Figma design

Combined CSV Test Case: "Verify Screen Share Modal Loading State"
```

**4. Action followed by immediate result verification:**

```
Test Case IDs:
- 7.1.1 Verify user can select screen
- 7.2.1 Verify Share button available after selection
- 7.3.1 Verify screen is shared when Share clicked
- 7.4.1 Verify shared screen displays as video feed
- 7.5.1 Verify shared screen visible to all users

Combined CSV Test Case: "Verify Share Screen Functionality"
```

### ❌ Should NOT be Combined

**1. Different user workflows or paths:**

```
DON'T combine:
- Scenario 5: User closes modal with X button
- Scenario 8: User clicks Cancel button

These are separate user journeys, even if outcomes are similar.
```

**2. Different preconditions or states:**

```
DON'T combine:
- Scenario 2: User not on a call
- Scenario 3: User on a call with other users

Different starting states = separate test cases.
```

**3. Independent error conditions:**

```
DON'T combine:
- Field validation for First Name
- Field validation for Last Name

Each field's validation is independent and testable separately.
```

**4. Timing-based or performance scenarios:**

```
DON'T combine:
- Connection retry timing (every 1 second)
- Connection failure timeout (after 20 seconds)

Timing scenarios need separate verification.
```

---

## Step 3: Writing Test Case Titles

Test case titles should be clear, concise, and action-oriented.

### Title Patterns

**1. Component verification (static elements):**

```
"Verify [Component] [Attribute] and [Attribute]"

Examples:
- "Verify Screen Share Icon Visibility and Position"
- "Verify Forms Based Authentication Welcome Screen Components"
```

**2. User action workflows:**

```
"Verify [Action] [Outcome/Functionality]"

Examples:
- "Verify Share Screen Functionality"
- "Verify Successful Patient Search with Results"
- "Verify Cancel Button Functionality"
```

**3. State-based scenarios:**

```
"Verify [Component] [State/Condition]"

Examples:
- "Verify Participants Tab Display When Not On Call"
- "Verify Participants Tab Display When On Call With Multiple Users"
- "Verify Screen Share Modal Loading State"
```

**4. Error or edge case testing:**

```
"Verify [Error Condition] [Behavior]"

Examples:
- "Verify Connection Failure Error Message"
- "Verify Search With No Results Displays Appropriate Message"
- "Verify Unsuccessful User Authentication"
```

---

## Step 4: Writing Test Steps

Each test step consists of:

- **Step Action:** What the tester does or observes
- **Step Expected:** What should happen as a result

### Test Step Writing Principles

**1. Start with setup/navigation:**

```
Step 1: "Navigate to the workspace page" → "Workspace page is displayed"
Step 1: "Launch application with forms based authentication enabled" → "Application loads at startup"
```

**2. Use clear, action-oriented language:**

```
Good: "Click the Participants button"
Bad: "The Participants button should be clicked"

Good: "Observe the screen share icon"
Bad: "User should see the screen share icon"
```

**3. Make expected results specific and measurable:**

```
Good: "Screen share icon is visible on the workspace page"
Bad: "Icon appears"

Good: "Error message reads \"Connection Failed, please contact your system administrator\""
Bad: "Error is shown"
```

**4. Include necessary context in expectations:**

```
"Guest user's role displays as 'Guest'"
"Screen share icon is located in the bottom right corner of the page"
"System stops attempting to connect after exactly 20 seconds"
```

**5. Build steps progressively:**

```
Step 1: Navigate to location
Step 2: Perform initial action
Step 3: Observe immediate result
Step 4: Perform secondary action
Step 5: Verify final outcome
```

---

## Step 5: Common Test Case Patterns

### Pattern 1: Component Verification Test

**When:** Multiple related UI elements need verification

**Structure:**

```
Step 1: Navigate to the screen
Step 2-N: Verify each component exists
```

**Example:**

```
Test Case: "Verify Forms Based Authentication Welcome Screen Components"
Step 1: Launch application → Application loads at startup
Step 2: Observe welcome screen → Welcome screen visible with username field
Step 3: Verify password field → Password field displayed on welcome screen
Step 4: Verify Sign-in button → Sign-in button displayed
Step 5: Verify forgot password button → Forgot password button displayed
...
```

### Pattern 2: Workflow/Action Test

**When:** User performs action with expected outcome

**Structure:**

```
Step 1: Navigate/Setup initial state
Step 2: Perform primary action
Step 3: Observe immediate result
Step 4-N: Verify additional outcomes
```

**Example:**

```
Test Case: "Verify Share Screen Functionality"
Step 1: Open screen share modal → Modal displays with available screens
Step 2: Select a screen → Screen is selected and highlighted
Step 3: Observe Share button → Share button enabled after selection
Step 4: Click Share button → Share button is clicked
Step 5: Verify screen shared locally → Screen displays as video feed for sharing user
Step 6: Verify screen shared to all → Shared screen visible to all users on call
```

### Pattern 3: State-Based Verification

**When:** UI behaves differently based on application state

**Structure:**

```
Step 1: Establish the required state
Step 2-N: Verify elements appropriate for that state
```

**Example:**

```
Test Case: "Verify Participants Tab Display When Not On Call"
Step 1: Navigate to workspace and open Participants tab → Tab open, user not on call
Step 2: Observe current user's avatar → Current user's avatar displayed
Step 3: Observe current user's name → Current user's name displayed
Step 4: Observe current user's role → Current user's role displayed
Step 5: Verify participant count → Only current user visible in tab
```

### Pattern 4: Error/Validation Test

**When:** Testing error conditions or validation behavior

**Structure:**

```
Step 1: Navigate to location
Step 2: Trigger error condition
Step 3: Verify error handling
Step 4: (Optional) Verify recovery
```

**Example:**

```
Test Case: "Verify Connection Failure Error Message"
Step 1: Launch application → Application starts loading
Step 2: Simulate sustained connection failure → Connection fails for 20 seconds
Step 3: Verify retry stops → System stops retrying after 20 seconds
Step 4: Observe error message → Error message displayed
Step 5: Verify error text → Message reads "Connection Failed, please contact..."
```

### Pattern 5: Data-Driven Test

**When:** Testing with different inputs or variations

**Structure:**

```
Step 1: Navigate/Setup
Step 2: Enter test data
Step 3: Execute action
Step 4: Verify outcome specific to data
```

**Example:**

```
Test Case: "Verify First Name Field Input Validation"
Step 1: Navigate to Select Patient screen → Screen is displayed
Step 2: Enter invalid characters → Invalid characters entered (e.g. # or %)
Step 3: Observe validation error → Validation error message displayed
Step 4: Clear and enter valid characters → Valid characters matching regex entered
Step 5: Observe no error → No validation error displayed
```

---

## Step 6: Smart Combination Examples

### Example 1: Icon Verification (2 test case IDs → 1 CSV test case)

**Requirement Analysis:**

```
Scenario 1: Screen Share Button
- 1.1.1 Verify screen share icon is visible
- 1.2.1 Verify icon position in bottom right corner
```

**CSV Test Case:**

```
"Verify Screen Share Icon Visibility and Position"
Step 1: Navigate to workspace page → Workspace page displayed
Step 2: Observe screen share icon → Icon visible on workspace page
Step 3: Verify icon position → Icon located in bottom right corner
```

### Example 2: Modal Loading (3 test case IDs → 1 CSV test case)

**Requirement Analysis:**

```
Scenario 3: User selects Screen Share button, loading functionality
- 3.1.1 Verify loading spinner displays
- 3.2.1 Verify "Loading ..." text displays
- 3.3.1 Verify loading UI matches Figma design
```

**CSV Test Case:**

```
"Verify Screen Share Modal Loading State"
Step 1: Navigate to workspace page → Workspace page displayed
Step 2: Click screen share icon → Modal begins to open
Step 3: Observe loading indicator → Loading spinner displays
Step 4: Observe loading text → "Loading ..." text displayed
Step 5: Compare with Figma design → Loading UI matches design specifications
```

### Example 3: Participant Display (6 test case IDs → 1 CSV test case)

**Requirement Analysis:**

```
Scenario 3: User on call with 1+ other users
- 3.1.1 Verify current user avatar displays
- 3.2.1 Verify current user name displays
- 3.3.1 Verify current user role displays
- 3.4.1 Verify other users' avatars display
- 3.5.1 Verify other users' names display
- 3.6.1 Verify other users' roles display
```

**CSV Test Case:**

```
"Verify Participants Tab Display When On Call With Multiple Users"
Step 1: Join or start call with 1+ participants → User on active call
Step 2: Open Participants tab → Participants tab opens
Step 3: Observe current user's information → Current user's avatar, name, role displayed
Step 4: Observe other participants' avatars → All other users' avatars displayed
Step 5: Observe other participants' names → All other users' names displayed
Step 6: Observe other participants' roles → All other users' roles displayed
```

### Example 4: Complete Workflow (5 test case IDs → 1 CSV test case)

**Requirement Analysis:**

```
Scenario 7: User selects screen
- 7.1.1 Verify user can select screen
- 7.2.1 Verify Share button available after selection
- 7.3.1 Verify screen shared when Share clicked
- 7.4.1 Verify shared screen displays as video feed
- 7.5.1 Verify shared screen visible to all users
```

**CSV Test Case:**

```
"Verify Share Screen Functionality"
Step 1: Open screen share modal → Modal displays with available screens
Step 2: Select a screen → Screen selected and highlighted
Step 3: Observe Share button → Share button available and enabled
Step 4: Click Share button → Share button clicked
Step 5: Verify screen shared for sharing user → Screen displays as video feed locally
Step 6: Verify screen shared for all participants → Shared screen visible to all on call
```

---

## Step 7: Maintaining Traceability

While you combine test case IDs into consolidated CSV test cases, maintain clear traceability:

1. **Each CSV test case should logically map back to specific scenarios** from the requirement analysis
2. **Test step sequences should cover all the test case IDs** that were combined
3. **Expected results should verify all the requirements** represented by those test case IDs

**Traceability Example:**

```
Requirements Analysis:
- 13 scenarios
- 43 requirements
- 43 test case IDs (1.1.1 through 13.3.1)

CSV Output:
- 13 test cases (combined from 43 test case IDs)
- Each CSV test case maps to 1-6 test case IDs
- All 43 test case IDs are covered
```

---

## Reference Examples

Study complete working examples in `.claude/skills/testcase-creator/examples/`:

1. **eNr_118557_Welcome-Log-In-Screen-Forms-Based-Authentication.TestCases.csv**
   - Shows component verification pattern (9 UI elements in one test case)
   - Demonstrates authentication workflows
   - Includes license-based behavior testing

2. **eNr_118559_Select-Patient-eNcounter-Cloud-Search.TestCases.csv**
   - Shows comprehensive search UI verification (15 elements combined)
   - Field validation patterns (separate test cases per field)
   - Data-driven testing approach

3. **eNr_121265_workspace-screen-share.TestCases.csv**
   - Modal workflow patterns
   - State transition testing
   - UI interaction sequences

4. **eNr_122019_encounter-refresh-user-directory-participants-tab.TestCases.csv**
   - State-based testing (not on call vs. on call)
   - Multiple user type handling
   - User role verification

5. **eNr_124798_app-loading-behavior.TestCases.csv**
   - Timing and performance testing
   - Error message verification
   - Retry behavior patterns

Each example demonstrates different combination strategies and test case patterns.

---

## Quality Checklist

Before finalizing your test cases:

- [ ] Every test case ID from requirement analysis is covered
- [ ] Related verifications are combined into logical test cases
- [ ] Separate user workflows remain separate test cases
- [ ] Test case titles clearly describe what is being tested
- [ ] Test steps follow a logical, executable sequence
- [ ] Step actions use clear, imperative language
- [ ] Expected results are specific and measurable
- [ ] Setup/navigation steps establish proper context
- [ ] Traceability to scenarios is maintained
- [ ] Test cases are efficient without sacrificing coverage
