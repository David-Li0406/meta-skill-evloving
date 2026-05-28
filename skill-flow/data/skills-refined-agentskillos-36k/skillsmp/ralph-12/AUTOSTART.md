# Ralph Auto-Start & Validation Loop

## Full Automated Flow

```
User: /ralph "build login page with tests"
         │
         ▼
┌─────────────────────────────────────────┐
│  CLORCH: Setup                          │
│  - Analyze codebase                     │
│  - Decompose tasks                      │
│  - Generate .ralph/ files               │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  CLORCH: "Ready to start Ralph?"        │
│  [Approve] [Modify] [Cancel]            │
└─────────────────────────────────────────┘
         │ User approves
         ▼
┌─────────────────────────────────────────┐
│  CLORCH: Auto-start                     │
│  ~/.claude/ralph-docker/                │
│    start-ralph-terminal.sh              │
│                                         │
│  Opens new Terminal window              │
│  Starts ralph-loop-host.sh              │
└─────────────────────────────────────────┘
         │
         ▼ (In new terminal)
┌─────────────────────────────────────────┐
│  RALPH LOOP: Executes                   │
│  Fresh Claude per iteration             │
│  ... tasks completing ...               │
└─────────────────────────────────────────┘
         │
         ▼ (User returns to Clorch)
┌─────────────────────────────────────────┐
│  User: /ralph validate                  │
│                                         │
│  CLORCH: Validates                      │
│  - Run test suite                       │
│  - Visual verification (Playwright)    │
│  - Check for regressions                │
└─────────────────────────────────────────┘
         │
         ├─ All pass → /ralph summary
         │
         └─ Failures found
                 │
                 ├─ Simple fix → Clorch fixes directly
                 │
                 └─ Complex fix → Add guardrail, restart Ralph
```

---

## Auto-Start Command

### Usage

```bash
# Clorch generates files, then auto-starts:
~/.claude/ralph-docker/start-ralph-terminal.sh /path/to/project 20
```

### What It Does

1. Opens a new Terminal window (macOS) or terminal emulator (Linux)
2. Changes to project directory
3. Starts `ralph-loop-host.sh` with specified iterations
4. User can monitor in that terminal

### Clorch Integration

After `/ralph "goal"` setup:

```
Ralph setup complete!

Files created in .ralph/
- task.md: 8 tasks
- prompt.md: Static instructions
- guardrails.md: 3 initial guardrails

[Start Ralph automatically?]
- Yes, open terminal and start (recommended)
- No, I'll start manually
```

If "Yes":
```bash
~/.claude/ralph-docker/start-ralph-terminal.sh "$(pwd)" 20
```

---

## Validation Workflow (`/ralph validate`)

### What Clorch Validates

1. **Test Suite**
   ```bash
   npm test
   npx playwright test
   ```

2. **Visual Verification** (using Playwright MCP)
   ```
   - Navigate to pages
   - Take screenshots
   - Compare with expectations
   - Check for visual regressions
   ```

3. **Functional Verification**
   ```
   - Click buttons
   - Fill forms
   - Verify responses
   ```

### Validation Output

```markdown
## Validation Results

### Tests
✓ Unit tests: 45/45 passing
✓ Integration tests: 12/12 passing
✗ E2E tests: 8/10 passing (2 failures)

### Visual Check
✓ Login page renders correctly
✓ Dashboard loads
✗ Profile page has layout issue

### Failures Found

1. **E2E: Profile update fails**
   - Error: "Save button not responding"
   - File: src/components/Profile.tsx
   - Severity: Medium

2. **Visual: Profile layout**
   - Issue: Sidebar overlaps content
   - File: src/components/Profile.tsx
   - Severity: Low

### Recommendation

- Failure 1: Complex (event handler issue) → Send to Ralph
- Failure 2: Simple (CSS fix) → Clorch can fix directly

[Fix simple issues now?] [Send all to Ralph?] [Review manually?]
```

---

## Quick Fix by Clorch

When validation finds a simple issue:

```
Clorch: "Found CSS issue in Profile.tsx - sidebar width"
        This is a 1-line fix. Should I fix it directly?

        [Yes, fix it] [Send to Ralph] [Show me first]
```

If "Yes, fix it":
```typescript
// Clorch edits directly
- className="w-64"
+ className="w-64 shrink-0"
```

---

## Feedback Loop to Ralph

When validation finds complex issues:

1. **Add guardrail** to `.ralph/guardrails.md`:
   ```markdown
   ## Sign: Profile save handler
   - Trigger: Editing Profile component
   - Issue: onClick handler not bound correctly
   - Fix: Use arrow function or bind in constructor
   - Added: Validation failure 2026-01-22
   ```

2. **Add fix task** to `.ralph/task.md`:
   ```markdown
   ### Fix Profile Save Button
   - description: Fix onClick handler in Profile.tsx (see guardrail)
   - validation: `npx playwright test --grep "profile save"`
   - passes: false
   ```

3. **Restart Ralph**:
   ```bash
   ~/.claude/ralph-docker/start-ralph-terminal.sh "$(pwd)" 5
   ```

---

## Full Cycle Example

```
User: /ralph "add user profile page"

Clorch: [Setup complete - 6 tasks]
        Start Ralph? [Yes]

        → Opens terminal, Ralph runs
        → 6 tasks complete

User: /ralph validate

Clorch: [Running validation...]

        Tests: 42/45 passing (3 failures)
        Visual: 2 issues found

        Simple fixes (Clorch can handle):
        - CSS margin issue in ProfileHeader

        Complex fixes (Ralph needed):
        - Form validation not working
        - API error handling missing

        [Fix simple, send complex to Ralph?]

User: Yes

Clorch: → Fixes CSS directly
        → Adds 2 guardrails
        → Adds 2 tasks to task.md
        → Restarts Ralph in terminal

        Ralph running (2 remaining tasks)...

User: /ralph validate

Clorch: All tests passing!
        Visual check: OK

        Ready for /ralph summary
```
