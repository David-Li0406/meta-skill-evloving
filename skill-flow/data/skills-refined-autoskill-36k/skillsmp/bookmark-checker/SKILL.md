---
name: bookmark-checker
description: Runs automated checks on Bookmark Vault code. Use when asked to verify code quality, run checks, or validate the project.
allowed-tools: Read, Bash, Glob
---

# Bookmark Checker

Automated validation and quality checks for Bookmark Vault.

## Available Checks

### Type Check
Verifies TypeScript compilation without errors and checks type safety.
- Runs: `./scripts/check-types.sh`
- Checks: `npx tsc --noEmit`
- Reports: TypeScript errors, type mismatches

### Component Check
Validates component sizes, structure, and pattern compliance.
- Runs: `./scripts/check-components.sh`
- Checks: Component line counts, prop interfaces, naming conventions
- Reports: Oversized components, pattern violations

### Test Check
Runs test suite and reports coverage metrics.
- Runs: `./scripts/check-tests.sh`
- Checks: Jest tests, coverage thresholds
- Reports: Test results, coverage gaps

### Validation Check
Validates Zod schemas and type coverage.
- Runs: `./scripts/check-validation.sh`
- Checks: Schema definitions, validation coverage
- Reports: Missing schemas, type gaps

## Execution Flow

When asked to check the project:

1. **Run checks in order**
   - Type Check (catches TypeScript errors)
   - Component Check (validates structure)
   - Validation Check (schema coverage)
   - Test Check (runs tests)

2. **Collect output from each**
   - Each script produces structured output
   - Exit codes indicate pass/fail
   - Details included in stdout

3. **Report pass/fail status**
   - Summary of which checks passed ✅
   - List of failed checks ❌
   - Issues grouped by severity

4. **Summarize issues found**
   - Critical: Blocking issues
   - Warning: Code quality issues
   - Info: Metrics and stats

## Script Outputs

All scripts follow standard conventions:

**Exit Codes:**
- `0`: All checks passed ✅
- `1`: Issues found (non-blocking warnings)
- `2`: Critical issues found (blocker errors)

**Output Format:**
```
[CHECK_TYPE] Status message
PASS: Specific metric (if success)
WARN: Issue detail (if warning)
ERROR: Critical issue (if error)
INFO: Informational stat
```

## Usage Examples

```bash
# Run all checks
Ask: "Run all checks on bookmark vault"

# Run specific check
Ask: "Run type check on the project"

# Run and report
Ask: "Check the bookmark vault and report any issues"

# Run and fix
Ask: "Run checks and fix any quick issues"
```

## Check Details

### Type Check (check-types.sh)
- Runs TypeScript compiler in noEmit mode
- Flags strict mode violations
- Reports unused variables
- Checks for implicit `any` types
- Time: ~5-10 seconds

### Component Check (check-components.sh)
- Analyzes each component file
- Checks line count (max 100 lines per component)
- Validates props interface exists
- Verifies "use client" directive where needed
- Checks naming conventions
- Time: ~2-3 seconds

### Validation Check (check-validation.sh)
- Counts type definitions in lib/types.ts
- Counts Zod schemas in lib/validation.ts
- Reports schema-type alignment
- Identifies missing schemas
- Calculates coverage percentage
- Time: ~1-2 seconds

### Test Check (check-tests.sh)
- Runs Jest test suite
- Reports test pass/fail count
- Shows coverage metrics
- Flags coverage gaps below threshold
- Time: ~20-30 seconds

## Expected Results

**When all checks pass:**
```
✅ Type Check: PASS (0 errors, 0 warnings)
✅ Component Check: PASS (72 components, 0 oversized)
✅ Validation Check: PASS (14 schemas, 87.5% coverage)
✅ Test Check: PASS (48 tests, 82% coverage)

Overall Status: ALL CHECKS PASSED 🎉
```

**When issues found:**
```
✅ Type Check: PASS
⚠️ Component Check: WARN (2 components >100 lines)
❌ Validation Check: FAIL (7 types missing schemas)
⚠️ Test Check: WARN (coverage below 80% target)

Overall Status: 2 WARNING, 1 FAILURE - Review issues
```

## Integration

### IDE Integration
Add to VS Code tasks.json:
```json
{
  "label": "Bookmark Checker",
  "type": "shell",
  "command": "bash",
  "args": ["${workspaceFolder}/.claude/skills/bookmark-checker/scripts/check-types.sh"],
  "problemMatcher": ["$tsc"]
}
```

### Pre-commit Hook
Add to .git/hooks/pre-commit:
```bash
#!/bin/bash
bash ./.claude/skills/bookmark-checker/scripts/check-types.sh
if [ $? -ne 0 ]; then
  echo "Type checks failed, aborting commit"
  exit 1
fi
```

### CI/CD Integration
Add to GitHub Actions workflow:
```yaml
- name: Bookmark Checks
  run: |
    bash .claude/skills/bookmark-checker/scripts/check-types.sh
    bash .claude/skills/bookmark-checker/scripts/check-components.sh
    bash .claude/skills/bookmark-checker/scripts/check-validation.sh
    bash .claude/skills/bookmark-checker/scripts/check-tests.sh
```

## Troubleshooting

**Scripts not executable:**
```bash
chmod +x ~/.claude/skills/bookmark-checker/scripts/*.sh
```

**Script path errors:**
- Scripts use `cd` to navigate to project root
- Ensure run from project directory or provide absolute paths

**Command not found errors:**
- Verify npm dependencies installed: `npm install`
- Check TypeScript: `npm list typescript`
- Check Jest: `npm list jest`

## When to Use This Skill

✅ **Use when:**
- Verifying code quality before commit
- Validating TypeScript changes
- Checking component structure changes
- Running tests after modifications
- Validating schema coverage
- Pre-deployment quality gate

❌ **Don't use when:**
- Need detailed IDE support (use VS Code extensions)
- Debugging specific tests (use Jest CLI directly)
- Need real-time file watching (use npm run dev)
- Analyzing performance (use profiling tools)

## Script Maintenance

Scripts are version-locked to project at:
- TypeScript config: `tsconfig.json`
- Jest config: `jest.config.js`
- Component directory: `components/`
- Test directory: `__tests__/`

Update scripts if project structure changes.
