# Enforcement Rules

**Purpose**: Non-negotiable requirements for intelligence-first code analysis.

---

## Rule 1: No Naked Claims

**Requirement**: Every claim MUST have traceable evidence with file:line references.

### ❌ Violation

```markdown
The login form has a bug in the useEffect.
```

**Problems**:
- No file location
- No line number
- No evidence trail
- Can't verify claim

### ✅ Correct

```markdown
The login form has a bug at src/LoginForm.tsx:45 in the useEffect hook.

Evidence:
- Intel Query: project-intel.mjs --symbols src/LoginForm.tsx
- Result: useEffect at line 45 with dependency [state]
- MCP Verify: Ref MCP confirms dependencies should include all referenced values
- Targeted Read: Lines 40-50 show effect mutates state while depending on it
```

**Why This Matters**:
- Enables verification
- Provides audit trail
- Saves tokens (others can read exact lines)
- Ensures accuracy

### Evidence Requirements

**Minimum Evidence for Any Claim**:
1. **File location**: Exact path (e.g., `src/components/LoginForm.tsx`)
2. **Line reference**: Specific line or range (e.g., `:45` or `:40-50`)
3. **Intelligence source**: Which query found it
4. **Verification**: MCP or targeted read confirming finding

**Example Evidence Chain**:
```markdown
Claim: Component re-renders infinitely

Evidence Chain:
1. Search: project-intel.mjs --search "LoginForm" --type tsx
   → Found src/components/LoginForm.tsx

2. Symbols: project-intel.mjs --symbols src/components/LoginForm.tsx
   → useEffect hook at line 45

3. Read: sed -n '40,50p' src/components/LoginForm.tsx
   → useEffect(() => { setUser({...user, lastLogin: Date.now()}) }, [user])

4. MCP: ref_search_documentation "React useEffect dependencies"
   → "Every value referenced inside effect must be in dependency array"

Conclusion: Re-render caused by useEffect at line 45 mutating state it depends on.
```

---

## Rule 2: Intel Before Reading

**Requirement**: Query project-intel.mjs BEFORE reading any files.

### ❌ Violation

```bash
# Agent reads entire file (1000 lines, ~3000 tokens)
cat src/LoginForm.tsx

# or
Read src/LoginForm.tsx
```

**Problems**:
- 3000+ tokens for 1000-line file
- Most content irrelevant
- Wastes context window
- Slower analysis

### ✅ Correct

```bash
# Step 1: Query intel first (~50 tokens)
project-intel.mjs --symbols src/LoginForm.tsx --json

# Result shows:
# - LoginForm function at line 12
# - useEffect hook at line 45
# - useState calls at lines 15, 18, 21

# Step 2: Read ONLY relevant lines (~100 tokens)
sed -n '40,60p' src/LoginForm.tsx
```

**Token Savings**: 96% reduction (150 tokens vs 3000 tokens)

### Required Intel Query Sequence

**For Every Analysis**:

1. **Overview** (if first analysis):
   ```bash
   project-intel.mjs --overview --json
   ```
   Tokens: ~50

2. **Search** (find relevant files):
   ```bash
   project-intel.mjs --search "<keyword>" --type <filetype> --json
   ```
   Tokens: ~100

3. **Symbols** (find functions/classes):
   ```bash
   project-intel.mjs --symbols path/to/file.ts --json
   ```
   Tokens: ~150 per file

4. **Dependencies** (understand relationships):
   ```bash
   project-intel.mjs --dependencies path/to/file.ts --direction upstream --json
   project-intel.mjs --dependencies path/to/file.ts --direction downstream --json
   ```
   Tokens: ~200 total

**Total Intel Cost**: ~500 tokens
**Baseline File Reading Cost**: 5000-20000 tokens
**Savings**: 90-97%

### Enforcement Mechanism

Before ANY file read operation, verify:
- [ ] Overview query executed (if first analysis)
- [ ] Search query executed (found relevant files)
- [ ] Symbols query executed (identified specific locations)
- [ ] Dependencies traced (understood relationships)
- [ ] Intel results saved to /tmp/ for evidence

**If ANY checklist item is unchecked → STOP and complete intel queries**

---

## Rule 3: MCP for Authority

**Requirement**: Verify library/framework behavior with authoritative MCP sources, not memory or assumptions.

### ❌ Violation

```markdown
Based on my knowledge, useEffect should include all dependencies.
```

