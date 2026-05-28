# Command Accuracy Analyzer

## Overview

This analyzer helps identify failed commands and error patterns to improve first-attempt success rate and reduce wasted time on retries.

## Error Categories

### 1. Path Errors

**Common Issues:**

❌ **Incorrect file paths**
- File doesn't exist at specified path
- Wrong directory structure assumption
- Typo in file name

❌ **Backslash vs forward slash (Windows)**
- Using `app\ui\...` instead of `app/ui/...`
- Path works on Windows cmd but fails in tools
- Always use forward slashes for cross-platform compatibility

❌ **Case sensitivity issues**
- `App/UI` vs `app/ui`
- Especially important on Linux systems
- Match exact case from Glob results

❌ **Missing directory verification**
- Assuming directory exists
- Not checking parent path before creating files
- Should use ls or Glob to verify

**Prevention Strategies:**
- Always use forward slashes in paths
- Use Glob to verify file exists before Read/Edit
- Match exact case from file system
- Check parent directory exists before Write

### 2. Syntax Errors

**Common Issues:**

❌ **Invalid tool parameters**
- Missing required parameters
- Wrong parameter type (string vs number)
- Invalid parameter value

❌ **Malformed regex patterns**
- Unescaped special characters
- Invalid regex syntax
- Missing delimiters

❌ **Type mismatches**
- Passing string when number expected
- Wrong interface shape
- Missing required properties

❌ **String matching errors in Edit**
- old_string doesn't match exactly
- Whitespace differences
- Line ending differences

**Prevention Strategies:**
- Validate tool parameters before calling
- Test regex patterns incrementally
- Read type definitions before implementing
- Copy exact strings from Read output for Edit

### 3. Permission Errors

**Common Issues:**

❌ **Unauthorized operations**
- Trying to modify protected files
- Accessing restricted directories
- Operating outside sandbox

❌ **Missing tool permissions**
- Tool not available in current context
- Operation requires elevated permissions
- Sandbox restrictions

❌ **Read-only file system**
- Trying to write to read-only location
- Modifying files in node_modules
- Changing generated files

**Prevention Strategies:**
- Understand tool permissions
- Stay within project boundaries
- Avoid modifying generated/dependency files
- Check file permissions before operations

### 4. Logic Errors

**Common Issues:**

❌ **Wrong assumptions about file structure**
- Assuming file organization
- Incorrect understanding of codebase
- Missing intermediate directories

❌ **Incorrect API usage**
- Wrong import path
- Using deprecated API
- Missing required setup

❌ **Type/Interface mismatches**
- Wrong property names
- Incorrect data structure
- Missing required fields

❌ **Race conditions**
- Reading before write completes
- Dependent operations not sequenced
- Parallel calls that should be sequential

**Prevention Strategies:**
- Use Explore agent to understand structure
- Check existing code for patterns
- Read interface definitions first
- Sequence dependent operations

## Severity Levels

### Critical (10-point deduction)
- Blocked progress for >10 minutes
- Required significant rework
- Cascaded into multiple errors
- Example: Wrong data model assumption requiring refactor

### High (5-point deduction)
- Caused noticeable delay
- Needed multiple retry attempts
- Required user intervention
- Example: Import path error in 3 files

### Medium (2-point deduction)
- Minor delay
- Fixed on first retry
- Single occurrence
- Example: Typo in file path

### Low (0-point deduction)
- Caught immediately
- No retry needed
- Proactively prevented
- Example: TypeScript error caught before runtime

## Accuracy Scoring (0-100)

### Base Score Calculation

```
Success Rate = (Successful Commands / Total Commands) × 100
```

### Adjustments

| Factor | Adjustment | Notes |
|--------|------------|-------|
| Critical failure | -10 points | Per critical error |
| High severity failure | -5 points | Per high severity error |
| Medium severity failure | -2 points | Per medium severity error |
| Quick recovery (1 retry) | +2 points | Fixed immediately |
| Proactive error prevention | +5 points | Caught before execution |
| Used verification step | +3 points | Glob before Read, etc. |

### Final Score

```
Base Success Rate = (Successful / Total) × 100
Adjusted Score = Base Rate + Bonuses - Severity Penalties
Final Score = max(0, min(100, Adjusted Score))
```

**Score Interpretation:**
- 95-100: Excellent accuracy
- 85-94: Good accuracy with minor issues
- 70-84: Moderate accuracy, room for improvement
- 50-69: Below average, frequent errors
- 0-49: Poor accuracy, significant issues

## Report Format

When analyzing command accuracy, generate a report with this structure:

```markdown
### Command Accuracy Analysis

**Total Commands:** XXX
**Success Rate:** YY.Y%
**Failed Commands:** ZZ (Z.Z%)

#### Failure Breakdown:
| Error Type | Count | Percentage |
|------------|-------|------------|
| Path errors | X | XX% |
| Syntax errors | X | XX% |
| Permission errors | X | XX% |
| Logic errors | X | XX% |

#### Recurring Issues:

1. ⚠️ **[Error Type]** (X occurrences)
   - Root cause: [Analysis of why this happened]
   - Example: [Specific instance from session]
   - Prevention: [How to avoid in future]
   - Impact: [Severity and consequences]

2. ⚠️ **[Error Type]** (X occurrences)
   - Root cause: [Analysis]
   - Example: [Instance]
   - Prevention: [Strategy]
   - Impact: [Severity]

[Continue for top 3 issues]

#### Improvements from Previous Sessions:

1. ✅ **[Improvement]**: [What was learned/applied]
2. ✅ **[Improvement]**: [What worked well]

[Note positive patterns]
```

