# Architecture Validator - Examples

## Verification Commands

### Detect Domain → Infrastructure violations

Use the Grep tool to detect violations:

**Pattern:** `from '@/infrastructure|from '@/application|from '@/presentation|from 'mongoose'|from 'next/|from 'react'`
**Path:** `src/domain/`
**Output mode:** `files_with_matches`

If **NO matches** → ✅ Domain is pure
If **MATCHES found** → ❌ CRITICAL VIOLATION

### Detect Application → Infrastructure violations

Use the Grep tool to detect violations:

**Pattern:** `from '@/infrastructure|from '@/presentation`
**Path:** `src/application/`
**Output mode:** `files_with_matches`

### Detect direct instantiation (no injection)

Use the Grep tool to detect violations:

**Pattern:** `new Mongo`
**Path:** `src/domain/use-cases/|src/application/`
**Output mode:** `files_with_matches`

If **MATCHES found** → ❌ Dependency injection violation

## Structured Validation Report

```markdown
# Hexagonal Architecture Validation Report

## ✅ Rules Respected

- ✅ Domain depends on nothing
- ✅ Application depends only on Domain
- ✅ Infrastructure implements Domain interfaces
- ✅ Dependency injection respected

## ❌ Violations Detected

### Critical (P0)

#### Violation 1 : Domain imports Infrastructure

- **File** : src/domain/use-cases/CreateTicket.ts:15
- **Forbidden import** : `import ... from '@/infrastructure/database'`
- **Impact** : Domain is no longer independent
- **Solution** :
  1. Create an interface in `src/domain/repositories/`
  2. Implement in `src/infrastructure/repositories/`
  3. Inject via constructor

## 📊 Statistics

- Domain files analyzed : X
- Critical violations : X
- Important violations : X

## ✅ Verdict

[ARCHITECTURE VALID / VIOLATIONS TO FIX]
```

## TypeScript Strict - Checklist

```typescript
// ❌ AVOID
const getValue = (obj: any) => obj.value; // any
const id = value!; // non-null assertion

// ✅ PREFER
const getValue = (obj: { value: string }) => obj.value; // Typing
const id = value ?? defaultValue; // Optional or guard
```

Check in `tsconfig.json` : `"strict": true`
