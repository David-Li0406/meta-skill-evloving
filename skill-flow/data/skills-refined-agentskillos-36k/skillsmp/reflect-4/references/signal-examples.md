# Signal Detection Examples

This document provides detailed examples for identifying signals during conversation analysis.

## External Feedback (HIGH Confidence) ⭐ NEW

**IMPORTANT**: External feedback provides objective evidence and should be prioritized over conversation signals.

These are automated signals from test suites, linters, type checkers, and build systems.

### Examples from Pytest:
- **Test failure**:
  - `FAILED tests/test_component.py::test_accessibility - AssertionError: missing aria-label on input`
  - **Signal**: Skill generated code missing accessibility attributes
  - **Confidence**: HIGH (objective failure)

- **Assertion error**:
  - `AssertionError: Expected dark mode toggle, got None`
  - **Signal**: Skill didn't include requested feature
  - **Confidence**: HIGH (test explicitly checks for feature)

### Examples from Ruff (Python Linter):
- **Unused import**:
  - `src/api.py:15:1: F401 'os' imported but unused`
  - **Signal**: Skill added unnecessary imports
  - **Confidence**: HIGH (objective lint rule)

- **Line too long**:
  - `src/components/Button.py:42:121: E501 line too long (135 > 120 characters)`
  - **Signal**: Skill doesn't follow line length conventions
  - **Confidence**: HIGH (style guide violation)

### Examples from MyPy (Type Checker):
- **Type error**:
  - `error: Argument 1 to "process" has incompatible type "str"; expected "int"`
  - **Signal**: Skill generated incorrect type usage
  - **Confidence**: HIGH (type safety violation)

- **Missing return type**:
  - `error: Function is missing a return type annotation`
  - **Signal**: Skill doesn't add type hints
  - **Confidence**: HIGH (type annotation requirement)

### Examples from ESLint (JavaScript Linter):
- **Undefined variable**:
  - `error: 'userName' is not defined  no-undef`
  - **Signal**: Skill referenced non-existent variable
  - **Confidence**: HIGH (runtime error risk)

- **Missing key prop**:
  - `warning: Missing "key" prop for element in iterator  react/jsx-key`
  - **Signal**: Skill doesn't follow React best practices
  - **Confidence**: HIGH (React requirement)