## Analysis Guidelines

### How to Analyze

1. **Review all tool calls**
   - Identify failed operations
   - Note error messages
   - Track retry attempts
   - Categorize by error type

2. **Calculate metrics**
   - Count total commands
   - Count successful commands
   - Count failed commands
   - Calculate success rate

3. **Identify patterns**
   - Find recurring error types
   - Spot common root causes
   - Note severity levels
   - Track time wasted

4. **Prioritize issues**
   - Focus on most frequent
   - Consider severity impact
   - Look for teachable patterns
   - Limit to top 3 issues

5. **Generate recommendations**
   - Be specific about prevention
   - Include concrete examples
   - Suggest verification steps
   - Acknowledge improvements

### Limit to Top 3

Only report the **3 most important** recurring issues:
- Prioritize by frequency × severity
- Focus on preventable patterns
- Skip one-off mistakes
- Emphasize learnings

### Be Constructive

- Use ⚠️ for issues, ✅ for improvements
- Explain root cause clearly
- Provide actionable prevention steps
- Recognize when patterns improve
- Focus on continuous learning

## Examples

### Example 1: Import Path Errors

❌ **Pattern Detected:**
```
Error in auto-assign/route.ts: Cannot find module '@/lib/auth'
Error in [id]/lock/route.ts: Cannot find module '@/lib/auth'
Fixed: Changed to '@/lib/authz'
```

**Analysis:**
- Error Type: Path error (import)
- Occurrences: 2
- Severity: Medium (fixed on first retry)
- Root Cause: Assumed wrong import path without checking existing code
- Time Wasted: ~2 minutes

**Report Entry:**
```markdown
⚠️ **Import Path Errors** (2 occurrences)
- Root cause: Assumed `@/lib/auth` without checking existing imports in similar files
- Example: Both auto-assign and lock APIs used wrong import initially
- Prevention: Always grep for existing imports in similar files first (e.g., `grep "requireRole" app/ui/app/api`)
- Impact: Medium - Required retry but fixed quickly
```

### Example 2: Type Interface Mismatch

❌ **Pattern Detected:**
```
Error: Type 'Room[]' is not assignable. Property 'currentCount' is missing
Expected: _count.studentAssignments
Used: currentCount
```

**Analysis:**
- Error Type: Logic error (type mismatch)
- Occurrences: 1
- Severity: High (required interface refactoring)
- Root Cause: Didn't read component interface before implementing
- Time Wasted: ~5 minutes

**Report Entry:**
```markdown
⚠️ **Type Interface Mismatch** (1 occurrence)
- Root cause: AutoAssignDialog expected `currentCount` but grades page uses `_count.studentAssignments`
- Example: Had to refactor interface to match existing pattern in codebase
- Prevention: Read component props/interfaces before implementing new components
- Impact: High - Required interface changes and testing
```

### Example 3: Good Pattern - Verification

✅ **Good Pattern Detected:**
```
Used Glob to find files matching "room-assignment*"
Then Read specific file found
No path errors
```

**Analysis:**
- Good Practice: Verified file exists before Read
- Prevented: Potential path errors
- Pattern: Search → Verify → Read

**Report Entry:**
```markdown
✅ **Proactive Verification**: Used Glob to find files before Reading
- Searched for pattern first to verify file paths
- Then read confirmed files
- Prevented potential path errors
```

## Common Error Patterns by Tool

### Read Tool
- File path doesn't exist
- Wrong directory structure
- Case sensitivity issues

### Edit Tool
- old_string doesn't match exactly (whitespace)
- old_string not unique in file
- File changed since last read

### Write Tool
- Parent directory doesn't exist
- File already exists (should use Edit)
- Permission issues

### Grep Tool
- Invalid regex syntax
- Unescaped special characters
- Wrong file type filter

### Glob Tool
- Invalid pattern syntax
- Too broad pattern (performance)
- Case sensitivity issues

### Bash Tool
- Command not found
- Permission denied
- Syntax errors in command

## Prevention Checklist

Before executing commands, verify:

**For Read/Edit/Write:**
- [ ] File path uses forward slashes
- [ ] Parent directory exists (if Write)
- [ ] File exists (if Read/Edit)
- [ ] Case matches exactly

**For Edit:**
- [ ] Have recent Read of the file
- [ ] old_string copied exactly from Read output
- [ ] old_string is unique in file (or using replace_all)

**For Grep/Glob:**
- [ ] Regex syntax is valid
- [ ] Special characters are escaped if literal
- [ ] Pattern is appropriately scoped

**For API/TypeScript:**
- [ ] Checked existing imports in similar files
- [ ] Read interface definitions
- [ ] Verified property names exist
- [ ] Confirmed type compatibility

## Tracking Improvements

Compare session to session:

**Metrics to Track:**
- Overall success rate
- Errors per category
- Average severity
- Time wasted on failures
- Proactive prevention instances

**Goal:**
- Increase success rate over time
- Reduce high-severity errors
- Build better verification habits
- Learn from recurring patterns
