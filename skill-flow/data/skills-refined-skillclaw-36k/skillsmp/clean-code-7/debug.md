# Debug Code Removal

Removes debugging artifacts before code is merged.

## Patterns to Remove

### Console/Print Statements

**JavaScript/TypeScript:**
```javascript
console.log(...)
console.debug(...)
console.trace(...)
console.table(...)
console.dir(...)
console.time(...) / console.timeEnd(...)
console.group(...) / console.groupEnd(...)
debugger;
```

**Python:**
```python
print(...)           # unless intentional output
pprint(...)
breakpoint()
import pdb; pdb.set_trace()
import ipdb; ipdb.set_trace()
```

**Go:**
```go
fmt.Println(...)     // in non-CLI code
fmt.Printf(...)      // debug prints
```

### TODO/FIXME Comments

**Remove if:**
- Generic placeholders: `// TODO: implement this`
- Reminders that should be issues: `// FIXME: this is broken`
- AI artifacts: `// TODO: as discussed above`
- Vague notes: `// TODO: clean this up later`

**Keep if:**
- References a ticket: `// TODO(JIRA-123): ...`
- Meaningful and actionable
- Existed before the branch

### Temporary Code
- Hardcoded test values: `const userId = "test-user-123"`
- Commented-out code blocks
- Mock implementations marked as temporary
- Sleep/delay calls for debugging
- Forced conditions: `if (true || actualCondition)`

### Debug Utilities
- Imports of debug-only libraries
- Custom debug helper functions defined inline
- Verbose logging of entire objects
- `JSON.stringify(obj, null, 2)` for debugging

## Safety Checks

**Do NOT remove:**
- Intentional user-facing console output (CLI tools)
- Error logging that's part of error handling
- Structured logging for observability
- TODO comments referencing real tickets
