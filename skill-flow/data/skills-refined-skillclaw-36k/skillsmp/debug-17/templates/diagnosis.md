# Diagnosis Template

## Symptom
[Exact error message or unexpected behavior]

```
[Error output if applicable]
```

**Reproduction steps:**
1. Step to reproduce
2. Step to reproduce
3. Observe: [what happens]

**Expected:** [what should happen]
**Actual:** [what actually happens]

## Root Cause
[Why it's failing — the actual problem, not the symptom]

**Component:** `path/to/file.ext:line`
**Mechanism:** How the bug manifests

## Evidence

| Source | Observation |
|--------|-------------|
| `file:line` | Code does X instead of Y |
| Command output | Shows unexpected value |
| Log entry | Error at timestamp |

## Fix Options

### Option A: [Name]
**Approach:** What to change
**Files:** `path/to/file.ext`
**Tradeoffs:**
- Pro: ...
- Con: ...

### Option B: [Name]
**Approach:** What to change
**Files:** `path/to/file.ext`
**Tradeoffs:**
- Pro: ...
- Con: ...

## Recommended
**Option [A/B]** because [rationale]

**Estimated scope:** [small/medium/large]
**Risk:** [low/medium/high]

## Verification Plan
After fix, verify by:
1. Run [command] — should pass
2. Check [behavior] — should work
3. Regression: [other areas to test]
