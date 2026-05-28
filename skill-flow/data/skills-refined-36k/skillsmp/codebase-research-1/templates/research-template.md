# Codebase Research: {TICKET-ID}

**Date**: {YYYY-MM-DD}
**Researcher**: AI Agent (Bug Researcher)
**Bug**: {Title from bug-context.md}
**Status**: Research Complete - Pending Verification

---

## Research Summary

[2-3 sentence summary of what was discovered about the bug-related code. Focus on WHAT EXISTS, not what should change.]

---

## Detailed Findings

### Code Locations

| File | Lines | Component | Description |
|------|-------|-----------|-------------|
| `path/to/file.ts` | XX-YY | [name] | [What this code does] |
| `path/to/other.ts` | XX | [name] | [What this code does] |

### Code Flow Analysis

#### Entry Points
[How the bug-related code is triggered]

- `[file.ts:XX]` - [Description of trigger]
- `[other.ts:YY]` - [Alternative entry point]

#### Execution Flow

```
[trigger description]
    ↓
[step 1: what happens] → file.ts:XX
    ↓
[step 2: what happens] → other.ts:YY
    ↓
[step 3: what happens] → service.ts:ZZ
    ↓
[output/result]
```

#### Dependencies

| Dependency | Location | Purpose |
|------------|----------|---------|
| [name] | `file.ts:XX` | [How it's used] |
| [external package] | `package.json` | [What it provides] |

#### Error Handling

| Location | Error Type | Handling |
|----------|------------|----------|
| `file.ts:XX` | [ErrorType] | [What happens when error occurs] |
| `service.ts:YY` | [ErrorType] | [What happens when error occurs] |

### Related Patterns

#### Similar Code
[Other places in the codebase with similar patterns - for context, not comparison]

| File | Lines | Similarity |
|------|-------|------------|
| `similar/file.ts` | XX-YY | [How it's similar - factually] |

#### Related Tests

| Test File | Line | What It Tests |
|-----------|------|---------------|
| `test/file.test.ts` | XX | [Description of test] |
| `test/integration.test.ts` | YY | [Description of test] |

#### Historical Context
[From git history if available - factual observations only]

- Commit `abc123` (YYYY-MM-DD): "[commit message]" - modified `file.ts`
- PR #XXX: "[title]" - relevant context

---

## Code Snippets

### {Component 1 Name}
**File**: `path/to/file.ts:XX-YY`
```typescript
// EXACT code from source - copied verbatim
[code snippet]
```

### {Component 2 Name}
**File**: `path/to/other.ts:XX-YY`
```typescript
// EXACT code from source - copied verbatim
[code snippet]
```

---

## Open Questions

[Areas that couldn't be fully researched - questions for the verifier or RCA phase]

1. [Question about behavior that couldn't be determined]
2. [Question about edge case not found in code]
3. [Question about configuration or environment]

---

## References

- Bug Context: `context/bugs/{TICKET-ID}/bug-context.md`
- Hypotheses: `context/bugs/{TICKET-ID}/research/hypothesis.md`
