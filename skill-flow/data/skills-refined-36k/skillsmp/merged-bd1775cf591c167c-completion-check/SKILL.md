---
name: completion-check
description: Use this skill to verify that infrastructure is properly connected and operational before marking it as complete.
---

# Completion Check: Verify Infrastructure Is Wired

When building infrastructure, verify it's actually connected to the system before marking as complete.

## Pattern

Infrastructure is not done when the code is written - it's done when it's wired into the system and actively used. Dead code (built but never called) is wasted effort.

## DO

1. **Trace the execution path** - Follow from user intent to actual code execution:
   ```bash
   # Example: Verify Task tool spawns correctly
   grep -r "<command>" src/
   ```

2. **Check hooks are registered**, not just implemented:
   ```bash
   # Hook exists?
   ls -la .claude/hooks/<hook-name>.sh

   # Hook registered in settings?
   grep "<hook-name>" .claude/settings.json
   ```

3. **Verify database connections** - Ensure infrastructure uses the right backend:
   ```bash
   # Check connection strings
   grep -r "<database-type>://" src/
   grep -r "<incorrect-database-type>:" src/  # Should NOT find if <database-type> expected
   ```

4. **Test end-to-end** - Run the feature and verify infrastructure is invoked:
   ```bash
   # Add debug logging
   echo "DEBUG: <feature-name> invoked" >> /tmp/debug.log

   # Trigger feature
   uv run python -m <feature-module>

   # Verify infrastructure was called
   cat /tmp/debug.log
   ```

5. **Search for orphaned implementations**:
   ```bash
   # Find functions defined but never called
   ast-grep --pattern 'async function $NAME() { $$$ }' | \
     xargs -I {} grep -r "{}" src/
   ```

## DON'T

- Mark infrastructure "complete" without testing execution path.
- Assume code is wired just because it exists.
- Build parallel systems (e.g., Task tool vs <alternative-tool>).
- Use wrong backends (e.g., SQLite when PostgreSQL is architected).
- Skip end-to-end testing ("it compiles" ≠ "it runs").

## Completion Checklist

Before declaring infrastructure complete:

- [ ] Traced execution path from entry point to infrastructure.
- [ ] Verified hooks are registered in .claude/settings.json.
- [ ] Confirmed correct database/backend in use.
- [ ] Ran end-to-end test showing infrastructure invoked.
- [ ] Searched for dead code or parallel implementations.
- [ ] Checked configuration files match implementation.

## Example: DAG Task Graph

**Wrong approach:**
```
✓ Built <TaskGraph class>
✓ Implemented DAG dependencies
✓ Added spawn logic
✗ Never wired - Task tool still runs instead
✗ Used <incorrect-database> instead of <correct-database>
```

**Right approach:**
```
✓ Built <TaskGraph class>
✓ Wired into Task tool execution path
✓ Verified <command> is called
✓ Confirmed <correct-database> backend in use
✓ Tested: user calls <function>() → DAG spawns → <tasks> execute
✓ No parallel implementations found
```

## Source Sessions

- This session: Architecture gap discovery - DAG built but not wired, Task tool runs instead of spawn, <incorrect-database> used instead of <correct-database>.