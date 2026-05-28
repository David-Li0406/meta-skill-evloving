---
name: pass-workflow
description: "Universal guide for all unmangleJS pass development tasks. Covers creating, modifying, debugging, refactoring, reviewing, and documenting passes. Integrates with existing project documentation - see CLAUDE.md for complete Pass System guide."
---

# Pass Development Workflow

Universal guide for all unmangleJS pass operations.

## 📚 Essential Prerequisites

**Before working on passes, read these:**

1. **[Pass System Guide → CLAUDE.md](../../CLAUDE.md#pass-system)**
   - Complete guide to pass architecture and lifecycle
   - Development workflow and best practices
   - Five-file sync rule

2. **[Babel API Gotchas → docs/en/babel-api-gotchas.md](../../docs/en/babel-api-gotchas.md)**
   - Critical pitfalls when working with Babel
   - Scope and binding issues
   - Reference invalidation

3. **[Utils Overview → docs/en/utils-overview.md](../../docs/en/utils-overview.md)**
   - Available utility functions
   - When to use utils vs implementing in pass

---

## 🎯 Quick Task Navigator

**What do you want to do?**

### 🆕 Create New Pass

**Step-by-step workflow:**

1. **Design**: What obfuscation pattern does this pass target?
2. **Implement**: See [Pass Structure → references/pass-structure.md](references/pass-structure.md)
3. **Test**: See [Testing Guide → references/testing-guide.md](references/testing-guide.md)
4. **Document**: Follow pattern in `docs/en/passes/constant-folding.md`
5. **Register**: Add to `src/passes/registry.ts` and `src/passes/index.ts`

**Quick Template:**
```bash
# Copy existing pass as template
cp src/passes/constant-folding.ts src/passes/my-pass.ts
# Edit to implement your transformation
```

**Validation:**
```bash
npm test tests/passes/my-pass.test.ts
npm run lint
npm run build
```

---

### ✏️ Modify Existing Pass

**When adding transformations or fixing bugs:**

1. **Read current implementation**:
   ```bash
   # View all files for the pass
   ls -1 src/passes/<name>.ts \
        tests/passes/<name>.test.ts \
        examples/<name>.js \
        docs/en/passes/<name>.md \
        docs/zh-CN/passes/<name>.md
   ```

2. **Add tests first** (TDD):
   ```typescript
   // tests/passes/<name>.test.ts
   it("should handle new pattern", async () => {
     const input = "<obfuscated>";
     const { code } = await unmangle(input, [yourPass]);
     expect(code).toContain("<deobfuscated>");
   });
   ```

3. **Implement transformation**:
   - See [Babel patterns → CLAUDE.md](../../CLAUDE.md#babel-best-practices)
   - Use utils from `src/utils/` (see [Utils Overview → docs/en/utils-overview.md](../../docs/en/utils-overview.md))
   - Mark dirty: `ctx.markAstDirty()`, `ctx.markScopeDirty()`

4. **Update all 5 files**:
   - Implementation
   - Tests
   - Examples
   - English docs
   - Chinese docs

**Validation:**
```bash
npm test tests/passes/<name>.test.ts
./bin/unmanglejs.js examples/<name>.js -p
```

---

### 🐛 Debug Pass Issues

**Debugging workflow:**

1. **Isolate the issue**:
   ```bash
   cat > tmp/debug.js << 'EOF'
   // Minimal reproduction
   const x = <problematic code>;
   EOF

   ./bin/unmanglejs.js tmp/debug.js -p -d
   ```

2. **Check common issues**:
   - ❌ Forgot `ctx.markAstDirty()`?
   - ❌ Using `path.node` after `replaceWith()`?
   - ❌ Missing `path.skip()` after replacement?
   - ❌ Scope issues? Read [Babel API Gotchas → docs/en/babel-api-gotchas.md](../../docs/en/babel-api-gotchas.md)

3. **Add logging**:
   ```typescript
   ctx.log.at(path).debug("Checking pattern");
   ctx.log.at(path).debug("Pattern matched, transforming");
   ```

4. **Test with single pass**:
   ```bash
   ./bin/unmanglejs.js input.js -p <pass-name> -d
   ```

**Common debugging scenarios:**
- **Infinite loop**: Missing `path.skip()` → see [Babel Gotchas → docs/en/babel-api-gotchas.md](../../docs/en/babel-api-gotchas.md)
- **Wrong transformations**: Check transformation logic, verify with `tryEvaluateConstant()`
- **Scope errors**: Read [Scope Management → docs/en/babel-api-gotchas.md](../../docs/en/babel-api-gotchas.md)

---

### 🔄 Refactor Pass Code

**When to refactor:**
- Code duplication across passes → extract to `src/utils/`
- Complex visitor logic → simplify with helper functions
- Performance issues → see [CLI Performance → docs/en/cli.md](../../docs/en/cli.md)

**Extraction workflow:**

1. **Identify reusable logic**
2. **Extract to `src/utils/<name>.ts`**
3. **Create utils tests**: `tests/utils/<name>.test.ts`
4. **Update imports** in all passes using the logic
5. **Validate**:
   ```bash
   npm test tests/utils/
   npm test
   ```

**Example**:
```typescript
// BEFORE: In multiple passes
if (path.node.type === "Identifier" && path.node.name.length > 10) { }

// AFTER: Extract to utils
// src/utils/identifier.ts
export function isLongIdentifier(path: NodePath<t.Identifier>): boolean {
  return path.node.name.length > 10;
}

// In pass
import { isLongIdentifier } from "../utils/identifier.js";
if (isLongIdentifier(path)) { }
```

---

### 📝 Update Pass Documentation

**Documentation resources:**

**For structure reference:**
- [constant-folding.md → docs/en/passes/constant-folding.md](../../docs/en/passes/constant-folding.md)
- [proxy-object-removal.md → docs/en/passes/proxy-object-removal.md](../../docs/en/passes/proxy-object-removal.md)

**Five-file sync checklist:**
- [ ] `src/passes/<name>.ts` - Implementation
- [ ] `tests/passes/<name>.test.ts` - Tests
- [ ] `examples/<name>.js` - Examples
- [ ] `docs/en/passes/<name>.md` - English docs
- [ ] `docs/zh-CN/passes/<name>.md` - Chinese docs

**Validation:**
```bash
# Test examples match docs
./bin/unmanglejs.js examples/<name>.js -p

# Verify structure
grep "^##" docs/en/passes/<name>.md
grep "^##" docs/zh-CN/passes/<name>.md
# Should have matching section counts
```

---

### 🧪 Fix Pass Tests

**Testing resources:**
- [Testing Guide → references/testing-guide.md](references/testing-guide.md)
- [Test examples → tests/passes/constant-folding.test.ts](../../tests/passes/constant-folding.test.ts)

**Common test issues:**

1. **Tests timeout (>10s)**:
   - Cause: Infinite loop in visitor
   - Fix: Add `path.skip()` after replacement

2. **Transformation not applied**:
   - Cause: Pattern matching too restrictive
   - Fix: Adjust conditions, use `tryEvaluateConstant()`

3. **Test expects wrong output**:
   - Cause: Test is brittle or outdated
   - Fix: Update test to match actual deobfuscation behavior

---

### ⚙️ Adjust Pass Execution Order

**Pass order is defined in:** `src/passes/registry.ts`

**Current order:**
```typescript
export const PASS_REGISTRY: Record<string, Pass> = {
  "string-array-decode": allPasses.stringArrayDecodePass,
  "proxy-object-removal": allPasses.proxyObjectRemoval,
  "array-unpacking": allPasses.arrayUnpacking,
  // ... (see full file)
};
```

**To change order:**
1. Edit `src/passes/registry.ts`
2. Reorder keys (object key insertion order defines execution order)
3. Test with specific passes:
   ```bash
   ./bin/unmanglejs.js input.js -p pass1,pass2,pass3
   ```

**Verification:**
```bash
./bin/unmanglejs.js --list-passes
```

---

### 🗑️ Remove Deprecated Pass

**Safe removal workflow:**

1. **Remove from registry**:
   ```bash
   # src/passes/registry.ts - remove pass from PASS_REGISTRY
   # src/passes/index.ts - remove export
   ```

2. **Delete all 5 files**:
   ```bash
   rm src/passes/<name>.ts
   rm tests/passes/<name>.test.ts
   rm examples/<name>.js
   rm docs/en/passes/<name>.md
   rm docs/zh-CN/passes/<name>.md
   ```

3. **Validate**:
   ```bash
   npm test
   npm run build
   ./bin/unmanglejs.js --list-passes  # Verify removed
   ```

---

## 🔧 Essential Quick Reference

### The Five-File Rule

Each public pass SHOULD maintain 5 files:

1. `src/passes/<pass-name>.ts` - Implementation
2. `tests/passes/<pass-name>.test.ts` - Tests
3. `examples/<pass-name>.js` - Examples
4. `docs/en/passes/<pass-name>.md` - English docs
5. `docs/zh-CN/passes/<pass-name>.md` - Chinese docs

Note: Internal utility passes or helper transformations may omit documentation files.

### Critical Commands

```bash
# Test single pass
npm test tests/passes/<name>.test.ts

# Run with custom passes
./bin/unmanglejs.js input.js -p pass1,pass2,pass3

# Check pass order
./bin/unmanglejs.js --list-passes

# Debug output
./bin/unmanglejs.js input.js -p -d

# Test examples
./bin/unmanglejs.js examples/<name>.js -p
```

### Common Gotchas

- ❌ Don't forget `ctx.markAstDirty()` after modifications
- ❌ Don't use `path.node` after `replaceWith()`
- ❌ Don't call other passes directly
- ❌ Don't share context across passes
- ✅ Do use `tryEvaluateConstant()` for literals
- ✅ Do use `getIdentifierBinding()` for function names
- ✅ Do clone nodes with `t.cloneNode()` when reusing
- ✅ Do use `path.skip()` after replacement

### Utils Available

Import from `src/utils/`:
- `tryEvaluateConstant(path)` - Safely evaluate literals
- `getIdentifierBinding(path)` - Handle hoisting correctly
- `valueToExpression(value, node)` - Convert values to AST
- `generateUniqueName(scope)` - Create non-colliding names

See [Utils Overview → docs/en/utils-overview.md](../../docs/en/utils-overview.md) for complete reference.

---

## 📖 Detailed References

### Core Project Documentation

- **[CLAUDE.md - Pass System](../../CLAUDE.md#pass-system)** - Complete pass development guide
- **[Babel API Gotchas](../../docs/en/babel-api-gotchas.md)** - Critical Babel pitfalls
- **[Passes Overview](../../docs/en/passes-overview.md)** - All passes with examples
- **[Utils Overview](../../docs/en/utils-overview.md)** - Available utilities
- **[CLI Reference](../../docs/en/cli.md)** - Command-line usage

### Skill-Specific References

- **[Pass Structure → references/pass-structure.md](references/pass-structure.md)** - Implementation patterns
- **[Testing Guide → references/testing-guide.md](references/testing-guide.md)** - Test strategies
- **[Checklists → workflows/checklist.md](workflows/checklist.md)** - Universal checklists

### Example Pass Documentation

Use these as templates for documenting new passes:
- [constant-folding.md → docs/en/passes/constant-folding.md](../../docs/en/passes/constant-folding.md)
- [proxy-object-removal.md → docs/en/passes/proxy-object-removal.md](../../docs/en/passes/proxy-object-removal.md)
- [sequence-flattening.md → docs/en/passes/sequence-flattening.md](../../docs/en/passes/sequence-flattening.md)

---

## 🚀 Getting Started

**New to pass development?**

1. Read [Pass System → CLAUDE.md](../../CLAUDE.md#pass-system)
2. Read [Babel API Gotchas → docs/en/babel-api-gotchas.md](../../docs/en/babel-api-gotchas.md)
3. Study example: `src/passes/constant-folding.ts`
4. Follow [Create New Pass](#-create-new-pass) workflow above

**Experienced developer?**

Jump to the [task navigator](#-quick-task-navigator) above.
