---
name: tasks
description: "Convert a PRD markdown file to prd.json for execution. Triggers on: convert prd, create tasks, prd to json, generate tasks from prd."
---

# Tasks - Convert PRD to JSON Format

Converts a PRD markdown document into the prd.json format for the execution loop.

---

## The Job

1. Read the PRD markdown file
2. Extract tasks (from Tasks section or User Stories)
3. **Explode each task into granular, machine-verifiable sub-tasks**
4. Order by dependencies (schema → backend → UI → tests)
5. Output to the specified prd.json location

**Autonomous mode:** Do not ask questions. Use the PRD content and any provided context (branch name, output path) to generate prd.json immediately.

---

## Critical: Agent-Testable Tasks

Every task must be **autonomously verifiable** by an AI agent without human intervention.

### The Golden Rule

Each acceptance criterion must be a **boolean check** that an agent can definitively pass or fail:

**❌ BAD - Vague/subjective:**
- "Works correctly"
- "Review the configuration"
- "Document the findings"
- "Identify the issue"
- "Verify it looks good"

**✅ GOOD - Machine-verifiable:**
- "Run `npm run typecheck` - exits with code 0"
- "Navigate to /signup - page loads without console errors"
- "Click submit button - form submits and redirects to /dashboard"
- "File `src/auth/config.ts` contains `redirectUrl: '/onboarding'`"
- "API response status is 200 and body contains `{ success: true }`"

### Acceptance Criteria Patterns

Use these patterns for agent-testable criteria:

| Type | Pattern | Example |
|------|---------|---------|
| Command | "Run `[cmd]` - exits with code 0" | "Run `npm test` - exits with code 0" |
| File check | "File `[path]` contains `[string]`" | "File `middleware.ts` contains `clerkMiddleware`" |
| Browser nav | "agent-browser: open `[url]` - [expected result]" | "agent-browser: open /login - SignIn component renders" |
| Browser action | "agent-browser: click `[element]` - [expected result]" | "agent-browser: click 'Submit' button - redirects to /dashboard" |
| Console check | "agent-browser: console shows no errors" | |
| API check | "GET/POST `[url]` returns `[status]` with `[body]`" | "POST /api/signup returns 200" |
| Screenshot | "agent-browser: screenshot shows `[element]` visible" | "agent-browser: screenshot shows CTA button above fold" |

### Browser Testing with agent-browser

