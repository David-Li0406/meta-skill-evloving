# Debugging Rules & Pitfalls

**Purpose**: Enforcement rules for CoD^Σ traces and common mistakes to avoid.

---

## Enforcement Rules

### Rule 1: Complete CoD^Σ Trace

Every bug diagnosis MUST include a complete CoD^Σ trace with file:line evidence.

**❌ Violation:**
```
The bug is in the discount calculation.
```

**Why This Fails:**
- No evidence provided
- No file:line reference
- No reasoning chain
- Cannot verify accuracy

**✓ Correct:**
```
Root cause: src/pricing/calculator.ts:67

CoD^Σ Trace:
Step 1: ParseError → TypeError at line 67
Step 2: IntelQuery → getDiscount returns undefined
Step 3: MCPVerify → TypeScript docs confirm optional chaining needed
Step 4: Conclusion → Missing null check causes error

Evidence:
- Error log: TypeError at calculator.ts:67
- Symbol query: getDiscount returns Discount | undefined
- Code read: Line 67 accesses .discount without null check
```

**Enforcement Mechanism:**
- Verify each step in trace has evidence source
- Confirm file:line references are accurate
- Check MCP queries are documented
- Validate conclusion follows logically from evidence

---

### Rule 2: Intel Before Reading

ALWAYS query project-intel.mjs BEFORE reading files.

**❌ Violation:**
```bash
# Read entire codebase looking for bug
cat src/**/*.ts  # Thousands of lines
```

**Why This Fails:**
- Wastes tokens (thousands vs hundreds)
- No targeted approach
- Slow and inefficient
- Misses intelligence benefits

**✓ Correct:**
```bash
# Intel-first approach
project-intel.mjs --search "calculateTotal" --json  # Find exact file
project-intel.mjs --symbols calculator.ts --json    # Find exact line
sed -n '62,75p' calculator.ts                       # Read only relevant lines
```

**Token Comparison:**
- Full file reading: ~8600 tokens
- Intel + targeted reads: ~750 tokens
- **Savings: 91%**

**Enforcement Mechanism:**
- Verify intel queries performed before any file reads
- Check targeted reads use line ranges from intel
- Confirm token efficiency documented

---

### Rule 3: Propose Fix with Verification

Every bug report MUST include specific fix and verification plan.

**❌ Violation:**
```
Fix: Change the code to handle undefined.
```

**Why This Fails:**
- No specific code provided
- No verification approach
- Cannot implement confidently
- May not solve root cause

**✓ Correct:**
```
Fix: Use optional chaining at line 67:
  getDiscount(code)?.discount ?? 0

Verification:
- Test with invalid code: expect(total).toBe(100) // No discount
- Test with valid code: expect(total).toBe(90)   // Discount applied
- AC: No errors thrown for any input
```

**Enforcement Mechanism:**
- Check fix includes exact code changes
- Verify test plan covers all cases
- Confirm acceptance criteria are testable
- Validate fix addresses root cause

---

## Common Pitfalls

### Pitfall 1: Assumptions Without Verification

**Problem:**
Making assumptions about library behavior or return types without checking documentation.

**Impact:**
Wrong diagnosis, incorrect fix, wasted time.

**Example:**
```
❌ "getDiscount probably returns null for invalid codes"
→ Assumption not verified

✓ Use MCP to verify:
Ref MCP: "TypeScript Discount type definition"
→ Confirms: returns Discount | undefined (not null)
```

**Solution:**
- Use MCP tools to verify library behavior
- Check TypeScript types in code
- Query documentation for APIs
- Test edge cases manually if needed

---

### Pitfall 2: Skipping Intel Queries

**Problem:**
Reading full files immediately without using project-intel.mjs first.

**Impact:**
Token waste, slower analysis, less context for reasoning.

**Example:**
```
❌ Read src/pricing/**/*.ts (5000+ lines)
→ Wastes tokens, hard to find issue

✓ Query first, read targeted:
project-intel.mjs --search "error location"
sed -n 'X,Yp' identified-file.ts
→ 91% token savings
```

**Solution:**
- ALWAYS use intel queries before reading
- Use symbol analysis to find exact lines
- Read only identified sections
- Save intel results to /tmp/ for evidence

---

### Pitfall 3: Incomplete Reproduction Steps

**Problem:**
Not documenting exact steps to reproduce the error.

**Impact:**
Cannot verify fix works, may miss edge cases, difficult to write tests.

**Example:**
```
❌ "Error happens sometimes on checkout"
→ Cannot reliably reproduce

✓ Exact steps:
1. Add product to cart
2. Enter discount code "INVALID"
3. Click "Checkout"
4. Observe: TypeError at calculator.ts:67
→ Reliable reproduction
```

**Solution:**
- Document exact user actions
- Include input data (e.g., specific codes)
- Note environment (browser, OS if relevant)
- Provide error output verbatim

---

### Pitfall 4: No Fix Proposal

**Problem:**
Identifying root cause but not proposing a specific fix.

**Impact:**
Bug remains open, requires another person to design fix, delays resolution.

**Example:**
```
❌ "The problem is missing null check"
→ What specific change is needed?

✓ Propose exact fix:
```typescript
// Change line 67 from:
getDiscount(discountCode).discount

// To:
getDiscount(discountCode)?.discount ?? 0
```
→ Clear, actionable fix
```

**Solution:**
- Always include exact code changes
- Provide before/after comparison
- Explain why fix works
- Include verification approach

---

## Pitfall Summary Table

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Assumptions without verification | Wrong diagnosis | Use MCP to verify library behavior |
| Skipping intel queries | Token waste (91% overhead) | Always query before reading |
| Incomplete reproduction steps | Can't verify fix | Document exact steps + inputs |
| No fix proposal | Bug remains open | Propose specific code changes |

---

## Enforcement Checklist

Before finalizing bug diagnosis, verify:

- [ ] **Rule 1**: Complete CoD^Σ trace with file:line evidence
- [ ] **Rule 2**: Intel queries performed before file reads
- [ ] **Rule 3**: Specific fix proposed with verification plan
- [ ] **Pitfall 1**: No unverified assumptions
- [ ] **Pitfall 2**: Intel-first approach followed
- [ ] **Pitfall 3**: Reproduction steps documented
- [ ] **Pitfall 4**: Fix proposal included
