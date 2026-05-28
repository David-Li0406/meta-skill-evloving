# AI Slop Removal

Removes AI-generated code artifacts that don't match human coding patterns.

## Patterns to Remove

### Excessive Comments
- Comments explaining obvious code (`// increment counter`, `// return the result`)
- Redundant JSDoc for simple functions with clear names
- Comments that restate what code does rather than why
- Block comments before every function when surrounding code has none

### Unnecessary Defensive Checks
- Null checks on values guaranteed by the type system
- Try/catch blocks around code that can't throw
- Redundant validation on already-validated inputs
- Optional chaining (`?.`) where values are always defined
- Default values for required parameters

### Type Workarounds
- Casts to `any` to silence type errors
- `as unknown as T` double casts
- `@ts-ignore` or `@ts-expect-error` comments
- Overly broad type assertions

### Style Inconsistencies
- Different quote styles than rest of file
- Inconsistent semicolon usage
- Different indentation or spacing patterns
- Variable naming that doesn't match file conventions
- Overly verbose variable names when surrounding code is concise

### Over-Engineering
- Unnecessary abstractions for single-use code
- Configuration objects where simple parameters would do
- Factory functions that create one thing
- Wrapper functions that just call another function

## Detection Strategy

Compare to surrounding code. The key indicator of slop is inconsistency with the existing file. Check git blame - if the pattern exists elsewhere from before the branch, it's not slop.