**Problems**:
- No source cited
- Can't verify
- May be outdated
- Lacks authority

### ✅ Correct

```markdown
MCP Verification (Ref): ref_search_documentation "React useEffect dependencies"

Official React docs confirm:
"Every value referenced inside the effect function must be included in the dependency array."

Source: https://react.dev/reference/react/useEffect
```

**Why This Matters**:
- Authoritative source
- Up-to-date information
- Verifiable claim
- Proper attribution

### When to Use MCP Verification

**MUST Use MCP When**:
- Library/framework behavior in question
- Best practices verification
- API usage patterns
- Type definitions
- Performance characteristics

**Available MCP Tools**:

| MCP Tool | Use For | Example Query |
|----------|---------|---------------|
| **Ref** | Library docs (React, Next.js, TypeScript) | `ref_search_documentation "React hooks"` |
| **Context7** | External package docs | `context7_get_docs "lodash"` |
| **Supabase** | Database schema, RLS policies | `supabase_get_schema "users"` |

### MCP Verification Pattern

**Template**:
```markdown
## Intel Finding
[What intelligence queries revealed]

## MCP Verification
**Tool:** [Which MCP tool]
**Query:** [Exact query executed]
**Result:** [What authoritative source says]

## Comparison
- **Intel shows:** [From project-intel.mjs]
- **Docs require:** [From MCP verification]
- **Conclusion:** [Agreement or discrepancy]
```

**Example**:
```markdown
## Intel Finding
useEffect at src/LoginForm.tsx:45 has dependency array [user]

## MCP Verification
**Tool:** Ref MCP
**Query:** ref_search_documentation "React useEffect dependencies"
**Result:** "Every value referenced inside the effect function, including props, state, and derived values, must be included in the dependency array."
**Source:** https://react.dev/reference/react/useEffect

## Comparison
- **Intel shows:** useEffect(() => { setUser({...user, lastLogin: Date.now()}) }, [user])
- **Docs require:** Both `user` and `setUser` should be in dependencies
- **Conclusion:** Missing `setUser` in dependency array ✗
- **Root Cause:** Effect mutates state while depending on it → infinite loop
```

### MCP Query Guidelines

**DO**:
- Query specific concepts: "React useEffect dependencies"
- Include context: "Next.js App Router routing"
- Target exact issue: "TypeScript generic constraints"

**DON'T**:
- Use vague queries: "React hooks"
- Query without intel context
- Skip MCP for framework issues
- Assume library behavior without verification

### Enforcement Mechanism

Before reporting any finding related to external libraries:
- [ ] Identified specific library/framework involved
- [ ] Determined which MCP tool to use (Ref, Context7, Supabase)
- [ ] Executed MCP query with specific question
- [ ] Documented MCP result in Evidence section
- [ ] Compared intel findings with MCP verification
- [ ] Noted any discrepancies or confirmations

**If ANY checklist item unchecked for library-related finding → STOP and verify with MCP**

---

## Rule Violations: Consequences

**Violation of Rule 1 (No Naked Claims)**:
- Analysis INVALID
- Cannot verify findings
- Must re-analyze with evidence

**Violation of Rule 2 (Intel Before Reading)**:
- Token budget exceeded
- Less context for actual reasoning
- Must restart with intel queries

**Violation of Rule 3 (MCP for Authority)**:
- Library assumptions unverified
- Risk of incorrect recommendations
- Must verify with MCP before finalizing

---

## Enforcement Checklist

Use this checklist at the end of every analysis to verify compliance:

```
Enforcement Verification:
- [ ] Rule 1: Every claim has file:line reference and evidence
- [ ] Rule 2: All intel queries executed before file reads
- [ ] Rule 3: All library behavior verified with MCP
- [ ] CoD^Σ trace complete with all 3 rules demonstrated
- [ ] Report includes evidence section with intel and MCP results
```

**Report is NOT complete until all checkboxes are checked.**

---

## Quick Reference

| Rule | Requirement | Verification |
|------|-------------|--------------|
| **Rule 1** | No naked claims | Every claim has file:line + evidence |
| **Rule 2** | Intel before reading | Intel queries → targeted reads only |
| **Rule 3** | MCP for authority | Library behavior verified with MCP |

**Remember**: These rules are non-negotiable. They ensure accuracy, efficiency, and verifiability of all code analysis.
