# Phase 5: Bug Report Generation

**Purpose**: Create comprehensive bug report using template with complete evidence and fix specification.

---

## Template Reference

Use **@.claude/templates/bug-report.md** to create structured report.

---

## Bug Report Structure

```markdown
---
bug_id: "checkout-discount-500"
severity: "critical"
status: "open"
assigned_to: "executor-agent"
---

# Bug Report: 500 Error on Checkout with Discount

## Symptom
[Full symptom from Phase 1]

## CoD^Σ Trace
[Complete trace from Phase 4]

## Root Cause
**Location:** src/pricing/calculator.ts:67

**Issue:** Missing null check before accessing .discount property

**Why It Fails:**
- getDiscount() returns Discount | undefined
- When discount code invalid/inactive, returns undefined
- Code attempts undefined.discount → TypeError

## Fix Specification
**Approach:** Add optional chaining

**Changes Required:**
```typescript
// Before (buggy)
const discountAmount = discountCode
  ? getDiscount(discountCode).discount * subtotal
  : 0

// After (fixed)
const discountAmount = discountCode
  ? (getDiscount(discountCode)?.discount ?? 0) * subtotal
  : 0
```

**Reason:**
- Optional chaining (?.) returns undefined if getDiscount returns undefined
- Nullish coalescing (?? 0) provides default value
- No TypeError, discount defaults to 0 for invalid codes

## Verification
**Test Plan:**
```typescript
it('handles invalid discount codes gracefully', () => {
  const cart = { items: [{ price: 100, quantity: 1 }] }
  const total = calculateTotal(cart, 'INVALID_CODE')
  expect(total).toBe(100) // No discount applied, no error
})
```

**Acceptance Criteria:**
- [ ] Invalid discount codes return subtotal (no discount)
- [ ] Valid discount codes still apply correctly
- [ ] No TypeError thrown
```

---

## File Naming Convention

Follow timestamp naming: `YYYYMMDD-HHMM-bug-<id>.md`

**Examples:**
- `20250123-1430-bug-checkout-discount-500.md`
- `20250123-1445-bug-login-timeout.md`
- `20250123-1500-bug-infinite-rerender.md`

---

## Required Sections

Every bug report MUST include:

1. **Symptom**: Complete reproduction steps and error output (from Phase 1)
2. **CoD^Σ Trace**: Full evidence chain with file:line references (from Phase 4)
3. **Root Cause**: Specific file:line + explanation of why it fails
4. **Fix Specification**: Exact code changes with before/after
5. **Verification**: Test plan + acceptance criteria

**Optional Sections:**
- **Impact Analysis**: How many users affected, severity justification
- **Workarounds**: Temporary solutions until fix deployed
- **Related Issues**: Links to similar bugs or dependencies

---

## Enforcement Checklist

Before saving bug report, verify:

- [ ] Bug report uses template format
- [ ] CoD^Σ trace complete with all evidence steps
- [ ] Root cause specifies exact file:line location
- [ ] Fix proposal provided with code examples
- [ ] Verification plan included with test cases
- [ ] Acceptance criteria are testable and specific
- [ ] File named with timestamp format

**Next Step**: Pass bug report to implement-and-verify skill for fix implementation.
