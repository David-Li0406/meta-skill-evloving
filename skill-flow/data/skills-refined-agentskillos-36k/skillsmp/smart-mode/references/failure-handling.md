# Failure Handling Protocol

Comprehensive guide for detecting, recovering from, and documenting failures in Smart Ralph mode.

## Stuck Detection

### Automatic Detection Triggers

Smart Ralph detects "stuck" state when:

1. **Same Error Repeated**
   - Identical error message 3 consecutive times
   - Same test failing after 3 fix attempts
   - Same build error persisting

2. **No Progress**
   - No file changes in 5+ iterations
   - Same code being written/deleted repeatedly
   - Circular debugging (trying same fixes)

3. **Explicit Admission**
   - Statements like "I don't know how to..."
   - "I'm not sure what's causing..."
   - "I've tried everything I can think of..."

### Detection Implementation

Track in state.yaml:
```yaml
failure_recovery:
  consecutive_same_error: 0  # Reset on new error
  iterations_without_change: 0  # Reset on file change
  last_error_hash: ""  # Hash of error message
  last_file_state_hash: ""  # Hash of changed files
```

## Recovery Levels

### Level 1: PIVOT (Attempts 1-3)

**When:** First signs of being stuck

**Protocol:**
1. **Stop** - Don't continue same approach
2. **Analyze** - What specifically failed and why?
3. **List Alternatives** - Generate 2-3 different approaches
4. **Evaluate** - Which is most promising?
5. **Execute** - Try the new approach

**Example:**
```
PIVOT ACTIVATED (Attempt 1/3)

❌ Failed Approach: Using useState for form
   Error: "Too many re-renders"

Alternative Approaches:
1. Use useReducer instead of useState (most promising)
2. Debounce the onChange handler
3. Use uncontrolled components with refs

Trying: Approach 1 - useReducer
```

**State Update:**
```yaml
failure_recovery:
  pivot_count: 1
  current_strategy: "useReducer instead of useState"
  last_error: "Too many re-renders with useState"
```

### Level 2: RESEARCH (Attempts 4-6)

**When:** 3 pivot attempts failed

**Protocol:**
1. **Acknowledge** - Pivoting isn't working
2. **Gather Context** - Read more related code
3. **Find Patterns** - Look for similar solutions in codebase
4. **Understand Dependencies** - Map what affects what
5. **Reformulate** - Create new approach with deeper understanding

**Example:**
```
RESEARCH MODE ACTIVATED (Attempt 1/3)

Previous pivots failed:
1. useReducer → Same re-render issue
2. Debounce → Delayed user feedback, rejected
3. Refs → Lost validation state

Research Actions:
1. Reading existing form implementations in codebase...
   Found: src/components/UserForm.tsx uses react-hook-form

2. Checking form library dependencies...
   Found: react-hook-form already installed

3. Understanding validation patterns...
   Found: Zod schema validation in src/lib/validations/

New Approach: Use react-hook-form with Zod (matches existing patterns)
```

**State Update:**
```yaml
failure_recovery:
  pivot_count: 3
  research_count: 1
  research_findings:
    - "react-hook-form already in use"
    - "Zod validation patterns exist"
  current_strategy: "Adopt existing react-hook-form + Zod pattern"
```

### Level 3: CHECKPOINT (After 6 failed attempts)

**When:** 3 research attempts failed (total 6+ attempts)

**Protocol:**
1. **Accept** - This requires human intervention
2. **Document** - Write comprehensive stuck report
3. **Preserve State** - Save all context for resume
4. **Exit Gracefully** - Clear message about what's needed

**Example:**
```
CHECKPOINT - STUCK

After 6 recovery attempts, Smart Ralph cannot proceed autonomously.

Attempts Summary:
- 3 pivot attempts (different approaches)
- 3 research attempts (deeper investigation)

Stuck Report saved to: .claude/smart-ralph/stuck-report.md

What's Needed:
- Human review of form validation approach
- Decision on whether to use existing patterns or new library
- Possible architecture guidance

To resume: Run /auto-smart and it will continue from this checkpoint
```

