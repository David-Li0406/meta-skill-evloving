# Command Accuracy Guidelines

## Overview

These guidelines help improve first-attempt success rate and reduce failed commands. The goal is to execute commands correctly the first time through verification and best practices.

## Core Principles

1. **Verify Before Executing** - Check assumptions before running commands
2. **Follow Existing Patterns** - Match what already works in the codebase
3. **Read Definitions First** - Understand types/interfaces before implementing
4. **Use Cross-Platform Paths** - Always use forward slashes
5. **Test Incrementally** - Validate each step before proceeding

## Path Accuracy

### DO: Use Forward Slashes

✅ **Pattern: Cross-Platform Paths**
```
app/ui/components/button.tsx
app/db/prisma/schema.prisma
.claude/skills/summary-generator/SKILL.md
```

**Why:** Works on Windows, macOS, and Linux consistently

✅ **Pattern: Verify Path Exists**
```
1. Glob pattern="app/ui/components/button*"
2. Read app/ui/components/button.tsx
```

**Why:** Confirms file exists and gets exact path/case

### DON'T: Use Backslashes

❌ **Anti-Pattern: Windows-Style Paths**
```
app\ui\components\button.tsx
app\db\prisma\schema.prisma
```

**Why:** Fails in most tools, only works in Windows cmd

❌ **Anti-Pattern: Assume Path Without Checking**
```
Read app/ui/components/Button.tsx  # Might be button.tsx
Read src/utils/helper.ts  # Might be in lib/utils/
```

**Better:**
```
1. Glob pattern="**/button*.tsx"  # Find exact path
2. Read app/ui/components/button.tsx  # Use confirmed path
```

### Case Sensitivity

✅ **Pattern: Match Exact Case**
```
1. Glob finds: app/ui/components/AutoAssignDialog.tsx
2. Read app/ui/components/AutoAssignDialog.tsx  # Exact match
```

❌ **Anti-Pattern: Wrong Case**
```
Glob finds: autoAssignDialog.tsx
Read: AutoAssignDialog.tsx  # Case mismatch
```

**Why:** Linux is case-sensitive; wrong case = file not found

## Import Path Accuracy

### DO: Check Existing Imports

✅ **Pattern: Grep for Existing Usage**
```
# Before using an import, check how others use it
Grep pattern="import.*requireRole" path="app/ui/app/api"

# Results show: import { requireRole } from "@/lib/authz"
# Now use the same path
```

**Why:** Confirms correct import path and usage pattern

✅ **Pattern: Verify Module Exports**
```
# Check what a module exports
Read app/ui/lib/prisma.ts

# See: export const prisma = new PrismaClient()
# Use: import { prisma } from "@/lib/prisma"
```

**Why:** Ensures you're importing what actually exists

### DON'T: Guess Import Paths

❌ **Anti-Pattern: Assumption Without Verification**
```
import { requireRole } from "@/lib/auth"  # Guessed
# Error: Module not found

# Should have checked existing files first
```

❌ **Anti-Pattern: Wrong Import Style**
```
import prisma from "@/lib/prisma"  # Default import
# But module uses: export const prisma

# Should be: import { prisma } from "@/lib/prisma"
```

**Prevention:**
1. Grep for existing imports in similar files
2. Read the module to see export style
3. Match existing patterns exactly

## Type Safety

### DO: Read Interfaces First

✅ **Pattern: Understand Types Before Implementing**
```
# Before creating component, read types
Read app/ui/components/room-assignments/room-assignment-dialog.tsx

# See interface Room { _count: { studentAssignments: number } }
# Match this in new component
```

**Why:** Prevents type mismatches and interface refactoring

✅ **Pattern: Check Existing Usage**
```
# Before passing props, check how parent uses them
Read app/ui/app/students/grades/page.tsx

# See: rooms={grade.rooms}  # Uses _count pattern
# Match this pattern in dialog component
```

**Why:** Ensures type compatibility across components