### Examples from Build Failures:
- **Compilation error**:
  - `error TS2339: Property 'username' does not exist on type 'User'`
  - **Signal**: Skill used non-existent property
  - **Confidence**: HIGH (won't compile)

- **Module not found**:
  - `ModuleNotFoundError: No module named 'requests'`
  - **Signal**: Skill didn't include dependency
  - **Confidence**: HIGH (missing dependency)

### When to Use External Feedback:
- ✅ After skill generates code
- ✅ When tests fail
- ✅ When linter reports errors
- ✅ When build fails
- ✅ When type checker reports issues

### How to Capture:
During the reflect workflow, include external feedback in your signal detection by noting:
- Test failures and their messages
- Linter warnings and errors
- Build failures and their causes
- Type checker reports

### Impact on Proposals:
External feedback becomes HIGH-confidence signals in proposals:

```
🔴 HIGH: Add constraint - "All interactive elements must have aria-labels"
   Evidence: 3 test failures in test_accessibility.py

🔴 HIGH: Add preference - "Avoid unused imports"
   Evidence: 5 ruff F401 errors across generated files

🔴 HIGH: Update guideline - "Include type hints for all functions"
   Evidence: 12 mypy errors about missing return types
```

---

## Corrections (HIGH Confidence)

These are strong negative signals indicating the skill did something wrong or unexpected.

### Examples:
- **User said "no"**: Direct rejection of output
  - "No, that's not what I meant"
  - "No, don't do it that way"

- **User said "not like that"**: Correction of approach
  - "Not like that, I want..."
  - "That's not right, instead..."

- **User said "I meant..."**: Clarification after misunderstanding
  - "I meant to say..."
  - "What I meant was..."

- **Explicit correction**: User directly fixes output
  - "Actually, it should be X not Y"
  - "Change that to..."

- **Immediate change request**: User asks for changes right after generation
  - User: "Add feature X"
  - Claude: [generates code]
  - User: "No, change it to Y" ← CORRECTION

### Counter-Examples (NOT Corrections):
- User asking follow-up questions (this is exploration, not correction)
- User requesting additional features (this is extension, not correction)
- User preferring a different approach for next time (this is preference, not correction)

## Successes (MEDIUM Confidence)

These are positive signals indicating the skill worked well.

### Examples:
- **User said "perfect"**: Explicit approval
  - "Perfect, thanks!"
  - "That's perfect"

- **User said "great"**: Positive feedback
  - "Great, exactly what I needed"
  - "Great work"

- **User said "yes"**: Confirmation/approval
  - "Yes, that's right"
  - "Yes, do it"

- **User said "exactly"**: Precise match to intent
  - "Exactly what I wanted"
  - "Exactly, thanks"

- **User accepted output**: No changes requested
  - Claude: [generates code]
  - User: "Now let's move on to..." ← ACCEPTED

- **User built on output**: Used it as foundation
  - Claude: [generates component]
  - User: "Now add a button to that component" ← BUILT ON

### Counter-Examples (NOT Successes):
- User silence (could mean anything - don't assume success)
- User saying "OK" without context (could be neutral acknowledgment)
- User moving on quickly (might have accepted suboptimal solution)

## Edge Cases (MEDIUM Confidence)

These are scenarios the skill didn't anticipate or handle well.

### Examples:
- **Unanticipated questions**: User asks something the skill didn't prepare for
  - Skill shows UI, user asks "How do I make this accessible?"
  - Skill wasn't designed to address accessibility

- **Workarounds needed**: Skill couldn't handle directly, user had to adapt
  - User: "Generate form validation"
  - Claude: [generates basic validation]
  - User: "How do I add custom validators?" ← Skill didn't cover this

- **Features not covered**: User expects feature, skill doesn't provide
  - User: "Add dark mode"
  - Claude: [adds toggle]
  - User: "What about system preference detection?" ← Not covered

- **Scope gaps**: Task requires knowledge skill doesn't have
  - User: "Optimize database query"
  - Claude: [suggests basic optimization]
  - User: "What about query plan analysis?" ← Beyond skill scope

### Counter-Examples (NOT Edge Cases):
- User asking for new features (this is normal evolution)
- User exploring "what if" scenarios (this is discovery, not gap)
- User requesting optional enhancements (this is extension, not edge case)

## Preferences (LOW Confidence - Accumulate)

These are patterns that emerge over multiple sessions, not single signals.

### Examples:
- **Repeated tool choices**: User always picks same library
  - Session 1: "Use React Query"
  - Session 2: "Use React Query"
  - Session 3: "Use React Query" ← PATTERN

- **Style consistency**: User always prefers certain style
  - Always asks for TypeScript strict mode
  - Always prefers CSS-in-JS over separate files
  - Always wants tests with each feature

- **Framework preferences**: User gravitates to specific approaches
  - Always chooses composition over inheritance
  - Always prefers functional over class components
  - Always uses GraphQL over REST

### Counter-Examples (NOT Preferences):
- One-time choices (not enough data for pattern)
- Context-dependent decisions (not consistent preference)
- Experimental explorations (not established pattern)

## Signal Counting Guidelines

**For each signal type, count distinct occurrences:**
- Multiple "no" responses to same issue = 1 correction
- User says "perfect" then "great" about same output = 1 success
- Three related edge cases in same feature = 3 edge cases (count separately)

**Weight by confidence:**
- HIGH (Corrections): Direct evidence, count every instance
- MEDIUM (Successes, Edge Cases): Good evidence, count conservatively
- LOW (Preferences): Weak evidence, need multiple sessions to establish

**Track session-to-session:**
- Same correction appearing again = edge case the last fix didn't solve
- Same success pattern = validation that approach works
- New edge case in familiar area = skill scope needs expansion