## Stuck Report Format

When Level 3 is reached, create `.claude/smart-ralph/stuck-report.md`:

```markdown
# Smart Ralph - Stuck Report

**Generated:** 2024-01-15T10:30:00Z
**Task:** "Implement form validation for user registration"
**Phase:** EXECUTE (ORCHESTRATED Phase 2/3)

## Summary

Smart Ralph encountered an issue it couldn't resolve autonomously after 6 recovery attempts.

## What Was Attempted

### Original Approach
Used useState for form state management with inline validation.

### Pivot Attempts
1. **useReducer** - Still caused re-render issues
2. **Debounce handler** - User experience was poor
3. **Uncontrolled components** - Lost validation state

### Research Findings
1. Codebase uses react-hook-form in other forms
2. Zod schemas exist for validation
3. But UserForm pattern doesn't match new requirements

### Why It's Stuck
The existing patterns don't support the specific validation requirements:
- Cross-field validation (password confirmation)
- Async validation (email uniqueness check)
- Progressive disclosure (show fields based on selection)

## Current State

Files modified:
- src/components/RegisterForm.tsx (partial implementation)
- src/lib/validations/user.ts (schema created)

Tests status:
- 3 passing, 2 failing (validation tests)

## What Human Needs to Decide

1. Should we extend react-hook-form setup for async validation?
2. Is a different form library acceptable (Formik, Final Form)?
3. Should cross-field validation be server-side instead?

## How to Resume

Option 1: Provide guidance and run `/auto-smart` again
Option 2: Make the decision and run `/auto-smart "continue with [decision]"`
Option 3: Fix manually and clear `.claude/smart-ralph/` directory

## Full Error Log

```
Error in validation test:
  ✕ should validate password confirmation
    Expected: passwords must match
    Received: undefined

  ✕ should check email uniqueness
    Timeout: async validation not completing
```

## Context Files

- State: .claude/smart-ralph/state.yaml
- Progress: .claude/smart-ralph/progress.md
```

## Recovery State Machine

```
                    ┌──────────────────┐
                    │  Normal Execution │
                    └────────┬─────────┘
                             │
                    (stuck detected)
                             │
                             ▼
┌───────────────────────────────────────────────────┐
│                    PIVOT MODE                      │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐          │
│  │Attempt 1│ → │Attempt 2│ → │Attempt 3│          │
│  └────┬────┘   └────┬────┘   └────┬────┘          │
│       │success      │success      │success        │
│       ▼             ▼             ▼               │
│    (resume)      (resume)      (resume)           │
└───────────────────────┬───────────────────────────┘
                        │ all failed
                        ▼
┌───────────────────────────────────────────────────┐
│                   RESEARCH MODE                    │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐          │
│  │Attempt 1│ → │Attempt 2│ → │Attempt 3│          │
│  └────┬────┘   └────┬────┘   └────┬────┘          │
│       │success      │success      │success        │
│       ▼             ▼             ▼               │
│    (resume)      (resume)      (resume)           │
└───────────────────────┬───────────────────────────┘
                        │ all failed
                        ▼
┌───────────────────────────────────────────────────┐
│                   CHECKPOINT                       │
│                                                    │
│  • Write stuck-report.md                          │
│  • Save complete state                            │
│  • Output STUCK message                           │
│  • Exit gracefully                                │
└───────────────────────────────────────────────────┘
```

## Configuration

Maximum attempts can be configured in state.yaml:
```yaml
failure_recovery:
  max_pivot_attempts: 3  # default
  max_research_attempts: 3  # default
  max_total_attempts: 10  # hard limit
```

## Best Practices

### During PIVOT
- Don't repeat the same approach with minor tweaks
- Each pivot should be fundamentally different
- Document why each approach was chosen

### During RESEARCH
- Read at least 3 related files
- Look for existing patterns, don't invent new ones
- Understand the "why" not just the "what"

### Before CHECKPOINT
- Ensure all state is saved
- Document everything tried
- Make it easy for human to continue
- Suggest specific questions/decisions needed