All browser-based acceptance criteria MUST use [agent-browser](https://github.com/vercel-labs/agent-browser).

**agent-browser commands:**
```bash
agent-browser open <url>              # Navigate to URL
agent-browser snapshot -i             # Get interactive elements with refs
agent-browser click @ref              # Click element by ref
agent-browser fill @ref "value"       # Fill input field
agent-browser screenshot <path>       # Save screenshot
agent-browser wait --load networkidle # Wait for page load
agent-browser console                 # Check console for errors
```

**Example browser acceptance criteria:**
```json
{
  "acceptanceCriteria": [
    "agent-browser: open http://localhost:3000/signup - page loads",
    "agent-browser: snapshot -i - find email input field ref",
    "agent-browser: fill @email 'test@example.com' - value entered",
    "agent-browser: fill @password 'TestPass123!' - value entered", 
    "agent-browser: click @submit - form submits",
    "agent-browser: wait --load networkidle - page settles",
    "agent-browser: screenshot tmp/signup-result.png - capture result",
    "agent-browser: console - no errors logged"
  ]
}
```

---

## Input

A PRD file created by the `prd` skill, typically at `tasks/prd-[feature-name].md`.

---

## Output Format

Create `prd.json`:

```json
{
  "project": "Project Name",
  "branchName": "compound/[feature-name]",
  "description": "[One-line description from PRD]",
  "tasks": [
    {
      "id": "T-001",
      "title": "[Specific action verb] [specific target]",
      "description": "[1-2 sentences: what to do and why]",
      "acceptanceCriteria": [
        "Specific machine-verifiable criterion with expected outcome",
        "Another criterion with pass/fail condition",
        "Run `npm run typecheck` - exits with code 0"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## Task Granularity Rules

### Target: 8-15 tasks per PRD

PRDs should typically generate 8-15 granular tasks. If you have fewer than 6, you probably need to split tasks further.

### Split Multi-Step Tasks

**❌ TOO BIG:**
```json
{
  "title": "Test signup flow and fix issues",
  "acceptanceCriteria": [
    "Test the signup flow",
    "Identify any issues", 
    "Fix the issues",
    "Verify the fix works"
  ]
}
```

**✅ PROPERLY SPLIT:**
```json
[
  {
    "id": "T-001",
    "title": "Navigate to signup page and capture baseline",
    "acceptanceCriteria": [
      "Navigate to /signup - page loads successfully",
      "Screenshot saved to tmp/signup-baseline.png",
      "Browser console errors logged to tmp/signup-console.log"
    ]
  },
  {
    "id": "T-002", 
    "title": "Test email input field validation",
    "acceptanceCriteria": [
      "Enter 'invalid-email' in email field - error message appears",
      "Enter 'valid@example.com' - error message disappears",
      "Field has aria-invalid='true' when invalid"
    ]
  },
  {
    "id": "T-003",
    "title": "Test form submission with valid data",
    "acceptanceCriteria": [
      "Fill email: 'test@example.com', password: 'TestPass123!'",
      "Click submit button - loading state appears",
      "After submit - redirects to /onboarding OR error message appears"
    ]
  }
]
```

### One Concern Per Task

Each task should do ONE thing:

| Concern | Separate Task |
|---------|---------------|
| Navigate to page | T-001 |
| Check for errors | T-002 |
| Test input validation | T-003 |
| Test form submission | T-004 |
| Verify redirect | T-005 |
| Test mobile viewport | T-006 |
| Implement fix | T-007 |
| Verify fix on desktop | T-008 |
| Verify fix on mobile | T-009 |

### Investigation vs Implementation

**Never combine "find the problem" with "fix the problem"** in one task.

```json
[
  {
    "id": "T-001",
    "title": "Check Clerk SignUp component configuration",
    "description": "Verify the Clerk SignUp component props match expected values",
    "acceptanceCriteria": [
      "File app/(public)/free-trial/page.tsx exists",
      "File contains <SignUp component",
      "SignUp has routing prop (log value to notes)",
      "SignUp has forceRedirectUrl prop (log value to notes)",
      "Run `npm run typecheck` - exits with code 0"
    ]
  },
  {
    "id": "T-002",
    "title": "Check middleware auth configuration",
    "description": "Verify middleware doesn't block signup routes",
    "acceptanceCriteria": [
      "File middleware.ts exists",
      "Log public routes configuration to notes",
      "/free-trial is in public routes OR not blocked by auth",
      "Run `npm run typecheck` - exits with code 0"
    ]
  }
]
```

---

## Task Sizing

Each task must be completable in ONE iteration (~one context window).

**Right-sized tasks:**
- Check one configuration file for specific values
- Test one user interaction (click, type, submit)
- Verify one redirect or navigation
- Change one prop or configuration value
- Add one CSS rule or style change
- Test one viewport size

**Too big (split these):**
- "Test the entire signup flow" → Split into: load page, test inputs, test submit, test redirect, test mobile
- "Fix the bug" → Split into: identify file, make change, verify change, test regression
- "Add authentication" → Split into: schema, middleware, login UI, session handling

---

## Priority Ordering

Set priority based on dependencies:

1. **Investigation tasks** - priority 1-3 (understand before changing)
2. **Schema/database changes** - priority 4-5
3. **Backend logic changes** - priority 6-7
4. **UI component changes** - priority 8-9
5. **Verification tasks** - priority 10+

Lower priority number = executed first.

---

## Process

### Step 1: Read the PRD

```
Read the PRD file the user specified
```

### Step 2: Extract High-Level Tasks

Look for:
- Tasks (T-001, T-002, etc.)
- User Stories (US-001, US-002, etc.)
- Functional Requirements (FR-1, FR-2, etc.)
- Any numbered/bulleted work items

### Step 3: Explode Into Granular Tasks

For each high-level task:
1. List every distinct action required
2. Separate investigation from implementation
3. Separate each verification concern
4. Ensure each has boolean pass/fail criteria

### Step 4: Order by Dependencies

Determine logical order:
1. What needs to be understood first? (investigation)
2. What needs to exist first? (database schema)
3. What depends on that? (backend logic)
4. What depends on that? (UI components)
5. What verifies everything? (browser tests)

### Step 5: Generate prd.json

Create the JSON file with all tasks having `passes: false`.

### Step 6: Save and Summarize

Save the file immediately, then output a brief summary:
- Number of tasks created
- Task order with priorities
- Branch name
- File path saved to

**Do NOT wait for user confirmation.** Save the file and proceed.

---

## Example: Debugging a Broken Page

**PRD Task:**
```markdown
### T-001: Fix signup page with 0% conversion
- Test the signup flow
- Identify the bug
- Fix it
- Verify on mobile and desktop
```

**Exploded to prd.json (10 tasks):**
```json
{
  "project": "MyProject",
  "branchName": "compound/fix-signup",
  "description": "Fix broken signup page",
  "tasks": [
    {
      "id": "T-001",
      "title": "Load signup page and check for errors",
      "acceptanceCriteria": [
        "Navigate to /signup - page loads (status 200)",
        "Screenshot saved to tmp/signup-desktop.png",
        "Console errors saved to notes field (or 'none' if clean)"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-002",
      "title": "Test signup page on mobile viewport",
      "acceptanceCriteria": [
        "Set viewport to 375x812 (iPhone)",
        "Navigate to /signup - page loads",
        "Screenshot saved to tmp/signup-mobile.png",
        "CTA button visible in screenshot (not below fold)"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-003",
      "title": "Test email input field",
      "acceptanceCriteria": [
        "Email input field exists and is interactable",
        "Type 'test@example.com' - value appears in field",
        "No console errors after typing"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-004",
      "title": "Test password input field",
      "acceptanceCriteria": [
        "Password input field exists and is interactable",
        "Type 'TestPassword123!' - value appears (masked)",
        "No console errors after typing"
      ],
      "priority": 4,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-005",
      "title": "Test form submission",
      "acceptanceCriteria": [
        "Click submit button - button responds to click",
        "Loading state appears OR form submits",
        "Log result to notes: success redirect URL or error message"
      ],
      "priority": 5,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-006",
      "title": "Inspect SignUp component configuration",
      "acceptanceCriteria": [
        "Read file containing SignUp component",
        "Log routing prop value to notes",
        "Log forceRedirectUrl prop value to notes",
        "Log any other relevant props to notes"
      ],
      "priority": 6,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-007",
      "title": "Check middleware route protection",
      "acceptanceCriteria": [
        "Read middleware.ts file",
        "Log public routes array to notes",
        "Confirm /signup is accessible without auth"
      ],
      "priority": 7,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-008",
      "title": "Implement fix based on findings",
      "acceptanceCriteria": [
        "Review notes from T-001 through T-007",
        "Make targeted code change to fix identified issue",
        "Run `npm run typecheck` - exits with code 0",
        "Run `npm test` - exits with code 0"
      ],
      "priority": 8,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-009",
      "title": "Verify fix on desktop",
      "acceptanceCriteria": [
        "Navigate to /signup",
        "Complete full signup with test credentials",
        "Redirect occurs to expected URL",
        "No console errors during flow"
      ],
      "priority": 9,
      "passes": false,
      "notes": ""
    },
    {
      "id": "T-010",
      "title": "Verify fix on mobile",
      "acceptanceCriteria": [
        "Set viewport to 375x812",
        "Navigate to /signup",
        "Complete full signup with test credentials",
        "Redirect occurs to expected URL"
      ],
      "priority": 10,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## Checklist

Before saving prd.json:

- [ ] **8-15 tasks** generated (not 3-5)
- [ ] Each task does **ONE thing**
- [ ] Investigation separated from implementation
- [ ] Every criterion is **boolean pass/fail**
- [ ] No vague words: "review", "identify", "document", "verify it works"
- [ ] Commands specify expected exit code
- [ ] Browser actions specify expected result
- [ ] All tasks have `passes: false`
- [ ] Priority order reflects dependencies