### DON'T: Assume Type Structure

❌ **Anti-Pattern: Guessing Interface Shape**
```
interface Room {
  currentCount: number  # Guessed
}

# But existing code uses:
interface Room {
  _count: { studentAssignments: number }
}
```

**Prevention:**
1. Read existing component interfaces
2. Check how parent components pass data
3. Match established patterns

❌ **Anti-Pattern: Using Wrong Property Names**
```
session.userId  # Wrong
# Error: Property 'userId' does not exist

# Should be: session.user.id
```

**Prevention:**
1. Read type definitions for session
2. Check existing API route usage
3. Use IDE autocomplete hints from errors

## Edit Tool Accuracy

### DO: Copy Exact Strings

✅ **Pattern: Read Then Edit**
```
1. Read file.ts lines 10-20
   # Output shows:
   # 15→  const user = session.userId

2. Edit file.ts
   old_string: "  const user = session.userId"  # Exact copy
   new_string: "  const user = session.user.id"
```

**Why:** Exact match prevents "string not found" errors

✅ **Pattern: Include Enough Context**
```
# If old_string appears multiple times, add more context
old_string: `export async function POST(req: NextRequest) {
  const session = await getSession()
  const userId = session.userId`

# Instead of just: "const userId = session.userId"
```

**Why:** Makes the match unique in the file

### DON'T: Modify Whitespace

❌ **Anti-Pattern: Changing Indentation**
```
Read output shows: "  const user = session.userId"  # 2 spaces
Edit uses: "    const user = session.userId"  # 4 spaces

# Result: String not found error
```

**Prevention:** Copy exactly from Read output, including whitespace

❌ **Anti-Pattern: Forgetting to Read First**
```
Edit file.ts
  old_string: "something I think is there"
  # Error: String not found
```

**Prevention:** Always Read the file first to see exact content

## Regex and Grep Accuracy

### DO: Escape Special Characters

✅ **Pattern: Literal Braces**
```
# To find: interface{}
Grep pattern="interface\\{\\}"

# To find: function()
Grep pattern="function\\(\\)"
```

**Why:** Braces and parentheses are regex special characters

✅ **Pattern: Test Pattern Incrementally**
```
1. Start simple: Grep pattern="interface"
2. Add specificity: Grep pattern="interface.*\\{\\}"
3. Final pattern: Grep pattern="interface\\s+\\w+\\s*\\{\\}"
```

**Why:** Easier to debug when pattern grows incrementally

### DON'T: Use Unescaped Special Characters

❌ **Anti-Pattern: Literal Special Characters**
```
Grep pattern="interface{}"  # Wrong
# Braces have special meaning in regex
```

**Better:**
```
Grep pattern="interface\\{\\}"  # Escaped
```

❌ **Anti-Pattern: Overly Complex Regex**
```
Grep pattern="(?:interface|type)\\s+(?!.*extends)[^{]+\\{(?:[^{}]*|\\{[^{}]*\\})*\\}"
# Too complex, hard to debug
```

**Better:**
```
Grep pattern="interface\\s+\\w+"
# Simpler, easier to verify
```

## API Route Accuracy

### DO: Match Async Route Patterns

✅ **Pattern: Check Next.js Route Params**
```
# Next.js 15 uses Promise<{ id: string }> for params
type RouteParams = {
  params: Promise<{ id: string }>
}

export async function PATCH(
  req: NextRequest,
  { params }: RouteParams
) {
  const { id } = await params  # Must await
}
```

**Why:** Next.js 15 changed params to be async

✅ **Pattern: Verify Auth Pattern**
```
# Check existing API routes first
Grep pattern="requireRole" path="app/ui/app/api"

# See pattern: const { session, error } = await requireRole([...])
# Match this exactly
```

**Why:** Consistent with existing authentication pattern

### DON'T: Use Outdated Patterns

❌ **Anti-Pattern: Synchronous Params (Next.js 14)**
```
export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }  # Old pattern
) {
  const { id } = params  # No await
}
```

**Prevention:** Check existing route files for current pattern

❌ **Anti-Pattern: Wrong Session Access**
```
const userId = session.userId  # Wrong
# Should be: session.user.id
```

**Prevention:** Read existing auth usage in API routes

## Verification Checklist

Before executing each command, verify:

### For Read Operations
- [ ] Path uses forward slashes
- [ ] File path exists (Glob to verify)
- [ ] Case matches exactly
- [ ] Not reading generated files (node_modules, .next, dist)

### For Edit Operations
- [ ] Recently read the file
- [ ] Copied old_string exactly from Read output
- [ ] Included enough context if not unique
- [ ] Preserved exact whitespace/indentation
- [ ] New string is different from old string

### For Write Operations
- [ ] Parent directory exists
- [ ] Not overwriting existing file (should use Edit)
- [ ] Path uses forward slashes
- [ ] Have appropriate permissions

### For Import Statements
- [ ] Grepped for existing imports in similar files
- [ ] Verified module exports (default vs named)
- [ ] Used correct path alias (@/, ~/, etc.)
- [ ] Import style matches export style

### For Type Usage
- [ ] Read interface/type definitions
- [ ] Checked existing component usage
- [ ] Property names are correct
- [ ] Type structure matches codebase

### For API Routes
- [ ] Checked Next.js version pattern
- [ ] Params handling matches existing routes
- [ ] Auth pattern matches existing routes
- [ ] Response format is consistent

## Common Error Prevention

### Path Errors
**Prevention Steps:**
1. Always use forward slashes
2. Glob to verify file exists
3. Match exact case from Glob results
4. Check parent directory exists (for Write)

### Import Errors
**Prevention Steps:**
1. Grep for existing imports in similar files
2. Read module to check export style
3. Use same import pattern as existing code
4. Verify module path exists

### Type Errors
**Prevention Steps:**
1. Read interface definitions before implementing
2. Check how existing components use types
3. Match property names exactly
4. Verify optional vs required fields

### Edit Errors
**Prevention Steps:**
1. Read file immediately before editing
2. Copy old_string exactly (including whitespace)
3. Include enough context to be unique
4. Test with small changes first

## Recovery Strategies

When a command fails:

### Immediate Actions
1. **Read the error message carefully**
   - Identifies exact issue
   - Often suggests the fix

2. **Check assumptions**
   - Verify file path exists
   - Confirm import path is correct
   - Validate type expectations

3. **Look for existing patterns**
   - How do other files handle this?
   - What's the established pattern?
   - Match existing code exactly

### Quick Fixes
- **Path error:** Glob to find correct path
- **Import error:** Grep to find correct import
- **Type error:** Read type definition
- **Edit error:** Re-read file for exact string

### Learning
After fixing an error:
1. Note the root cause
2. Add to prevention checklist
3. Apply learning to similar situations
4. Update patterns for next time

## Success Metrics

Target accuracy metrics:

**Overall:**
- Success Rate: 95%+
- Critical Errors: 0
- High-Severity Errors: <2 per session
- Time wasted on retries: <5 minutes per session

**By Category:**
- Path Errors: <1 per session
- Import Errors: <1 per session
- Type Errors: <2 per session
- Edit Errors: <1 per session

## Best Practices Summary

1. **Always verify paths** with Glob before Read/Edit/Write
2. **Always check existing patterns** before implementing
3. **Always read type definitions** before using types
4. **Always use forward slashes** in all paths
5. **Always copy exactly** when using Edit tool
6. **Always grep for imports** before adding new ones
7. **Always test incrementally** rather than all at once
8. **Always learn from errors** and update patterns

## Remember

The goal is **getting it right the first time** through:
- Verification before execution
- Following existing patterns
- Understanding types and interfaces
- Using cross-platform conventions
- Learning from each error

Spending 30 seconds to verify is better than spending 5 minutes fixing errors.
