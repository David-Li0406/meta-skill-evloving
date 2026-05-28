# Issue Evaluation Criteria

## Evaluation Framework

When Codex reports an issue, evaluate it against these criteria before acting.

## Valid Issue Indicators

### Definitely Fix

**Runtime Impact:**
- Code will crash or throw exception
- Incorrect output produced
- Data corruption possible
- Memory leak or resource exhaustion

**Security Concerns:**
- User input reaches dangerous sink without sanitization
- Authentication or authorization bypass
- Sensitive data exposure
- Injection vulnerability (SQL, command, LDAP)

**Logic Errors:**
- Off-by-one errors in loops
- Incorrect boolean logic
- Missing null/undefined checks on external data
- Race conditions with shared state

**API Contract Violations:**
- Breaking changes to public interfaces
- Missing required fields in responses
- Type mismatches in contracts

### Examples of Valid Issues

```csharp
// VALID: SQL Injection
var query = $"SELECT * FROM users WHERE id = {userId}"; // Untrusted input

// VALID: Null reference
var name = user.Profile.Name; // Profile could be null

// VALID: Logic error
if (count > 0 || count < 10) // Should be && not ||

// VALID: Resource leak
var stream = File.OpenRead(path); // Never disposed
```

## False Positive Indicators

### Intentional Design

- Behavior is documented as intentional
- Code comments explain the reasoning
- Team style guide allows the pattern
- Performance tradeoff was considered

### Context Misunderstanding

- Codex doesn't see the full picture
- Variable is validated elsewhere
- Framework guarantees safety
- Test environment only

### Style Preferences

- Different but valid approach
- No functional impact
- Readable and maintainable
- Follows project conventions

### Examples of False Positives

```csharp
// FALSE POSITIVE: Intentional nullable
string? optionalName = null; // By design, represents absence

// FALSE POSITIVE: Framework handles it
[Required]
public string Email { get; set; } // ModelState validates

// FALSE POSITIVE: Validated upstream
public void Process(User user) // Caller guarantees non-null

// FALSE POSITIVE: Style choice
var x = items.FirstOrDefault() ?? defaultItem; // Valid pattern
```

## Evaluation Decision Tree

```
Issue Reported
    |
    v
Does it affect runtime behavior?
    |-- No --> Likely false positive (style issue)
    |-- Yes --> Continue
    v
Is there documented intent for this pattern?
    |-- Yes --> False positive (intentional design)
    |-- No --> Continue
    v
Is the concern handled elsewhere in code?
    |-- Yes --> False positive (context not seen)
    |-- No --> Continue
    v
Does the framework/library handle this case?
    |-- Yes --> False positive (framework guarantee)
    |-- No --> VALID ISSUE - Fix it
```

## Handling Edge Cases

### "It works in practice"

Even if code works in current usage, fix issues that could fail with:
- Different inputs
- Concurrent execution
- Future modifications

### "It's test code"

Apply lighter standards to test code, but still fix:
- Security issues (credentials, injection)
- Flaky test causes
- Resource leaks that affect CI

### "It's legacy code"

For legacy code:
- Fix critical and high severity
- Document medium severity for future
- Skip low severity unless refactoring

### "Time pressure"

Under deadlines:
1. Fix all critical issues (non-negotiable)
2. Fix high severity if any
3. Document medium/low for follow-up

## Resolution Workflow

### For Valid Issues

1. **Read Context**
   - Open the file
   - Understand surrounding code
   - Check for related patterns

2. **Determine Fix**
   - Use suggested fix if appropriate
   - Or design better solution
   - Follow project conventions

3. **Apply Fix**
   - Make minimal necessary change
   - Don't refactor unrelated code
   - Preserve existing tests

4. **Verify**
   - Compile/build succeeds
   - Tests pass
   - Re-run review on changed files

### For False Positives

1. **Document Decision**
   - Note why issue is false positive
   - Add code comment if pattern repeats

2. **Consider Improvement**
   - Could code be clearer?
   - Would comment help future reviewers?

3. **Move On**
   - Don't spend time on non-issues
   - Focus on valid findings

## Priority Matrix

| Severity | Valid Issue | False Positive |
|----------|-------------|----------------|
| Critical | Fix immediately | Document why ignored |
| High | Fix before merge | Review decision |
| Medium | Fix if time | Skip |
| Low | Consider | Skip |

## Team Calibration

To reduce false positives over time:

1. Track patterns that are consistently false positives
2. Add to custom review instructions as exclusions
3. Create CODEX.md file with project context
4. Share evaluation decisions across team

Example CODEX.md addition:
```markdown
## Review Guidelines

Ignore these patterns:
- Nullable reference types are intentional in DTOs
- async void is acceptable in event handlers
- FirstOrDefault without null check is OK when collection guaranteed non-empty
```
